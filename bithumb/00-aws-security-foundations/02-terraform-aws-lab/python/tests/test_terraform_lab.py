from pathlib import Path

import pytest

from terraform_aws_lab.verify import run_lab, terraform_available


pytestmark = pytest.mark.skipif(not terraform_available(), reason="terraform is not installed")


def _project_root() -> Path:
    return Path(__file__).resolve().parents[2]


def test_insecure_lab_generates_plan_json() -> None:
    plan = run_lab(_project_root() / "terraform" / "insecure")
    resource_types = {resource["type"] for resource in plan["planned_values"]["root_module"]["resources"]}
    assert "aws_s3_bucket" in resource_types
    assert "aws_security_group" in resource_types


def test_secure_lab_generates_plan_json() -> None:
    plan = run_lab(_project_root() / "terraform" / "secure")
    resource_types = {resource["type"] for resource in plan["planned_values"]["root_module"]["resources"]}
    assert "aws_s3_bucket_public_access_block" in resource_types
    assert "aws_iam_policy" in resource_types

