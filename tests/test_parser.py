from RfcParser.parser import RFC


def test_rfc2119(rfc2119):
    rfc = RFC(rfc2119)
    assert rfc.title == "Key words for use in RFCs to Indicate Requirement Levels"
    assert len(rfc._chapters) == 11


def test_rfc3261(rfc3261):
    rfc = RFC(rfc3261)
    assert rfc.title == "SIP: Session Initiation Protocol"
    assert len(rfc._chapters) == 322


def test_rfc2327(rfc2327):
    rfc = RFC(rfc2327)
    assert rfc.title == "SDP: Session Description Protocol"
    assert len(rfc._chapters) == 26