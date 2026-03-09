# Pydantic 완전 가이드

Pydantic은 Python의 **타입 힌트를 런타임 검증으로 바꾸는 라이브러리**다. `BaseModel`을 상속하면 선언한 필드의 타입 검사, 변환, 직렬화가 자동으로 동작한다. FastAPI의 핵심 엔진이기도 하다. 이 글을 읽고 나면 Pydantic v2를 자유롭게 다루고, 실무에서 데이터 모델을 견고하게 설계할 수 있다.

---

## 1. BaseModel — 모든 것의 시작

Pydantic은 "클래스를 예쁘게 선언하는 도구"가 아니라, 타입 힌트를 실제 런타임 계약으로 바꾸는 계층이다. 아래 그림처럼 `입력 -> 검증/변환 -> 모델 인스턴스 -> 직렬화` 흐름으로 읽는 편이 빠르다.

![Pydantic BaseModel 사고방식](./images/pydantic-mental-model.svg)

- 타입 힌트와 `Field()` 선언은 문서가 아니라 실제 검증 규칙이 된다.
- 기본 모드는 "가능하면 변환하고, 불가능하면 거부한다"이다.
- 한 번 모델이 만들어지면 API 응답, 설정 객체, ORM 변환의 기준점이 된다.

```python
from pydantic import BaseModel

class User(BaseModel):
    id: int
    name: str
    email: str

# 올바른 데이터
user = User(id=1, name="Lee", email="lee@example.com")
print(user.name)         # "Lee"
print(user.model_dump()) # {'id': 1, 'name': 'Lee', 'email': 'lee@example.com'}

# 타입 변환 — "2"를 int로 자동 변환
user2 = User(id="2", name="Kim", email="kim@example.com")
print(user2.id)          # 2 (int)

# 잘못된 데이터 — ValidationError 발생
User(id="abc", name="", email="bad")
# ValidationError: 1 validation error for User
#   id - Input should be a valid integer
```

### 핵심 원리

Pydantic은 값을 **"가능하면 변환하고, 불가능하면 거부한다."** 이것이 `dataclass`와 결정적 차이다:

| 기능 | dataclass | Pydantic |
|------|-----------|----------|
| 타입 강제 변환 | ✗ | ✓ (`"1"` → `1`) |
| 런타임 검증 | ✗ | ✓ |
| 직렬화 (dict/JSON) | 직접 구현 | `.model_dump()` / `.model_dump_json()` |
| 역직렬화 | 직접 구현 | `.model_validate()` / `.model_validate_json()` |
| 중첩 모델 자동 파싱 | ✗ | ✓ |

---

## 2. Field — 제약 조건 선언

```python
from pydantic import BaseModel, Field

class Product(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    price: float = Field(gt=0, description="가격은 0보다 커야 한다")
    quantity: int = Field(ge=0, default=0)
    sku: str = Field(pattern=r"^[A-Z]{2}-\d{4}$")  # 정규식 패턴

product = Product(name="Widget", price=9.99, sku="AB-1234")
```

### 자주 쓰는 Field 옵션

| 옵션 | 의미 | 예시 |
|------|------|------|
| `min_length` / `max_length` | 문자열 길이 | `Field(min_length=1)` |
| `gt` / `ge` / `lt` / `le` | 숫자 범위 | `Field(ge=0, le=100)` |
| `pattern` | 정규식 매칭 | `Field(pattern=r"^\d{3}$")` |
| `default` | 기본값 | `Field(default=0)` |
| `default_factory` | 기본값 팩토리 | `Field(default_factory=list)` |
| `alias` | JSON 키 매핑 | `Field(alias="userName")` |
| `exclude` | 직렬화에서 제외 | `Field(exclude=True)` |
| `examples` | OpenAPI 예시 | `Field(examples=["foo"])` |

---

## 3. 타입 활용

### Optional / None 처리

```python
from typing import Optional

class UserUpdate(BaseModel):
    name: Optional[str] = None      # ✅ 선택 필드 — 기본값 None
    email: Optional[str]            # ⚠️ 필수 필드! None을 허용하지만 반드시 전달해야 함
```

> **흔한 실수**: `Optional[str]`은 "None을 허용하는 타입"일 뿐, "선택적 필드"가 아니다. 선택적으로 만들려면 반드시 `= None`을 붙여야 한다.

### Union / Literal

```python
from typing import Literal, Union

class Event(BaseModel):
    type: Literal["click", "view", "purchase"]
    payload: Union[ClickData, ViewData, PurchaseData]
```

### 리스트, 딕셔너리, 중첩 모델

