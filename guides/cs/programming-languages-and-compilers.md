# 프로그래밍 언어와 컴파일러 완전 가이드

프로그래밍 언어 학습은 "문법을 안다"와 "실행 모델을 안다"를 함께 붙여 읽어야 훨씬 빨라진다. 이 문서는 lexer, parser, AST, type checker, bytecode/VM이 각각 어떤 질문에 답하는지를 구체적인 코드 예시와 함께 한 장으로 연결하는 가이드다. 이 문서를 읽고 나면 언어 구현의 각 단계가 왜 존재하는지, 단계 간 경계가 어디에 있는지를 설명할 수 있다.

아래 세 질문을 기준으로 읽으면 파이프라인이 훨씬 빨리 정리된다.

1. 이 단계는 **무엇을 입력으로 받고 무엇을 출력하는가?**
2. 이 단계가 **없다면 어떤 문제가 생기는가?**
3. **에러는 이 단계에서 잡는가, 다음 단계에서 잡는가?**

---

## 1. 전체 파이프라인

```
source code (문자열)
    ↓ lexer
token stream
    ↓ parser
AST (Abstract Syntax Tree)
    ↓ static checker / type checker
타입 주석이 붙은 AST (annotated AST)
    ↓ code generator / lowering
bytecode / IR instructions
    ↓ VM / interpreter
실행 결과
```

각 단계는 독립적인 책임을 가진다. 단계 경계를 명확히 유지할수록 각 단계를 따로 테스트하고 교체하기 쉬워진다.

---

## 2. Lexer — 문자를 token으로 자르기

lexer는 소스 코드 문자열을 의미 있는 단위(token)로 분리한다. 이 단계를 거쳐야 parser가 구조를 볼 수 있다.

```python
from enum import Enum, auto
from dataclasses import dataclass

class TokenKind(Enum):
    NUMBER = auto()
    PLUS = auto(); MINUS = auto(); STAR = auto(); SLASH = auto()
    LPAREN = auto(); RPAREN = auto()
    LET = auto(); IN = auto(); FUN = auto(); IF = auto(); ELSE = auto()
    IDENT = auto()
    ARROW = auto()   # =>
    EQ = auto()      # =
    EOF = auto()

@dataclass
class Token:
    kind: TokenKind
    value: str       # 원본 문자열 (NUMBER면 "42", IDENT면 "x")

def tokenize(src: str) -> list[Token]:
    tokens = []
    i = 0
    while i < len(src):
        if src[i].isspace():
            i += 1
            continue
        if src[i].isdigit():
            j = i
            while j < len(src) and src[j].isdigit():
                j += 1
            tokens.append(Token(TokenKind.NUMBER, src[i:j]))
            i = j
            continue
        if src[i].isalpha() or src[i] == '_':
            j = i
            while j < len(src) and (src[j].isalnum() or src[j] == '_'):
                j += 1
            word = src[i:j]
            kind = {
                "let": TokenKind.LET, "in": TokenKind.IN,
                "fun": TokenKind.FUN, "if": TokenKind.IF, "else": TokenKind.ELSE,
            }.get(word, TokenKind.IDENT)
            tokens.append(Token(kind, word))
            i = j
            continue
        # 단일 문자 token 처리
        ch_map = {'+': TokenKind.PLUS, '-': TokenKind.MINUS,
                  '*': TokenKind.STAR, '/': TokenKind.SLASH,
                  '(': TokenKind.LPAREN, ')': TokenKind.RPAREN,
                  '=': TokenKind.EQ}
        if src[i] in ch_map:
            tokens.append(Token(ch_map[src[i]], src[i]))
            i += 1
            continue
        raise SyntaxError(f"unexpected character: {src[i]!r}")
    tokens.append(Token(TokenKind.EOF, ""))
    return tokens

# tokenize("let x = 1 + 2 in x")
# → [LET, IDENT('x'), EQ, NUMBER('1'), PLUS, NUMBER('2'), IN, IDENT('x'), EOF]
```

