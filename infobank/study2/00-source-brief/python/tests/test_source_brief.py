from stage00.source_brief import REFERENCE_SPINE, build_source_brief


def test_source_brief_contract():
    brief = build_source_brief()
    assert brief.topic == "챗봇 상담 품질 관리"
    assert brief.baseline_version == "08/v0-initial-demo"
    assert "FastAPI" in brief.primary_stack
    assert len(REFERENCE_SPINE) == 5