```python
class Address(BaseModel):
    city: str
    zipcode: str

class Company(BaseModel):
    name: str
    tags: list[str] = []
    metadata: dict[str, str] = {}
    headquarters: Address                     # 중첩 모델
    branches: list[Address] = []              # 중첩 모델 리스트

# 중첩 모델은 dict로 전달해도 자동 파싱
company = Company(
    name="Acme",
    headquarters={"city": "Seoul", "zipcode": "06000"},
    branches=[{"city": "Busan", "zipcode": "48000"}],
)
```

---

## 4. Validator — 커스텀 검증

검증은 한 번에 뭉뚱그려 일어나는 것이 아니다. 입력 전처리, 타입/제약 검증, 모델 단위 검증, 에러 수집이 단계적으로 이어진다.

![Pydantic 검증 파이프라인](./images/pydantic-validation-pipeline.svg)

- `mode="before"`는 원시 입력을 정리할 때 쓴다.
- `field_validator`는 단일 필드의 정규화와 검증에 맞다.
- `model_validator(mode="after")`는 여러 필드의 관계를 본다.

### field_validator

```python
from pydantic import BaseModel, field_validator

class SignupRequest(BaseModel):
    username: str
    password: str
    password_confirm: str

    @field_validator("username")
    @classmethod
    def username_alphanumeric(cls, v: str) -> str:
        if not v.isalnum():
            raise ValueError("username must be alphanumeric")
        return v.lower()  # 정규화: 소문자로 변환

    @field_validator("password")
    @classmethod
    def password_strength(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("password must be at least 8 characters")
        if not any(c.isupper() for c in v):
            raise ValueError("password must contain an uppercase letter")
        return v
```

### model_validator — 필드 간 관계 검증

```python
from pydantic import model_validator

class DateRange(BaseModel):
    start: date
    end: date

    @model_validator(mode="after")
    def check_date_order(self) -> "DateRange":
        if self.start >= self.end:
            raise ValueError("end must be after start")
        return self
```

### mode="before" — 원시 데이터 전처리

```python
class FlexibleInput(BaseModel):
    tags: list[str]

    @field_validator("tags", mode="before")
    @classmethod
    def split_tags(cls, v):
        if isinstance(v, str):
            return [t.strip() for t in v.split(",")]
        return v

# 문자열로 전달해도 리스트로 변환
FlexibleInput(tags="python, fastapi, pydantic")
# tags=['python', 'fastapi', 'pydantic']
```

---

## 5. 직렬화와 역직렬화

### model_dump — 모델 → dict

```python
user = User(id=1, name="Lee", email="lee@example.com")

user.model_dump()                              # 전체
user.model_dump(include={"id", "name"})        # 특정 필드만
user.model_dump(exclude={"email"})             # 특정 필드 제외
user.model_dump(exclude_none=True)             # None인 필드 제외
user.model_dump(exclude_unset=True)            # 명시적으로 설정하지 않은 필드 제외
user.model_dump(by_alias=True)                 # alias 이름으로 출력
```

### model_dump_json — 모델 → JSON 문자열

```python
json_str = user.model_dump_json(indent=2)
```

### model_validate — dict → 모델

```python
data = {"id": 1, "name": "Lee", "email": "lee@example.com"}
user = User.model_validate(data)
```

### model_validate_json — JSON 문자열 → 모델

```python
json_str = '{"id": 1, "name": "Lee", "email": "lee@example.com"}'
user = User.model_validate_json(json_str)
```

### ORM에서 변환 — from_attributes

```python
class UserResponse(BaseModel):
    model_config = {"from_attributes": True}

    id: int
    name: str
    email: str

# SQLAlchemy 모델 인스턴스를 직접 변환
response = UserResponse.model_validate(db_user)
```

---

## 6. 모델 상속과 재사용

실무에서는 재사용보다 경계 분리가 더 중요하다. 아래 구조처럼 "공통 필드"는 공유하되, 입력 모델과 출력 모델은 역할별로 나누는 편이 안전하다.

![Pydantic 요청/응답 모델 분리](./images/pydantic-model-splitting.svg)

- `UserCreate`는 입력 전용이라 비밀번호 같은 민감 필드를 포함할 수 있다.
- `UserUpdate`는 부분 수정을 위해 optional 필드 중심으로 둔다.
- `UserResponse`는 출력 전용이라 `from_attributes`와 읽기용 필드에 집중한다.

### 공통 필드 추출

```python
class TimestampMixin(BaseModel):
    created_at: datetime
    updated_at: datetime

class UserResponse(TimestampMixin):
    id: int
    name: str
    email: str
```

### 요청/응답 모델 분리 패턴

```python
# ── Base: 공통 필드 ──
class UserBase(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: str

# ── Create: 입력용 (비밀번호 포함) ──
class UserCreate(UserBase):
    password: str = Field(min_length=8)

# ── Update: 부분 수정용 (모든 필드 optional) ──
class UserUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    email: Optional[str] = None

# ── Response: 출력용 (비밀번호 제외, 타임스탬프 포함) ──
class UserResponse(UserBase):
    model_config = {"from_attributes": True}
    id: int
    created_at: datetime
```