---

## 3. Parser — token stream을 AST로 바꾸기

parser는 token 열에서 **의미 단위(AST node)**를 만든다. `1 + 2 * 3`이 `(1 + (2 * 3))`인지 `((1 + 2) * 3)`인지는 parser가 결정한다.

### AST 노드 정의

```python
from dataclasses import dataclass
from typing import Union

# 표현식 AST 노드
@dataclass
class Num:
    value: int

@dataclass
class BinOp:
    op: str                  # '+' | '-' | '*' | '/'
    left: "Expr"
    right: "Expr"

@dataclass
class Var:
    name: str

@dataclass
class Let:
    name: str
    value: "Expr"
    body: "Expr"

@dataclass
class Fun:
    param: str
    body: "Expr"

@dataclass
class App:                   # 함수 적용: f(arg)
    func: "Expr"
    arg: "Expr"

@dataclass
class If:
    cond: "Expr"
    then: "Expr"
    else_: "Expr"

Expr = Union[Num, BinOp, Var, Let, Fun, App, If]
```

### Recursive Descent + Precedence Climbing

```python
class Parser:
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.pos = 0

    def peek(self) -> Token:
        return self.tokens[self.pos]

    def consume(self, kind: TokenKind | None = None) -> Token:
        tok = self.tokens[self.pos]
        if kind and tok.kind != kind:
            raise SyntaxError(f"expected {kind}, got {tok.kind}")
        self.pos += 1
        return tok

    def parse_expr(self) -> Expr:
        # special form: let, fun, if
        if self.peek().kind == TokenKind.LET:
            return self.parse_let()
        if self.peek().kind == TokenKind.FUN:
            return self.parse_fun()
        if self.peek().kind == TokenKind.IF:
            return self.parse_if()
        # binary operator: precedence climbing
        return self.parse_add()

    def parse_add(self) -> Expr:
        left = self.parse_mul()
        while self.peek().kind in (TokenKind.PLUS, TokenKind.MINUS):
            op = self.consume().value
            right = self.parse_mul()
            left = BinOp(op, left, right)
        return left

    def parse_mul(self) -> Expr:
        left = self.parse_atom()
        while self.peek().kind in (TokenKind.STAR, TokenKind.SLASH):
            op = self.consume().value
            right = self.parse_atom()
            left = BinOp(op, left, right)
        return left

    def parse_atom(self) -> Expr:
        tok = self.peek()
        if tok.kind == TokenKind.NUMBER:
            self.consume()
            return Num(int(tok.value))
        if tok.kind == TokenKind.IDENT:
            self.consume()
            return Var(tok.value)
        if tok.kind == TokenKind.LPAREN:
            self.consume()
            expr = self.parse_expr()
            self.consume(TokenKind.RPAREN)
            return expr
        raise SyntaxError(f"unexpected token: {tok}")

    def parse_let(self) -> Expr:
        self.consume(TokenKind.LET)
        name = self.consume(TokenKind.IDENT).value
        self.consume(TokenKind.EQ)
        value = self.parse_expr()
        self.consume(TokenKind.IN)
        body = self.parse_expr()
        return Let(name, value, body)

    def parse_fun(self) -> Expr:
        self.consume(TokenKind.FUN)
        param = self.consume(TokenKind.IDENT).value
        self.consume(TokenKind.ARROW)
        body = self.parse_expr()
        return Fun(param, body)

# parse("1 + 2 * 3")
# → BinOp('+', Num(1), BinOp('*', Num(2), Num(3)))
# 즉 곱셈이 먼저 묶임 — parse_mul이 parse_add보다 아래 호출되기 때문
```

---

## 4. Tree-walk Evaluator — AST를 직접 실행하기

AST를 재귀적으로 걸으며 값을 계산한다. 가장 직관적인 실행 방식이다.

