# Python Implementation

- Scope: Kubernetes manifest와 Docker metadata를 읽고 guardrail finding을 생성한다.
- Build: `PYTHONPATH=src python -m container_guardrails.cli <manifest.yaml> <image.json>`
- Test: `PYTHONPATH=src python -m pytest tests`
- Status: `verified`
- Known gaps: PodSecurity admission 전체를 재현하지는 않는다.