> **원칙**: 입력 모델과 출력 모델은 **절대** 같은 클래스로 쓰지 않는다. API 계약이 혼동되고, 민감한 필드가 노출된다.

---

## 7. model_config — 모델 설정

```python
class StrictUser(BaseModel):
    model_config = {
        "strict": True,           # 타입 변환 비활성화 ("1" → int 거부)
        "frozen": True,           # 불변 모델 (수정 불가)
        "from_attributes": True,  # ORM 모델 변환 허용
        "populate_by_name": True, # alias와 원래 이름 모두 허용
        "str_strip_whitespace": True,  # 문자열 앞뒤 공백 자동 제거
        "extra": "forbid",        # 정의되지 않은 필드 전달 시 에러
    }

    id: int
    name: str
```

| 옵션 | 기본값 | 용도 |
|------|--------|------|
| `strict` | `False` | `True`면 자동 변환 비활성화 |
| `frozen` | `False` | `True`면 불변 (hashable) |
| `from_attributes` | `False` | ORM 객체 → Pydantic 모델 |
| `extra` | `"ignore"` | `"forbid"` / `"allow"` |
| `str_strip_whitespace` | `False` | 문자열 자동 trim |
| `populate_by_name` | `False` | alias 외 원래 이름도 허용 |

---

## 8. Alias — JSON 키 매핑

```python
class ExternalEvent(BaseModel):
    model_config = {"populate_by_name": True}

    user_id: int = Field(alias="userId")
    event_type: str = Field(alias="eventType")
    created_at: datetime = Field(alias="createdAt")

# 카멜케이스 JSON → 스네이크케이스 Python
data = {"userId": 1, "eventType": "click", "createdAt": "2024-01-01T00:00:00"}
event = ExternalEvent.model_validate(data)
print(event.user_id)  # 1 (Python에서는 snake_case로 접근)

# 출력 시 다시 camelCase로
print(event.model_dump(by_alias=True))
# {'userId': 1, 'eventType': 'click', 'createdAt': ...}
```

---

## 9. Computed Field

```python
from pydantic import computed_field

class CartItem(BaseModel):
    name: str
    unit_price: float
    quantity: int

    @computed_field
    @property
    def total_price(self) -> float:
        return self.unit_price * self.quantity

item = CartItem(name="Widget", unit_price=10.0, quantity=3)
print(item.total_price)       # 30.0
print(item.model_dump())       # {'name': 'Widget', 'unit_price': 10.0, 'quantity': 3, 'total_price': 30.0}
```

---

## 10. Discriminated Union — 다형 모델

```python
from typing import Annotated, Literal, Union
from pydantic import BaseModel, Field

class TextBlock(BaseModel):
    type: Literal["text"]
    content: str

class ImageBlock(BaseModel):
    type: Literal["image"]
    url: str
    alt: str

class CodeBlock(BaseModel):
    type: Literal["code"]
    language: str
    source: str

Block = Annotated[
    Union[TextBlock, ImageBlock, CodeBlock],
    Field(discriminator="type"),
]

class Document(BaseModel):
    title: str
    blocks: list[Block]

# type 필드 값에 따라 자동으로 올바른 모델 선택
doc = Document.model_validate({
    "title": "My Doc",
    "blocks": [
        {"type": "text", "content": "Hello"},
        {"type": "code", "language": "python", "source": "print(1)"},
    ],
})
```

---

## 11. BaseSettings — 환경변수 관리

설정은 "문자열 환경변수 몇 개 읽기"가 아니라, 외부 입력을 타입 안전한 앱 설정으로 바꾸는 과정이다. 이 섹션은 아래 흐름으로 읽으면 된다.

![Pydantic BaseSettings 환경변수 흐름](./images/pydantic-settings-flow.svg)

- 기본값, `.env`, 실제 환경변수는 모두 `Settings` 클래스로 모인다.
- 환경변수가 더 높은 우선순위를 가져 override 역할을 한다.
- 한 곳에서 타입 검증을 끝내 두면 앱 나머지는 `settings.port` 같은 값만 믿고 쓸 수 있다.

```bash
pip install pydantic-settings
```

```python
from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": False,
    }

    database_url: str
    redis_url: str = "redis://localhost:6379"
    debug: bool = False
    port: int = Field(default=8000, ge=1, le=65535)
    allowed_origins: list[str] = ["http://localhost:3000"]

settings = Settings()  # .env 파일 + 환경변수에서 자동 로드
```

```env
# .env
DATABASE_URL=postgresql://user:pass@localhost:5432/mydb
REDIS_URL=redis://localhost:6379/1
DEBUG=true
```