### Environment와 Lexical Scope

```python
from typing import Any, Callable

# 값 타입
Value = int | bool | Callable   # closure도 값

class Environment:
    """lexical scope을 체인으로 구현"""
    def __init__(self, parent: "Environment | None" = None):
        self._bindings: dict[str, Value] = {}
        self._parent = parent

    def lookup(self, name: str) -> Value:
        if name in self._bindings:
            return self._bindings[name]
        if self._parent:
            return self._parent.lookup(name)
        raise NameError(f"unbound variable: {name}")

    def extend(self, name: str, value: Value) -> "Environment":
        """새 binding을 추가한 자식 environment 반환"""
        child = Environment(parent=self)
        child._bindings[name] = value
        return child
```

```python
def evaluate(expr: Expr, env: Environment) -> Value:
    match expr:
        case Num(value):
            return value

        case BinOp(op, left, right):
            lv, rv = evaluate(left, env), evaluate(right, env)
            match op:
                case '+': return lv + rv
                case '-': return lv - rv
                case '*': return lv * rv
                case '/':
                    if rv == 0:
                        raise ZeroDivisionError("division by zero")
                    return lv // rv

        case Var(name):
            return env.lookup(name)          # lexical lookup

        case Let(name, value, body):
            val = evaluate(value, env)
            new_env = env.extend(name, val)
            return evaluate(body, new_env)

        case Fun(param, body):
            # closure: body + definition 시점의 env 캡처
            def closure(arg: Value) -> Value:
                return evaluate(body, env.extend(param, arg))
            return closure

        case App(func, arg):
            fn = evaluate(func, env)
            av = evaluate(arg, env)
            return fn(av)                    # closure 호출

# 예시: let x = 10 in let f = fun y => x + y in f 5
# → 15  (x는 call 시점이 아니라 definition 시점의 env에서 해석)
```

**lexical scope**: closure는 정의된 위치의 environment를 캡처한다. `x`가 call 시점에 다른 값으로 바뀌어 있어도 closure 안의 `x`는 definition 시점 값을 유지한다.

---

## 5. Static Type Checker — 실행 전에 오류 잡기

type checker는 AST를 한 번 더 순회하며 "실행하면 반드시 오류가 날 것"을 미리 찾는다. 실행 없이 발견하는 것이 핵심이다.

### 타입 정의와 Type Environment

```python
from dataclasses import dataclass
from typing import Union

@dataclass(frozen=True)
class TInt: pass           # 정수 타입

@dataclass(frozen=True)
class TBool: pass          # 불리언 타입

@dataclass(frozen=True)
class TFun:
    param: "Type"          # 파라미터 타입
    ret: "Type"            # 반환 타입

Type = TInt | TBool | TFun

class TypeError(Exception): pass

def infer(expr: Expr, tenv: dict[str, Type]) -> Type:
    """AST를 읽어 타입을 추론 (또는 검증), 오류면 TypeError"""
    match expr:
        case Num(_):
            return TInt()

        case BinOp(op, left, right):
            lt, rt = infer(left, tenv), infer(right, tenv)
            if not isinstance(lt, TInt) or not isinstance(rt, TInt):
                raise TypeError(f"operator '{op}' requires Int operands")
            return TInt()

        case Var(name):
            if name not in tenv:
                raise TypeError(f"unbound variable: {name}")
            return tenv[name]

        case Let(name, value, body):
            val_type = infer(value, tenv)
            new_tenv = {**tenv, name: val_type}
            return infer(body, new_tenv)

        case Fun(param, body):
            # 간단한 모노타입: param 타입을 외부에서 받거나 추론
            # 여기서는 annotation으로 받는 버전 생략, 학습용 단순 버전
            raise NotImplementedError("type annotation required for Fun")

        case If(cond, then, else_):
            ct = infer(cond, tenv)
            if not isinstance(ct, TBool):
                raise TypeError("if condition must be Bool")
            tt = infer(then, tenv)
            et = infer(else_, tenv)
            if type(tt) != type(et):
                raise TypeError(f"if branches have different types: {tt} vs {et}")
            return tt

# infer(BinOp('+', Num(1), Num(2)), {})       → TInt()    ✓
# infer(BinOp('+', Num(1), Var('x')), {})     → TypeError: unbound variable  ✗
# infer(If(Num(1), Num(2), Num(3)), {})        → TypeError: if condition must be Bool ✗
```

