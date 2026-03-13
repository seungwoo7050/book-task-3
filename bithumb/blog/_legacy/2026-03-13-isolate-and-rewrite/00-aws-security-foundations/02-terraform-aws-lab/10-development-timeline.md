# 10 Development Timeline

이 문서는 `Terraform AWS Lab`을 현재 Terraform fixture와 검증 스크립트만으로 다시 읽기 위해 chronology를 재구성한 기록입니다.

## Day 1
### Session 1

- 목표: 이 프로젝트가 Terraform 입문 자체가 아니라, 05번 규칙 엔진이 다시 읽을 입력을 준비하는 단계인지 확인한다.
- 진행: `problem/README.md`, `python/README.md`, `verify.py`, `terraform/insecure/main.tf`, `terraform/secure/main.tf`, `test_terraform_lab.py`를 같이 읽었다.
- 이슈: 처음엔 `terraform apply`까지 가야 실습이 완성된다고 생각했는데, 실제 제약은 의도적으로 `show -json`에서 멈춰 있었다.
- 판단: 이 프로젝트의 핵심은 리소스 배포가 아니라 `planned_values.root_module.resources`를 안정적인 분석 입력으로 고정하는 데 있다.

CLI:

```bash
$ sed -n '1,120p' 00-aws-security-foundations/02-terraform-aws-lab/problem/README.md
$ sed -n '1,220p' 00-aws-security-foundations/02-terraform-aws-lab/python/src/terraform_aws_lab/verify.py
$ sed -n '1,200p' 00-aws-security-foundations/02-terraform-aws-lab/python/tests/test_terraform_lab.py
$ find 00-aws-security-foundations/02-terraform-aws-lab/terraform -maxdepth 2 -type f | sort
```

이 시점의 핵심 코드는 실행 경로를 끊어서 plan JSON으로 고정하는 부분이었다.

```python
    subprocess.run(["terraform", f"-chdir={lab_dir}", "plan", "-refresh=false", f"-out={plan_path.name}"], ...)
    rendered = subprocess.run(
        ["terraform", f"-chdir={lab_dir}", "show", "-json", plan_path.name],
        ...
    )
    json_path.write_text(rendered.stdout)
```

처음엔 `validate`까지만 있어도 충분할 거라 생각했지만, 후속 프로젝트가 사람이 읽는 stdout이 아니라 JSON payload를 다시 파싱해야 하므로 `show -json`을 파일로 남기는 조각이 실제 중심이었다.

### Session 2

- 진행: 실제 검증 명령을 다시 돌려 insecure/secure 두 lab이 모두 재현되는지 확인했다.
- 검증: 실행 스크립트는 `insecure: 5 resources`, `secure: 5 resources`를 출력했고, pytest는 3개 테스트를 통과했다.
- 판단: 처음 가설은 insecure lab만 있으면 충분하다는 쪽이었지만, `test_secure_lab_generates_plan_json`이 있어야 05번에서 false positive를 줄이는 기준선을 확보할 수 있다.
- 다음: 이 프로젝트의 plan JSON은 05번에서 S3 public access, open ingress, encryption 규칙의 직접 입력이 된다.

CLI:

```bash
$ make venv
$ PYTHONPATH=00-aws-security-foundations/02-terraform-aws-lab/python/src .venv/bin/python -m terraform_aws_lab.verify
$ PYTHONPATH=00-aws-security-foundations/02-terraform-aws-lab/python/src .venv/bin/python -m pytest 00-aws-security-foundations/02-terraform-aws-lab/python/tests
```

출력:

```text
insecure: 5 resources
secure: 5 resources
3 passed in 55.50s
```