### 중첩 환경변수

```python
class DBSettings(BaseModel):
    host: str = "localhost"
    port: int = 5432
    name: str = "mydb"

class Settings(BaseSettings):
    model_config = {"env_nested_delimiter": "__"}
    db: DBSettings = DBSettings()

# 환경변수: DB__HOST=prod-db DB__PORT=5433
```

---

## 12. 커스텀 타입

```python
from typing import Annotated
from pydantic import AfterValidator

def validate_phone(v: str) -> str:
    cleaned = v.replace("-", "").replace(" ", "")
    if not cleaned.isdigit() or len(cleaned) not in (10, 11):
        raise ValueError("invalid phone number")
    return cleaned

PhoneNumber = Annotated[str, AfterValidator(validate_phone)]

class Contact(BaseModel):
    name: str
    phone: PhoneNumber

# "010-1234-5678" → "01012345678"로 정규화
contact = Contact(name="Lee", phone="010-1234-5678")
print(contact.phone)  # "01012345678"
```

---

## 13. 에러 처리

```python
from pydantic import ValidationError

try:
    user = User(id="abc", name="", email="not-email")
except ValidationError as e:
    print(e.error_count())    # 에러 개수
    for err in e.errors():
        print(err)
        # {'type': 'int_parsing', 'loc': ('id',), 'msg': 'Input should be a valid integer', ...}

    # JSON 형태로 에러 반환 (API 응답에 유용)
    print(e.json())
```

### FastAPI에서 422 응답 커스터마이징

```python
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import ValidationError

app = FastAPI()

@app.exception_handler(ValidationError)
async def validation_error_handler(request: Request, exc: ValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "message": "Validation failed",
            "details": [
                {"field": ".".join(str(l) for l in e["loc"]), "message": e["msg"]}
                for e in exc.errors()
            ],
        },
    )
```

---

## 14. v1 → v2 마이그레이션

| v1 | v2 | 비고 |
|----|-----|------|
| `.dict()` | `.model_dump()` | |
| `.json()` | `.model_dump_json()` | |
| `.parse_obj(data)` | `.model_validate(data)` | |
| `.parse_raw(json_str)` | `.model_validate_json(json_str)` | |
| `class Config:` | `model_config = {...}` | dict 형태로 변경 |
| `@validator` | `@field_validator` | `@classmethod` 필수 |
| `@root_validator` | `@model_validator` | |
| `orm_mode = True` | `from_attributes = True` | |
| `schema_extra` | `json_schema_extra` | |

---

## 15. 자주 하는 실수

| 실수 | 원인과 해결 |
|------|-------------|
| `Optional[str]`만 쓰고 기본값 없음 | `Optional[str] = None`으로 써야 "선택적" 필드 |
| Pydantic 모델과 ORM 모델 혼용 | Pydantic은 API 계약, SQLAlchemy는 DB 매핑 — 분리 |
| v1 메서드를 v2에서 사용 | `.dict()` → `.model_dump()`, `.parse_obj()` → `.model_validate()` |
| `extra` 설정 누락 | `extra="forbid"`를 안 하면 오타 필드가 조용히 무시됨 |
| 입력/응답 모델 미분리 | `UserCreate`(입력), `UserResponse`(출력) 분리 필수 |
| `model_validator`에서 dict 반환 | `mode="after"`에서는 self(인스턴스)를 반환해야 함 |
| `frozen=True`에서 수정 시도 | frozen 모델은 `.model_copy(update={...})`로 새 인스턴스 생성 |

---

## 16. 빠른 참조

```python
from pydantic import BaseModel, Field, field_validator, model_validator, computed_field
from typing import Optional, Literal

# ── 모델 정의 ──
class Item(BaseModel):
    model_config = {"strict": False, "extra": "forbid", "from_attributes": True}
    name: str = Field(min_length=1, max_length=200)
    price: float = Field(gt=0)
    tags: list[str] = []

# ── 생성 / 변환 ──
item = Item(name="A", price=10.0)              # 직접 생성
item = Item.model_validate({"name": "A", "price": 10})  # dict → 모델
item = Item.model_validate_json('{"name":"A","price":10}')  # JSON → 모델

# ── 직렬화 ──
item.model_dump()                               # → dict
item.model_dump_json()                          # → JSON 문자열
item.model_dump(exclude_none=True)              # None 제외
item.model_dump(include={"name"})               # 특정 필드만

# ── 검증 ──
@field_validator("name") / @classmethod         # 단일 필드 검증
@model_validator(mode="after")                  # 필드 간 관계 검증

# ── 불변 모델 수정 ──
new_item = item.model_copy(update={"price": 20.0})

# ── JSON Schema ──
Item.model_json_schema()                        # OpenAPI 호환 스키마
```
