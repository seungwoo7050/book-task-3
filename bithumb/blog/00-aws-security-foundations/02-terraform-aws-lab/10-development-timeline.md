# 02 Terraform AWS Lab: apply 없는 Terraform lab을 scan input으로 만들기

Terraform을 apply 도구가 아니라 이후 보안 스캐너가 읽을 선언형 입력으로 다루게 만드는 실습이다. 이 글은 결과만 요약하지 않고, 어떤 기준을 먼저 세우고 어떤 검증으로 다음 단계로 넘어갔는지를 차근차근 따라간다.

아래 phase를 순서대로 읽으면 "왜 Terraform lab의 핵심 산출물을 apply 결과가 아니라 plan JSON으로 봤는가"라는 질문에 답이 어떻게 만들어졌는지 자연스럽게 연결된다.

## 구현 순서 요약
먼저 전체 흐름을 짧게 잡아 두면, 각 phase가 왜 그 순서로 배치됐는지 훨씬 덜 버겁게 읽힌다.
1. insecure/secure Terraform 쌍을 유지하고, 같은 검증 스크립트가 두 lab을 모두 읽게 했다.
2. `init -> validate -> plan -> show -json` 흐름을 코드로 고정해 plan JSON 산출을 자동화했다.
3. 테스트가 insecure/secure lab 각각의 대표 resource type을 검증해, 후속 CSPM rule engine 입력을 안정화했다.

## Phase 1. insecure/secure lab을 같은 검증 흐름에 묶었다

여기서부터 흐름이 한 단계 또렷해진다. 먼저 `insecure/secure lab을 같은 검증 흐름에 묶었다`를 단단히 잡아야 뒤에서 나오는 테스트와 CLI가 왜 필요한지 설명할 수 있기 때문이다.

- 당시 목표: 두 Terraform 실습을 사람이 수동 비교하지 않고 같은 코드 경로로 돌릴 수 있게 만든다.
- 변경 단위: `python/src/terraform_aws_lab/verify.py`의 `AWS_ENV`, `terraform_available`, `run_lab` 진입부
- 처음 가설: 후속 프로젝트가 plan JSON을 입력으로 쓰려면, 먼저 lab 두 개가 같은 루틴으로 재현돼야 한다.
- 실제 진행: 스크립트는 Terraform CLI 유무를 먼저 확인하고, 로컬 더미 AWS 환경 변수를 주입한 뒤 각 lab 디렉터리에서 같은 명령을 반복하게 만들었다. 핵심은 실제 apply 없이도 같은 입력 구조를 계속 얻을 수 있게 하는 쪽이었다.

CLI:

```bash
$ PYTHONPATH=00-aws-security-foundations/02-terraform-aws-lab/python/src .venv/bin/python -m terraform_aws_lab.verify
```

검증 신호:
- 검증 스크립트 실행 결과가 `insecure: 5 resources`, `secure: 5 resources`로 떨어졌다.
- Terraform 1.5.7 환경에서 실제 명령 경로가 살아 있어 로컬에서 그대로 재현됐다.

핵심 코드:

```python
def run_lab(lab_dir: Path) -> dict[str, Any]:
    if not terraform_available():
        raise RuntimeError("terraform is not installed")

    env = os.environ.copy()
    env.update(AWS_ENV)

    subprocess.run(
        ["terraform", f"-chdir={lab_dir}", "init", "-backend=false"],
        check=True,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    subprocess.run(
        ["terraform", f"-chdir={lab_dir}", "validate"],
        check=True,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
```

왜 이 코드가 중요했는가: 이 부분이 없으면 insecure lab과 secure lab은 단지 두 개의 디렉터리일 뿐이다. 같은 절차로 돌려야만 두 상태를 비교 가능한 입력 쌍으로 다룰 수 있다.

새로 배운 것: CSPM 관점에서 Terraform의 핵심 산출물은 apply 결과보다 `planned_values.root_module.resources` 같은 plan 구조다. 분석은 선언형 변경 의도를 읽는 데서 시작한다.

다음: 이제 plan 결과를 파일로 남겨, 다른 프로젝트가 바로 읽을 수 있는 형태로 고정해야 했다.

## Phase 2. plan JSON을 산출물로 남겼다

여기서부터 흐름이 한 단계 또렷해진다. 먼저 `plan JSON을 산출물로 남겼다`를 단단히 잡아야 뒤에서 나오는 테스트와 CLI가 왜 필요한지 설명할 수 있기 때문이다.

- 당시 목표: `terraform show -json` 결과를 후속 스캐너가 읽을 실제 파일로 남긴다.
- 변경 단위: `python/src/terraform_aws_lab/verify.py`의 `plan -> show -json -> tfplan.json` 경로
- 처음 가설: stdout만 보고 끝내면 다음 단계에서 다시 Terraform CLI를 호출해야 한다. JSON 파일이 남아야 rule engine이 입력을 재사용할 수 있다.
- 실제 진행: `terraform plan`으로 binary plan을 만든 뒤 `terraform show -json`으로 렌더링해 `tfplan.json`으로 저장했다. 마지막에는 `planned_values.root_module.resources` 길이를 세어 lab별 resource count를 바로 확인하게 했다.

