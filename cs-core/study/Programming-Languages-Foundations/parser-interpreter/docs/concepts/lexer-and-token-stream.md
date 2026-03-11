# Lexer와 Token Stream

이 프로젝트의 lexer는 "문법을 이해한다"기보다 "parser가 쓰기 좋은 입력 단위로 문자열을 자른다"는 역할에 집중합니다.

## 왜 token stream이 먼저 필요한가

- parser는 공백과 줄바꿈 자체보다 `LET`, `IDENTIFIER`, `TYPE_ARROW` 같은 안정된 기호를 다루는 편이 훨씬 단순합니다.
- `->`와 `=>`, `==`와 `=`처럼 문자 수가 다른 연산자를 lexer 단계에서 먼저 고정해 두면 parser가 lookahead를 덜 써도 됩니다.
- keyword와 identifier를 lexer에서 구분하면 parser가 "문맥상 이 이름이 예약어인지"를 다시 판단하지 않아도 됩니다.

## 현재 프로젝트에서 고정한 것

- keyword: `let`, `in`, `if`, `then`, `else`, `fun`, `true`, `false`, `not`, `and`, `or`, `Int`, `Bool`
- multi-character token: `->`, `=>`, `==`, `!=`, `<=`, `>=`
- single-character token: `(`, `)`, `,`, `:`, `=`, `+`, `-`, `*`, `/`, `<`, `>`

## line/column을 남기는 이유

- parser 오류를 "unexpected token"으로만 내보내면 학습자가 어디서 문법이 깨졌는지 바로 찾기 어렵습니다.
- 이 프로젝트는 syntax diagnostic을 `line:column: message` 한 줄로 고정해, 테스트와 CLI에서 같은 오류 표면을 쓰도록 했습니다.
