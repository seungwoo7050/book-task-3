from aws_security_primitives.engine import evaluate_policy


def test_allow_matches_when_action_and_resource_match() -> None:
    policy = {
        "Statement": {
            "Sid": "AllowRead",
            "Effect": "Allow",
            "Action": ["s3:GetObject"],
            "Resource": ["arn:aws:s3:::study2-logs/*"],
        }
    }
    request = {"Action": "s3:GetObject", "Resource": "arn:aws:s3:::study2-logs/app.log"}
    decision = evaluate_policy(policy, request)
    assert decision.allowed is True
    assert decision.reason == "at least one allow matched"


def test_explicit_deny_overrides_allow() -> None:
    policy = {
        "Statement": [
            {
                "Sid": "AllowRead",
                "Effect": "Allow",
                "Action": ["s3:GetObject"],
                "Resource": ["arn:aws:s3:::study2-logs/*"],
            },
            {
                "Sid": "DenySensitivePrefix",
                "Effect": "Deny",
                "Action": ["s3:GetObject"],
                "Resource": ["arn:aws:s3:::study2-logs/secret/*"],
            },
        ]
    }
    request = {"Action": "s3:GetObject", "Resource": "arn:aws:s3:::study2-logs/secret/key.txt"}
    decision = evaluate_policy(policy, request)
    assert decision.allowed is False
    assert decision.reason == "explicit deny matched"


def test_request_denied_when_no_allow_statement_matches() -> None:
    policy = {
        "Statement": {
            "Sid": "AllowRead",
            "Effect": "Allow",
            "Action": ["s3:GetObject"],
            "Resource": ["arn:aws:s3:::study2-logs/*"],
        }
    }
    request = {"Action": "s3:PutObject", "Resource": "arn:aws:s3:::study2-logs/app.log"}
    decision = evaluate_policy(policy, request)
    assert decision.allowed is False
    assert decision.reason == "no allow statement matched"

