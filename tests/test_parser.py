from RfcParser import RFC


def test_rfc2119(rfc2119):
    rfc = RFC(rfc2119)
    assert rfc.title == "Key words for use in RFCs to Indicate Requirement Levels"
    assert len(rfc.chapters) == 11
    assert rfc.chapters[0].title == "Status of this Memo"
    assert len(rfc.chapters[0]) == 1
    assert rfc.chapters[1].title == "Abstract"
    assert len(rfc.chapters[1]) == 3
    assert rfc.chapters[2].title == "1. MUST"
    assert len(rfc.chapters[2]) == 1
    assert rfc.chapters[3].title == "2. MUST NOT"
    assert len(rfc.chapters[3]) == 1
    assert rfc.chapters[4].title == "3. SHOULD"
    assert len(rfc.chapters[4]) == 1
    assert rfc.chapters[5].title == "4. SHOULD NOT"
    assert len(rfc.chapters[5]) == 1
    assert rfc.chapters[6].title == "5. MAY"
    assert len(rfc.chapters[6]) == 1
    assert rfc.chapters[7].title == "6. Guidance in the use of these Imperatives"
    assert len(rfc.chapters[7]) == 1
    assert rfc.chapters[8].title == "7. Security Considerations"
    assert len(rfc.chapters[8]) == 1
    assert rfc.chapters[9].title == "8. Acknowledgments"
    assert len(rfc.chapters[9]) == 1
    assert rfc.chapters[10].title == "9. Author's Address"
    assert len(rfc.chapters[10]) == 3


def test_rfc3261(rfc3261):
    rfc = RFC(rfc3261)
    assert rfc.title == "SIP: Session Initiation Protocol"
    assert len(rfc.chapters) == 322


def test_rfc2327(rfc2327):
    rfc = RFC(rfc2327)
    assert rfc.title == "SDP: Session Description Protocol"
    assert len(rfc.chapters) == 26
