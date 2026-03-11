# 01 Approach Log

## 설계 선택

- 문법은 expression-only 코어로 제한하고, `let`, `if`, `fun`, call만 남겼습니다.
- parser는 recursive descent + precedence climbing 조합으로 나눴습니다. special form과 infix operator를 다른 층으로 두기 위해서입니다.
- evaluator는 tree-walk 방식으로 유지하고, function value는 정의 시점 environment를 같이 들고 있는 closure로 모델링했습니다.
- type annotation은 parser가 읽고 AST에 남기되, evaluator는 사용하지 않았습니다. 다음 프로젝트에서 static/runtime 경계를 비교하기 위해서입니다.
