import re
import logging

from typing import List

from .chapter import Chapter

logger = logging.getLogger(__name__)


class RFC:

    PAGE_SEPARATOR = "\u000c"

    def __init__(self, text: str):
        self._raw = text
        self.title = None
        self._chapters = []

        self.pages: List[str] = None

        self._parse_rfc(text)

    def _parse_metadata(self, text):
        for match in re.finditer(r"\n\n^ +", text, re.MULTILINE):
            # TODO: parse metadata before skipping it
            return text[match.end():]
        raise Exception("Function _parse_metadata have not found the beggining of the RFC")

    def _parse_rfc(self, text):
        text = self._parse_metadata(text)
        self.pages = text.split(self.PAGE_SEPARATOR)

        first_page = True
        line_was_empty = True

        for page in self.pages:
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
                            first_line and self._chapters[-1]["paragraphs"][-1][-1].endswith(".")
                        ):
                            # Line starts with indent and previous line was empty
                            # -> Create new paragraph
                            self._chapters[-1]["paragraphs"].append([])
                        # Append line to current paragraph
                        self._chapters[-1]["paragraphs"][-1].append(line)
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
                        self._chapters.append({
                            "name": line.strip(),
                            "paragraphs": []
                        })
                    # New Chapter with paragraph right away
                    elif match := re.match(r"^(([\d\.]+) ([\w\s]+))   (.*)", line, re.MULTILINE):
                        self._chapters.append({
                            "name": match.group(1),
                            "paragraphs": [
                                [match.group(4)]
                            ]
                        })
                    else:
                        self._chapters[-1]["paragraphs"].append([])
                        self._chapters[-1]["paragraphs"][-1].append(line)
                        logger.warning(f"Unexpected line: {line}")
                    first_line = False  # <- first non empty line encountered on this page
                line_was_empty = line == ""

    @property
    def chapters(self) -> List[Chapter]:
        return [
            Chapter(title=ch["name"], paragraphs=ch["paragraphs"])
            for ch in self._chapters
        ]
