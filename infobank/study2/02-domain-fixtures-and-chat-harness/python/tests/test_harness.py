from pathlib import Path

from stage02.harness import run_replay, seed_knowledge_base


def test_seeded_kb_reproducible():
    kb = seed_knowledge_base(Path('data/knowledge_base'))
    assert set(kb) == {'cancellation_policy.md', 'identity_verification.md', 'refund_policy.md'}


def test_replay_harness_reproduces_expected_docs():
    result = run_replay(Path('data/replay_sessions.json'), Path('data/knowledge_base'))
    assert result['session_count'] == 2
    assert result['items'][0]['retrieved_doc_ids'][0] == 'refund_policy.md'
