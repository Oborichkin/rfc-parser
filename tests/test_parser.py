from RfcParser import RFC

def test_rfc3261(rfc3261):
    assert rfc3261.title == "SIP: Session Initiation Protocol"
    assert len(rfc3261.chapters) == 322


def test_rfc2327(rfc2327):
    assert rfc2327.title == "SDP: Session Description Protocol"
    assert len(rfc2327.chapters) == 26


def test_rfc_json_parser(rfc3261, rfc2327):
    assert rfc3261.json == RFC.from_json(rfc3261.json).json
    assert rfc2327.json == RFC.from_json(rfc2327.json).json
