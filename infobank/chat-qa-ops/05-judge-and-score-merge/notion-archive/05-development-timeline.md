# Judge & Score Merge — 개발 타임라인

## 1단계: 디렉터리 생성

```bash
mkdir -p chat-qa-ops/05-judge-and-score-merge/python/{src/stage05,tests}
```

## 2단계: pyproject.toml 작성

```bash
cat > chat-qa-ops/05-judge-and-score-merge/python/pyproject.toml << 'EOF'
[project]
name = "stage05-judge-and-score-merge"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = []

[tool.pytest.ini_options]
testpaths = ["tests"]
EOF
```

stage 01의 rubric 모듈을 import해야 하지만, 이 stage에서는 WEIGHTS를 직접 복사하는 방식을 택했다.
cross-stage dependency를 pyproject.toml에 넣지 않은 이유는 각 stage가 독립 실행 가능해야 하기 때문이다.

## 3단계: judge_response() 구현

```bash
touch chat-qa-ops/05-judge-and-score-merge/python/src/stage05/__init__.py
# judge.py 작성 시작
```

구현 순서:
1. `judge_response(response_text, failure_types)` — correctness부터 작성
2. correctness: `max(0, 90 - len(failure_types) * 10)` — failure가 많을수록 감점
3. resolution: 응답 길이 > 10이면 85, 아니면 40
4. communication: "감사", "안내" 등 상담 키워드 포함 여부로 80/50 분기

이 시점에서 한번 테스트를 돌려 judge_response()가 dict를 정상 반환하는지 확인했다:

```bash
cd chat-qa-ops/05-judge-and-score-merge/python
uv run pytest tests/ -x -v
```

## 4단계: merge_score() 구현

```bash
# judge.py에 merge_score() 추가
```

stage 01 rubric.py의 WEIGHTS를 그대로 가져와서 가중 평균을 계산한다.
empathy와 efficiency는 judge_response()에서 생산하지 않으므로, merge_score()의 입력 dict에 기본값(예: 70.0)을 넣는 방식으로 처리했다.

```python
# 기본값 패턴
scores.setdefault("empathy", 70.0)
scores.setdefault("efficiency", 70.0)
```

## 5단계: 테스트 추가

```bash
touch chat-qa-ops/05-judge-and-score-merge/python/tests/test_judge.py
```

테스트 케이스:
1. failure 없을 때 correctness == 90
2. failure 5개 이상일 때 correctness == max(0, ...)으로 0 이하 방지
3. merge_score()가 0~100 범위 float 반환

```bash
cd chat-qa-ops/05-judge-and-score-merge/python
uv run pytest tests/ -x -v
```

## 6단계: critical override 검증

stage 01의 critical override 로직이 merge 결과에 제대로 적용되는지 확인하기 위해,
correctness=0인 케이스를 추가했다.

```bash
# test_judge.py에 critical override 테스트 추가
uv run pytest tests/test_judge.py::test_critical_override -v
```

## 7단계: README 및 문서 정리

```bash
cat > chat-qa-ops/05-judge-and-score-merge/python/README.md << 'EOF'
# Stage 05 — Judge & Score Merge
...
EOF
```

## 비고

- 이 stage에서 외부 패키지 설치는 없다. 순수 Python 표준 라이브러리만 사용한다.
- LLM provider SDK(openai, anthropic 등)는 capstone v1에서 추가된다.
