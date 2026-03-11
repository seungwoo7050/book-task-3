# 디버그 로그

## 1. artifact 파일명을 고정하지 않으면 demo 비교가 어렵다

artifact writer는 JSON 파일 6개와 markdown report 1개를 항상 같은 이름으로 생성해야 한다. 이름이 흔들리면 README와
demo walkthrough, CLI test가 동시에 깨지고, "무엇이 생성돼야 하는가"를 설명하기 어려워진다.

## 2. remediation board는 priority만 같아도 충분하지 않았다

priority만 맞으면 얼핏 통과처럼 보이지만, 같은 `P1` 안에서 crypto/auth/backend/dependency 순서가 흔들리면 review 회의에서
읽는 방식이 매번 달라진다. 그래서 category 정렬 규칙까지 고정했다.

## 3. `make demo-capstone`은 이전 실행 결과를 지워야 했다

CLI 자체는 `--output-dir`을 덮어쓸 수 있지만, 루트 demo 명령은 "이번 실행에서 정확히 무엇이 생성됐는가"를 보여 줘야 한다.
그래서 `.artifacts/capstone/demo/`를 먼저 비우고 다시 만들도록 잡았다.
