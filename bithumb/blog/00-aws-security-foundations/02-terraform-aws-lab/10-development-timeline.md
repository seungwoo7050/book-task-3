# 02 Terraform AWS Lab: Terraform을 배포 도구보다 먼저 "보안 분석 입력"으로 고정한 단계

이 프로젝트는 Terraform을 얼마나 많이 아느냐를 보여 주는 lab이 아니다. `problem/README.md`가 요구하는 건 훨씬 좁다. insecure 설정과 secure 설정의 차이를 apply 없이도 반복해서 읽을 수 있게 만들고, 그 결과를 다음 프로젝트가 그대로 받아서 rule evaluation을 할 수 있는 입력으로 남기는 것이다. `2026-03-14`에 verify와 pytest를 다시 돌려 보니, 이 lab의 핵심은 Terraform 문법 자체보다 "같은 선언형 변경 의도"를 plan JSON으로 안정적으로 재생산하는 절차에 있었다.

## Step 1. insecure/secure 두 예제를 비교 가능한 한 쌍으로 먼저 고정했다

`terraform/insecure/main.tf`와 `terraform/secure/main.tf`는 리소스 수만 보면 둘 다 5개다. 하지만 실제 차이는 "어떤 위험한 의도"와 "어떤 통제된 의도"를 대표하느냐에 있다.

`2026-03-14`에 다시 확인한 source 신호는 이랬다.

- insecure `aws_s3_bucket_public_access_block`: 네 플래그가 모두 `false`
- secure `aws_s3_bucket_public_access_block`: 네 플래그가 모두 `true`
- insecure security group ingress: `0.0.0.0/0`
- secure security group ingress: `10.10.10.0/24`
- insecure IAM policy: `Action "*", Resource "*"`
- secure IAM policy: S3 read 범위만 허용

즉 이 lab은 "보안이 좋은 예제"와 "나쁜 예제"를 막연히 나란히 둔 것이 아니라, 이후 scanner가 읽을 핵심 차이를 plan에 확실히 남기는 fixture 쌍을 만든 셈이다. `docs/concepts/terraform-plan-reading.md`가 말하는 "CSPM 관점에서는 apply보다 plan JSON이 더 중요한 입력"이라는 문장이 여기서 실제 소스로 연결된다.

## Step 2. 그 fixture 쌍을 같은 검증 루프로 돌리게 만들었다

두 예제를 나란히 두기만 해서는 다음 프로젝트 입력이 되지 않는다. `verify.py`는 두 lab을 사람이 수동으로 열어 비교하지 않아도 되게, 같은 Terraform 절차를 코드로 묶는다.

```python
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

여기서 중요한 건 두 가지다.

- Terraform이 설치되지 않았으면 바로 실패해 입력 재현 가능성을 먼저 확인한다.
- dummy AWS credential을 환경 변수로 넣어, 실제 계정 없이도 `init -> validate -> plan -> show -json` 흐름을 돌린다.

`2026-03-14` 재실행 결과도 이 의도를 뒷받침했다.

```bash
PYTHONPATH=00-aws-security-foundations/02-terraform-aws-lab/python/src \
  .venv/bin/python -m terraform_aws_lab.verify
```

출력은 아래처럼 끝났다.

```text
insecure: 5 resources
secure: 5 resources
```

이 숫자 자체보다 중요한 건, 두 lab이 같은 코드 경로를 통과해 비교 가능한 산출물로 정리된다는 사실이다.

## Step 3. stdout이 아니라 `tfplan.json`을 남겨 다음 프로젝트 입력으로 만들었다

이 lab이 단순 Terraform 연습과 갈라지는 지점은 `terraform show -json` 결과를 파일로 고정한다는 점이다.

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
```

이 설계 때문에 다음 프로젝트는 Terraform CLI를 직접 다시 다루지 않고도 `planned_values.root_module.resources`를 바로 읽을 수 있다. `2026-03-14`에 plan JSON을 다시 확인했을 때도, insecure와 secure 모두 정확히 5개 resource를 담고 있었고, public access block 값과 policy scope 차이가 JSON 안에서 직접 드러났다.

즉 이 lab의 진짜 산출물은 `main.tf`만이 아니다. `tfplan.json`이 남아 있기 때문에 Terraform은 여기서부터 "배포 도구"가 아니라 "정적 보안 입력"이 된다.

## Step 4. 마지막으로 resource type 테스트로 입력 계약을 잠갔다

다음 CSPM rule engine이 안심하고 이 입력을 읽으려면, 단지 파일이 생성된다는 사실만으로는 부족하다. 어떤 자원 종류가 꼭 포함돼야 하는지도 테스트가 말해 줘야 한다. `test_terraform_lab.py`는 바로 그 역할을 맡는다.

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

`2026-03-14` 순차 재실행 결과 pytest는 `3 passed in 11.35s`였다. 여기서 "순차"라는 말이 중요하다. 처음에는 `verify`와 `pytest`를 병렬로 돌렸더니 insecure lab에서 `Error acquiring the state lock`이 났다. `run_lab()`가 lab 디렉터리 안의 고정 파일명 `tfplan`을 사용하기 때문에, 같은 경로를 동시에 plan 하려 하면 충돌하는 구조라는 뜻이다. 같은 명령을 순차로 다시 돌리자 pytest는 정상 통과했다. 이건 코드와 실제 재실행 결과를 함께 보고 내린 source-based inference다.

즉 이 lab은 재현 가능하지만, 병렬 안전한 캐시/출력 분리를 가진 verifier는 아니다. 오늘 검증에서 드러난 이 성질도 문서에 남겨 두는 편이 정확하다.

## 정리

`02-terraform-aws-lab`의 성취는 apply를 생략한 데 있지 않다. insecure/secure fixture 쌍을 같은 검증 루프로 돌리고, 그 차이를 `tfplan.json`으로 남기고, 어떤 resource type을 포함해야 하는지 테스트로 잠갔다는 데 있다. 그래서 다음 프로젝트는 Terraform 자체를 다시 설명하는 대신, 이 JSON을 바로 읽어 misconfiguration finding을 만드는 데 집중할 수 있다. 작은 lab이지만, 여기서부터 Terraform은 배포 도구가 아니라 scan input이 된다.