CLI:

```bash
$ PYTHONPATH=00-aws-security-foundations/02-terraform-aws-lab/python/src .venv/bin/python -m terraform_aws_lab.verify
```

검증 신호:
- 스크립트는 insecure/secure 모두 5개 resource를 읽었다.
- `tfplan.json`이 실제 파일로 남아서 05번 CSPM scanner가 fixture처럼 재사용할 수 있는 상태가 됐다.

핵심 코드:

```python
    plan_path = lab_dir / "tfplan"
    json_path = lab_dir / "tfplan.json"
    subprocess.run(
        ["terraform", f"-chdir={lab_dir}", "plan", "-refresh=false", f"-out={plan_path.name}"],
        check=True,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    rendered = subprocess.run(
        ["terraform", f"-chdir={lab_dir}", "show", "-json", plan_path.name],
        check=True,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    json_path.write_text(rendered.stdout)
    return json.loads(rendered.stdout)


def default_labs_root() -> Path:
    return Path(__file__).resolve().parents[3] / "terraform"


if __name__ == "__main__":
    root = default_labs_root()
    for lab_name in ("insecure", "secure"):
        plan = run_lab(root / lab_name)
        resource_count = len(plan["planned_values"]["root_module"]["resources"])
```

왜 이 코드가 중요했는가: 보안 분석 파이프라인에서 중요한 경계는 여기였다. Terraform CLI 실행이 끝난 자리에 JSON 산출물이 남아야 다음 단계가 느슨하게 연결된다.

새로 배운 것: “배포 전에 읽는 보안”은 실행 결과가 아니라 plan의 구조화된 표현을 다룬다. JSON으로 렌더링하는 순간부터 Terraform은 분석 입력이 된다.

다음: 이제 테스트로 insecure/secure lab이 각각 어떤 자원을 포함하는지 잠가 두어야 했다.

## Phase 3. resource type 테스트로 입력 계약을 고정했다

여기서부터 흐름이 한 단계 또렷해진다. 먼저 `resource type 테스트로 입력 계약을 고정했다`를 단단히 잡아야 뒤에서 나오는 테스트와 CLI가 왜 필요한지 설명할 수 있기 때문이다.

- 당시 목표: 다음 프로젝트가 기대하는 자원 종류가 실제 plan에 들어 있는지 테스트로 확인한다.
- 변경 단위: `python/tests/test_terraform_lab.py`의 insecure/secure 검증
- 처음 가설: plan JSON 파일이 만들어지기만 해서는 부족하다. insecure lab과 secure lab이 어떤 보안 차이를 대표하는지도 테스트가 말해줘야 한다.
- 실제 진행: 테스트는 insecure lab에서 `aws_s3_bucket`, `aws_security_group`가 보이는지 확인하고, secure lab에서는 `aws_s3_bucket_public_access_block`, `aws_iam_policy`가 있는지 확인했다. 이 검증이 있어야 05번 프로젝트가 S3 public access나 ingress 규칙을 안정적으로 읽을 수 있다.

CLI:

```bash
$ PYTHONPATH=00-aws-security-foundations/02-terraform-aws-lab/python/src .venv/bin/python -m pytest 00-aws-security-foundations/02-terraform-aws-lab/python/tests
```

검증 신호:
- 직렬 재검증 기준 pytest가 `3 passed in 17.61s`로 통과했다.
- insecure/secure가 서로 다른 resource type 집합을 대표한다는 계약이 테스트에 남았다.

핵심 코드:

```python
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
```

왜 이 코드가 중요했는가: plan 생성만으로는 후속 scanner가 뭘 기대해도 되는지 알 수 없다. 이 테스트가 “어떤 위험 시나리오를 담은 입력인가”를 문서 대신 코드로 못 박았다.

새로 배운 것: 보안용 fixture는 단순히 파일이 존재하는 것으로 충분하지 않다. 어떤 resource type을 담고 있어야 하는지까지 계약으로 고정해야 false positive가 줄어든다.

다음: 다음 프로젝트는 이 plan JSON을 직접 읽어 misconfiguration finding을 만든다.

## 여기서 남는 질문
이 문단은 단순한 회고가 아니라, 다음 프로젝트로 넘어갈 때 무엇을 들고 가야 하는지 짚어 두는 자리다.

Terraform lab의 핵심은 apply를 생략한 것이 아니라, plan JSON을 다음 프로젝트가 믿고 읽을 수 있는 입력으로 만든 데 있었다. 검증 스크립트와 resource-type 테스트가 있었기 때문에 05번 rule engine은 Terraform 자체보다 JSON 구조에 집중할 수 있었다.
