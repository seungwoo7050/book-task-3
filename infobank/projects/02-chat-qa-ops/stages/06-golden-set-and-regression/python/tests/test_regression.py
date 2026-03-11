from pathlib import Path

from stage06.regression import evaluate_case, load_manifest


def test_golden_assertion_and_compare_manifest():
    assert evaluate_case(['refund_policy.md'], ['refund_policy.md'])['passed'] is True
    manifest = load_manifest(Path('data/compare_manifest.json'))
    assert manifest['baseline'] == 'v1.0'
    assert manifest['candidate'] == 'v1.1'
