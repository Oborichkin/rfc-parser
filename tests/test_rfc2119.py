def test_rfc2119_titles(rfc2119):
    assert rfc2119.title == "Key words for use in RFCs to Indicate Requirement Levels"
    assert len(rfc2119.chapters) == 11

    assert rfc2119.chapters[0].title == "Status of this Memo"
    assert len(rfc2119.chapters[0]) == 1
    assert rfc2119.chapters[0].sections[0].text == \
        "This document specifies an Internet Best Current Practices for the " \
        "Internet Community, and requests discussion and suggestions for " \
        "improvements.  Distribution of this memo is unlimited."

    assert rfc2119.chapters[1].title == "Abstract"
    assert len(rfc2119.chapters[1]) == 3
    assert rfc2119.chapters[1].sections[0].text == \
        "In many standards track documents several words are used to signify " \
        "the requirements in the specification.  These words are often " \
        "capitalized.  This document defines these words as they should be " \
        "interpreted in IETF documents.  Authors who follow these guidelines " \
        "should incorporate this phrase near the beginning of their document:"
    assert rfc2119.chapters[1].sections[1].text == \
        'The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL ' \
        'NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED",  "MAY", and ' \
        '"OPTIONAL" in this document are to be interpreted as described in ' \
        'RFC 2119.'
    assert rfc2119.chapters[1].sections[2].text == \
        "Note that the force of these words is modified by the requirement "\
        "level of the document in which they are used."

    assert rfc2119.chapters[2].title == "1. MUST"
    assert len(rfc2119.chapters[2]) == 1

    assert rfc2119.chapters[3].title == "2. MUST NOT"
    assert len(rfc2119.chapters[3]) == 1

    assert rfc2119.chapters[4].title == "3. SHOULD"
    assert len(rfc2119.chapters[4]) == 1

    assert rfc2119.chapters[5].title == "4. SHOULD NOT"
    assert len(rfc2119.chapters[5]) == 1

    assert rfc2119.chapters[6].title == "5. MAY"
    assert len(rfc2119.chapters[6]) == 1

    assert rfc2119.chapters[7].title == "6. Guidance in the use of these Imperatives"
    assert len(rfc2119.chapters[7]) == 1

    assert rfc2119.chapters[8].title == "7. Security Considerations"
    assert len(rfc2119.chapters[8]) == 1

    assert rfc2119.chapters[9].title == "8. Acknowledgments"
    assert len(rfc2119.chapters[9]) == 1

    assert rfc2119.chapters[10].title == "9. Author's Address"
    assert len(rfc2119.chapters[10]) == 3