### Static vs Runtime 오류 경계

```
static checker가 잡는 것:
  ✓ if 조건이 Bool이 아닌 경우
  ✓ + 에 Int가 아닌 값
  ✓ 함수 호출 arity 불일치
  ✓ unbound variable (type environment 기준)

runtime이 잡는 것:
  ✗ division by zero  (값에 따라 달라지므로 static 분석 어려움)
  ✗ 외부 입력 기반 오류
  ✗ 무한 루프 (halting problem)

경계를 명확히 하는 이유:
  static 단계에서 잡을 수 있는 오류를 runtime에 두면
  사용자는 실행 중 오류를 만날 때까지 발견하지 못한다.
```

---

## 6. Bytecode VM — AST를 instruction으로 낮추기

bytecode VM은 AST를 더 단순한 instruction sequence로 변환(lowering)하고, 그 sequence를 stack 기반으로 실행한다. tree-walk interpreter와 동일한 프로그램을 다른 실행 모델로 보여 준다.

### Instruction Set 정의

```python
from enum import Enum, auto
from dataclasses import dataclass, field

class OpCode(Enum):
    PUSH_INT = auto()   # 스택에 정수 push
    ADD = auto()        # 스택 상위 두 값 pop, 합 push
    SUB = auto()
    MUL = auto()
    DIV = auto()
    LOAD = auto()       # 변수 이름으로 environment에서 값 load
    STORE = auto()      # 변수 이름으로 environment에 값 store
    CALL = auto()       # 함수 호출 (스택 top이 arg, 그 아래가 fn)
    RETURN = auto()     # 현재 frame에서 반환
    JUMP_IF_FALSE = auto()  # 조건 false면 offset만큼 jump
    JUMP = auto()       # 무조건 jump

@dataclass
class Instruction:
    opcode: OpCode
    arg: int | str | None = None

@dataclass
class Bytecode:
    instructions: list[Instruction] = field(default_factory=list)

    def emit(self, opcode: OpCode, arg=None):
        self.instructions.append(Instruction(opcode, arg))
```

### Compiler: AST → Bytecode

```python
def compile_expr(expr: Expr, code: Bytecode):
    match expr:
        case Num(value):
            code.emit(OpCode.PUSH_INT, value)

        case BinOp(op, left, right):
            compile_expr(left, code)   # left 결과 → 스택
            compile_expr(right, code)  # right 결과 → 스택
            match op:
                case '+': code.emit(OpCode.ADD)
                case '-': code.emit(OpCode.SUB)
                case '*': code.emit(OpCode.MUL)
                case '/': code.emit(OpCode.DIV)

        case Var(name):
            code.emit(OpCode.LOAD, name)

        case Let(name, value, body):
            compile_expr(value, code)
            code.emit(OpCode.STORE, name)
            compile_expr(body, code)

        case If(cond, then, else_):
            compile_expr(cond, code)
            jump_if_false = len(code.instructions)
            code.emit(OpCode.JUMP_IF_FALSE, None)   # placeholder
            compile_expr(then, code)
            jump_over = len(code.instructions)
            code.emit(OpCode.JUMP, None)             # placeholder
            # patch jump_if_false target
            code.instructions[jump_if_false].arg = len(code.instructions)
            compile_expr(else_, code)
            # patch jump_over target
            code.instructions[jump_over].arg = len(code.instructions)

# BinOp('+', Num(1), BinOp('*', Num(2), Num(3))) 컴파일 결과:
# PUSH_INT 1
# PUSH_INT 2
# PUSH_INT 3
# MUL
# ADD
# → 스택 기반 후위 표기법(RPN)으로 변환된 것과 동일
```

