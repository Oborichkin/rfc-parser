import re
import logging

from typing import List, Optional

logger = logging.getLogger(__name__)


class Section:
    def __init__(self, lines: Optional[List[str]] = None):
        self.type = None
        self.text = None

        if lines:
            self.parse_lines(lines)

    def parse_lines(self, lines):
        joined_lines = " ".join([line.strip() for line in lines])
        self.k = len(re.findall(r"[ \.\-\|:\\\/]", joined_lines)) / len(joined_lines)
        if self.k >= 0.25:  # TODO Need more complex determination of figures, schemes, tables etc.
            self.text = "\n".join(lines)
            self.type = "preformatted"
        else:
            self.text = joined_lines
            self.type = "text"

    @property
    def json(self):
        return {
            "type": self.type,
            "text": self.text
        }

    @staticmethod
    def from_json(obj) -> "Section":
        section = Section()
        section.text = obj.get("text")
        section.type = obj.get("type")
        return section


class Chapter:
    def __init__(self, title: Optional[str] = None, raw_sections: Optional[List[List[str]]] = None):
        self.title = title
        self.sections: List[Section] = [Section(sec) for sec in raw_sections] if raw_sections else []

    @property
    def text(self):
        return "\n\n".join([sec.text for sec in self.sections if sec.type == "text"])

    @property
    def json(self):
        return {
            "title": self.title,
            "sections": [section.json for section in self.sections]
        }

    @staticmethod
    def from_json(obj) -> "Chapter":
        ch = Chapter()
        ch.title = obj.get("title")
        ch.sections = [Section.from_json(sec) for sec in obj.get("sections")]
        return ch

    def __len__(self):
        return len(self.sections)


class RFC:

    PAGE_SEPARATOR = "\u000c"

    def __init__(self, text: Optional[str] = None):
        self.title = None
        self._sections = []
        self._chapters = []
        self._pages: List[str] = None

        if text:
            self._parse_rfc(text)

    @property
    def json(self):
        return {
            "title": self.title,
            "chapters": [ch.json for ch in self.chapters]
        }

    @staticmethod
    def from_json(obj) -> "RFC":
        rfc = RFC()
        rfc.title = obj.get("title")
        rfc._chapters = [Chapter.from_json(ch) for ch in obj.get("chapters", [])]
        return rfc

    @property
    def text(self):
        return "\n\n".join([ch.text for ch in self.chapters])

    def to_md(self, filename):
        with open(filename, "w+") as f:
            for ch in self.chapters:
                f.write(f"# {ch.title}\n\n")
                f.write(f"{ch.text}\n\n")

    def _parse_metadata(self, text):
        for match in re.finditer(r"\n\n^ +", text, re.MULTILINE):
            # TODO: parse metadata before skipping it
            return text[match.end():]
        raise Exception("Function _parse_metadata have not found the beggining of the RFC")

    def _parse_rfc(self, text):
        text = self._parse_metadata(text)
        self._pages = text.split(self.PAGE_SEPARATOR)

        first_page = True
        line_was_empty = True

        for page in self._pages:
            first_line = True
            if not first_page:
                lines = page.splitlines()[2:-1]     # Skip insignificant lines
            else:
                self.title = page.splitlines()[0].strip()
                lines = page.splitlines()[1:-1]
                first_page = False
            for i, line in enumerate(lines):
                if line:
                    # Chapter continues:
                    if line.startswith("   ") or not line_was_empty:
                        if (
                            line_was_empty and not first_line or
                            first_line and self._sections[-1]["paragraphs"][-1][-1].endswith(".")
                        ):
                            # Line starts with indent and previous line was empty
                            # -> Create new paragraph
                            self._sections[-1]["paragraphs"].append([])
                        # Append line to current paragraph
                        self._sections[-1]["paragraphs"][-1].append(line)
                    # New Chapter begins:
                    elif (
                        # ! This conditions is only applicable to RFC 3261 and might not be
                        # ! suiable for others.
                        # TODO: Parse this problematic situations separately
                        "Content-Length:" not in line   # Not an end of the SIP message
                        and "->" not in line            # Not a name for SIP message from figure
                        and "--" not in line            # Not an end of the table
                        and "=" not in line             # Not a SIP grammar description
                        and lines[i+1] == ""            # Next line is empty
                        and not line.startswith("(")    # Not an SDP not shown commend
                    ):
                        self._sections.append({
                            "name": line.strip(),
                            "paragraphs": []
                        })
                    # New Chapter with paragraph right away
                    elif match := re.match(r"^(([\d\.]+) ([\w\s]+))   (.*)", line, re.MULTILINE):
                        self._sections.append({
                            "name": match.group(1),
                            "paragraphs": [
                                [match.group(4)]
                            ]
                        })
                    else:
                        self._sections[-1]["paragraphs"].append([])
                        self._sections[-1]["paragraphs"][-1].append(line)
                        logger.warning(f"Unexpected line: {line}")
                    first_line = False  # <- first non empty line encountered on this page
                line_was_empty = line == ""

    @property
    def chapters(self) -> List[Chapter]:
        if not self._chapters:
            self._chapters = [
                Chapter(
                    title=sec["name"],
                    raw_sections=sec["paragraphs"]
                )
                for sec in self._sections
            ]
        return self._chapters
