def extract_claims(text: str) -> list[dict[str, str]]:
    sentences = [part.strip() for part in text.replace('?', '.').split('.') if part.strip()]
    return [{'claim_id': f'claim-{index}', 'statement': sentence} for index, sentence in enumerate(sentences, start=1)]


def verify_claims(claims: list[dict[str, str]], kb: dict[str, str]) -> dict[str, object]:
    claim_results = []
    for claim in claims:
        matched = [doc_id for doc_id, content in kb.items() if any(token in content for token in claim['statement'].split())]
        verdict = 'support' if matched else 'not_found'
        claim_results.append(
            {
                'claim_id': claim['claim_id'],
                'verdict': verdict,
                'evidence_doc_ids': matched[:2],
                'retrieval_trace': {'query': claim['statement'], 'docs': matched[:3]},
            }
        )
    return {'claim_results': claim_results}