### Stack-based VM 실행

```python
def run(code: Bytecode, env: dict) -> int | bool:
    stack: list = []
    pc = 0

    while pc < len(code.instructions):
        instr = code.instructions[pc]
        pc += 1

        match instr.opcode:
            case OpCode.PUSH_INT:
                stack.append(instr.arg)
            case OpCode.ADD:
                b, a = stack.pop(), stack.pop()
                stack.append(a + b)
            case OpCode.SUB:
                b, a = stack.pop(), stack.pop()
                stack.append(a - b)
            case OpCode.MUL:
                b, a = stack.pop(), stack.pop()
                stack.append(a * b)
            case OpCode.DIV:
                b, a = stack.pop(), stack.pop()
                if b == 0: raise ZeroDivisionError
                stack.append(a // b)
            case OpCode.LOAD:
                stack.append(env[instr.arg])
            case OpCode.STORE:
                env[instr.arg] = stack.pop()
            case OpCode.JUMP_IF_FALSE:
                if not stack.pop():
                    pc = instr.arg
            case OpCode.JUMP:
                pc = instr.arg

    return stack[-1] if stack else None
```

### Tree-walk vs Bytecode VM 비교

| 구분 | Tree-walk Interpreter | Bytecode VM |
|------|----------------------|-------------|
| 구현 복잡도 | 낮음 (재귀 순회) | 높음 (compiler + VM 두 단계) |
| 실행 추적 | AST 구조와 1:1 대응 | instruction 단위로 분리됨 |
| 최적화 가능성 | 제한적 | instruction 레벨 최적화 쉬움 |
| 첫 학습 적합성 | 매우 적합 | parser-interpreter 이후 단계 |

---

## 7. 이 워크스페이스에서의 읽는 순서

```
parser-interpreter  → lexer + recursive descent parser + tree-walk evaluator
                       "문법을 정의하고 의미를 부여한다"

static-type-checking → 같은 문법 + type environment + infer/check pass
                        "실행 전에 잡을 수 있는 오류는 미리 잡는다"

bytecode-ir          → 같은 AST + instruction lowering + stack-based VM
                        "실행 모델을 바꾸면 같은 의미가 다르게 표현된다"
```

이 순서로 읽으면 "문법을 만든다 → 의미를 제한한다 → 실행 모델을 교체한다"는 흐름이 한 번에 잡힌다.

연결 프로젝트:
- [`parser-interpreter`](../../cs-core/study/Programming-Languages-Foundations/parser-interpreter/README.md)
- [`static-type-checking`](../../cs-core/study/Programming-Languages-Foundations/static-type-checking/README.md)
- [`bytecode-ir`](../../cs-core/study/Programming-Languages-Foundations/bytecode-ir/README.md)

---

## 빠른 참조

| 단계 | 입력 | 출력 | 주요 오류 |
|------|------|------|----------|
| Lexer | source string | token list | unexpected character |
| Parser | token list | AST | syntax error, unexpected token |
| Type Checker | AST + type env | annotated AST / Type | type mismatch, unbound variable |
| Evaluator | AST + env | Value | runtime error (division by zero 등) |
| Compiler | AST | Bytecode | (컴파일 타임에는 type checker가 주로 담당) |
| VM | Bytecode + env | Value | stack underflow, jump out of bounds |

```
핵심 설계 결정:
  1. precedence 결정 → parse_mul이 parse_add 아래에서 호출되는 구조
  2. lexical scope    → closure가 definition 시점 env를 캡처
  3. static/runtime 경계 → type checker pass에서 잡을 수 있는 것은 여기서 모두 처리
  4. tree-walk vs VM → 같은 AST, 다른 실행 모델
```
