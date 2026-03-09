# SQLAlchemy 완전 가이드

SQLAlchemy는 Python의 사실상 표준 ORM이다. 두 가지 층으로 나뉜다: **Core**(SQL 표현식 빌더)와 **ORM**(모델 매핑). FastAPI·Flask·Django 외 프레임워크에서 DB에 접근하는 코드는 대부분 SQLAlchemy 위에서 동작한다. 이 글을 읽고 나면 모델 설계, 세션 관리, 쿼리 작성, Alembic 마이그레이션까지 실무에서 SQLAlchemy를 자유롭게 다룰 수 있다. (2.0 스타일 기준)

---

## 1. SQLAlchemy의 사고방식

SQLAlchemy는 API 목록보다 세 가지 경계를 먼저 잡는 편이 훨씬 이해가 빠르다. Engine은 연결 풀을, Session은 작업 단위를, loading 전략은 쿼리 수를 결정한다.

![SQLAlchemy를 읽는 기준](./images/sqlalchemy-mental-model.svg)

이 그림은 이 문서 전체를 읽는 기준표다. 먼저 아래 세 질문으로 읽으면 된다.

1. **Resource boundary:** Engine, `sessionmaker`, Session은 각각 무엇을 담당하는가?
2. **Loading boundary:** 연관 데이터를 언제 lazy, `joinedload`, `selectinload`로 읽어야 하는가?
3. **I/O boundary:** sync Session과 AsyncSession은 어디서 분리해야 하는가?

뒤 섹션들은 이 세 질문을 순서대로 구체화한다. 엔진과 세션은 "자원을 어떻게 관리하는가", 모델과 loading 전략은 "객체와 쿼리를 어떻게 연결하는가", async와 Alembic은 "어떤 실행 환경에서 어떤 흐름을 쓸 것인가"를 설명한다.

---

## 2. 설치와 초기 설정

SQLAlchemy에서 가장 자주 엉키는 부분은 Engine과 Session을 같은 것으로 보는 것이다. Engine은 애플리케이션 전역 자원이고, Session은 요청이나 작업 단위마다 새로 열고 닫는 컨텍스트다.

![Session 생성부터 종료까지의 흐름](./images/sqlalchemy-session-lifecycle.svg)

그림 기준으로 먼저 보면 된다.

- Engine은 연결 풀을 들고 있는 장기 자원이다.
- Session은 요청, 커맨드, 배치 작업처럼 짧은 단위로 열고 닫는다.
- `commit()`이나 `rollback()` 뒤에는 `close()`로 세션을 정리해 연결을 풀에 돌려준다.

```bash
pip install sqlalchemy psycopg2-binary   # PostgreSQL
# 또는
pip install sqlalchemy[asyncio] asyncpg   # 비동기
```

### 엔진과 세션

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# 엔진 — DB 연결 풀
engine = create_engine(
    "postgresql://user:pass@localhost:5432/mydb",
    pool_size=5,
    max_overflow=10,
    echo=False,         # True면 실행되는 SQL을 로그로 출력
)

# 세션 팩토리
SessionLocal = sessionmaker(bind=engine)

# Base 클래스
class Base(DeclarativeBase):
    pass
```

### FastAPI 세션 주입

```python
from typing import Generator
from sqlalchemy.orm import Session

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 사용
from fastapi import Depends

@router.get("/users/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.execute(select(User).where(User.id == user_id)).scalar_one_or_none()
    if not user:
        raise HTTPException(404, "User not found")
    return user
```

---

## 3. 모델 정의 — Mapped 스타일 (2.0)

```python
from datetime import datetime
from sqlalchemy import String, Text, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(100))
    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now()
    )

    # 관계 — 1:N
    posts: Mapped[list["Post"]] = relationship(back_populates="author", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<User(id={self.id}, email={self.email})>"


class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(300))
    content: Mapped[str | None] = mapped_column(Text, nullable=True)
    published: Mapped[bool] = mapped_column(default=False)
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    # 관계 — N:1
    author: Mapped["User"] = relationship(back_populates="posts")
    # 관계 — N:M
    tags: Mapped[list["Tag"]] = relationship(secondary="posts_tags", back_populates="posts")
```

### 다대다 관계

```python
from sqlalchemy import Table, Column, Integer, ForeignKey

# Association Table — 클래스 대신 Table 사용
posts_tags = Table(
    "posts_tags",
    Base.metadata,
    Column("post_id", Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True),
    Column("tag_id", Integer, ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True),
)

class Tag(Base):
    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True)

    posts: Mapped[list["Post"]] = relationship(secondary=posts_tags, back_populates="tags")
```

### Nullable vs Optional

```python
# 필수 필드 (NOT NULL)
name: Mapped[str] = mapped_column(String(100))

# 선택 필드 (NULL 허용)
bio: Mapped[str | None] = mapped_column(Text, nullable=True)
# 또는
bio: Mapped[Optional[str]] = mapped_column(Text)
```

---

## 4. Select — 조회 (2.0 스타일)

```python
from sqlalchemy import select, and_, or_, func, desc

# 전체 조회
stmt = select(User)
users = db.execute(stmt).scalars().all()

# 조건 조회
stmt = select(User).where(
    and_(User.is_active == True, User.name.like("%Lee%"))
)
users = db.execute(stmt).scalars().all()

# 단건 조회
stmt = select(User).where(User.id == 1)
user = db.execute(stmt).scalar_one_or_none()   # 없으면 None
user = db.execute(stmt).scalar_one()            # 없으면 NoResultFound

# 특정 컬럼만
stmt = select(User.id, User.email).where(User.is_active == True)
rows = db.execute(stmt).all()  # [(1, "a@..."), (2, "b@...")]

# 정렬 + 페이지네이션
stmt = (
    select(User)
    .order_by(desc(User.created_at))
    .limit(20)
    .offset(0)
)

# 집계
stmt = select(func.count(User.id)).where(User.is_active == True)
total = db.execute(stmt).scalar()
```

### JOIN

```python
# INNER JOIN
stmt = (
    select(Post.title, User.name)
    .join(User, Post.author_id == User.id)
    .where(Post.published == True)
)

# LEFT OUTER JOIN
stmt = (
    select(User.name, func.count(Post.id).label("post_count"))
    .outerjoin(Post, User.id == Post.author_id)
    .group_by(User.name)
)
```

---

## 5. Eager Loading — N+1 문제 해결

Eager loading은 "성능 최적화 옵션"이 아니라, 관계 데이터를 몇 번의 쿼리로 어떤 형태로 가져올지를 결정하는 전략이다.

![loading 전략 선택 기준](./images/sqlalchemy-loading-decision.svg)

그림 기준으로 선택하면 된다.

- 1:1이나 작은 N을 한 번에 붙여 읽을 때는 `joinedload`.
- 1:N에서 행 폭발을 피하고 싶으면 `selectinload`.
- 기본 lazy loading은 의도적으로 허용한 경우가 아니면 N+1 원인으로 먼저 의심한다.

```python
from sqlalchemy.orm import joinedload, selectinload, subqueryload

# ❌ Lazy Loading — N+1 쿼리 발생
users = db.execute(select(User)).scalars().all()
for user in users:
    print(user.posts)   # 유저마다 추가 쿼리 발생!

# ✅ joinedload — JOIN으로 한 번에 가져옴
stmt = select(User).options(joinedload(User.posts))
users = db.execute(stmt).unique().scalars().all()

# ✅ selectinload — SELECT ... WHERE id IN (...) 로 가져옴
stmt = select(User).options(selectinload(User.posts))
users = db.execute(stmt).scalars().all()
```

| 전략 | SQL | 적합 상황 |
|------|-----|----------|
| `joinedload` | LEFT JOIN | 1:1, 적은 N |
| `selectinload` | SELECT IN | 1:N (많은 데이터) |
| `subqueryload` | 서브쿼리 | N:M |

---

## 6. Insert / Update / Delete

```python
# Create
new_user = User(email="lee@example.com", name="Lee")
db.add(new_user)
db.commit()
db.refresh(new_user)   # id 등 DB 생성 값 반영
print(new_user.id)

# Bulk Insert
db.add_all([
    User(email="a@example.com", name="A"),
    User(email="b@example.com", name="B"),
])
db.commit()

# Update
user = db.execute(select(User).where(User.id == 1)).scalar_one()
user.name = "Updated Name"
db.commit()

# Bulk Update (ORM 없이)
from sqlalchemy import update
stmt = (
    update(User)
    .where(User.is_active == False)
    .values(name="Deactivated")
)
db.execute(stmt)
db.commit()

# Delete
db.delete(user)
db.commit()

# Bulk Delete
from sqlalchemy import delete
stmt = delete(User).where(User.is_active == False)
db.execute(stmt)
db.commit()
```

---

## 7. 트랜잭션

### 기본 패턴

```python
# sessionmaker의 commit / rollback
try:
    user = User(email="lee@example.com", name="Lee")
    db.add(user)

    post = Post(title="First", author_id=user.id)
    db.add(post)

    db.commit()
except Exception:
    db.rollback()
    raise
```

### begin 블록 (자동 commit/rollback)

```python
with SessionLocal.begin() as session:
    session.add(User(email="lee@example.com", name="Lee"))
    # 블록이 끝나면 자동 commit, 예외 발생 시 rollback
```

### 중첩 트랜잭션 (Savepoint)

```python
with db.begin_nested() as savepoint:
    db.add(User(email="temp@example.com", name="Temp"))
    # savepoint 내에서 예외 발생 시 이 블록만 롤백
```

---

## 8. Async — 비동기

비동기 모드에서는 엔진, 세션, 쿼리 호출 방식이 함께 바뀐다. sync 코드에 `await`만 붙이는 식으로는 전환되지 않는다.

![sync와 async SQLAlchemy 경계](./images/sqlalchemy-async-sync-flow.svg)

그림 기준으로 기억하면 된다.

- sync 스택은 `create_engine` + `Session` + 일반 함수 호출 조합이다.
- async 스택은 `create_async_engine` + `AsyncSession` + `await db.execute(...)` 조합이다.
- 같은 요청 흐름 안에서 sync Session과 AsyncSession을 섞지 않는 편이 안전하다.

```python
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

async_engine = create_async_engine("postgresql+asyncpg://user:pass@localhost/mydb")
AsyncSessionLocal = async_sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)

# FastAPI 비동기 세션 주입
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

# 비동기 쿼리
@router.get("/users/{user_id}")
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    stmt = select(User).where(User.id == user_id)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(404)
    return user
```

### 비동기에서 Eager Loading

```python
# selectinload은 비동기에서 안전
stmt = select(User).options(selectinload(User.posts))
result = await db.execute(stmt)
users = result.scalars().all()

# ⚠️ joinedload → unique() 필요
stmt = select(User).options(joinedload(User.posts))
result = await db.execute(stmt)
users = result.unique().scalars().all()
```

---

## 9. Alembic — 마이그레이션

### 초기화

```bash
pip install alembic
alembic init alembic
```

### alembic/env.py 설정

```python
from app.database import Base, engine

target_metadata = Base.metadata

def run_migrations_online():
    connectable = engine
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()
```

### 워크플로우

```bash
# 1. 모델 변경 후 마이그레이션 생성
alembic revision --autogenerate -m "add bio to users"

# 2. 생성된 파일 확인
cat alembic/versions/abc123_add_bio_to_users.py

# 3. 적용
alembic upgrade head

# 4. 롤백
alembic downgrade -1

# 기타
alembic current            # 현재 버전
alembic history            # 전체 이력
alembic upgrade +1         # 한 단계만 적용
```

### 생성된 마이그레이션 파일

```python
def upgrade() -> None:
    op.add_column("users", sa.Column("bio", sa.Text(), nullable=True))

def downgrade() -> None:
    op.drop_column("users", "bio")
```

---

## 10. 1.x → 2.0 마이그레이션

| 1.x 스타일 | 2.0 스타일 |
|-----------|-----------|
| `Column(Integer)` | `Mapped[int] = mapped_column()` |
| `session.query(User).filter()` | `session.execute(select(User).where())` |
| `session.query(User).get(1)` | `session.get(User, 1)` |
| `session.query(User).all()` | `session.execute(select(User)).scalars().all()` |
| `session.query(User).first()` | `session.execute(select(User)).scalar_one_or_none()` |
| `session.query(func.count)` | `session.execute(select(func.count(User.id))).scalar()` |

---

## 11. 실전 패턴

### Repository 패턴

```python
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models import User

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def find_by_id(self, user_id: int) -> User | None:
        return self.db.execute(
            select(User).where(User.id == user_id)
        ).scalar_one_or_none()

    def find_by_email(self, email: str) -> User | None:
        return self.db.execute(
            select(User).where(User.email == email)
        ).scalar_one_or_none()

    def create(self, **kwargs) -> User:
        user = User(**kwargs)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def update(self, user: User, **kwargs) -> User:
        for key, value in kwargs.items():
            setattr(user, key, value)
        self.db.commit()
        self.db.refresh(user)
        return user

    def delete(self, user: User) -> None:
        self.db.delete(user)
        self.db.commit()
```

### Mixin — 공통 컬럼

```python
from datetime import datetime
from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column

class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())

class SoftDeleteMixin:
    deleted_at: Mapped[datetime | None] = mapped_column(default=None)

class User(TimestampMixin, SoftDeleteMixin, Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True)
```

---

## 12. 자주 하는 실수

| 실수 | 원인과 해결 |
|------|-------------|
| Session 미종료 → connection leak | `try/finally`로 닫거나 `Depends(get_db)`로 자동 관리 |
| ORM 객체를 API 응답에 직접 반환 | Pydantic 모델로 변환 후 반환. lazy loading 에러 방지 |
| 1.x `session.query()` 혼용 | 새 코드는 2.0 `select()` 스타일로 통일 |
| N+1 쿼리 | `joinedload()`, `selectinload()` 사용 |
| migration 없이 모델만 수정 | `alembic revision --autogenerate` 후 `alembic upgrade head` |
| `commit()` 없이 데이터 저장 기대 | `add()` 후 반드시 `commit()` 호출 |
| `refresh()` 누락으로 DB 생성 값 없음 | `commit()` 후 `refresh(obj)`로 DB 기본값(id 등) 반영 |
| 비동기에서 lazy loading | async에서는 반드시 eager loading 사용 |

---

## 13. 빠른 참조

```python
# ── 모델 ──
class T(Base):
    __tablename__ = "t"
    id: Mapped[int] = mapped_column(primary_key=True)
    col: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    fk: Mapped[int] = mapped_column(ForeignKey("other.id"))
    rel: Mapped["Other"] = relationship(back_populates="ts")

# ── 조회 ──
select(T).where(T.col == val)
select(T).where(and_(a, b))
select(T).order_by(desc(T.col)).limit(20).offset(0)
select(func.count(T.id))
select(T).options(selectinload(T.rel))

# ── 결과 ──
db.execute(stmt).scalars().all()       # 리스트
db.execute(stmt).scalar_one_or_none()  # 단건 또는 None
db.execute(stmt).scalar_one()          # 단건 (없으면 에러)
db.execute(stmt).scalar()              # 단일 값

# ── CUD ──
db.add(obj)       → db.commit() → db.refresh(obj)
db.delete(obj)    → db.commit()
update(T).where().values()  → db.execute() → db.commit()

# ── 트랜잭션 ──
with SessionLocal.begin() as session: ...

# ── Alembic ──
alembic revision --autogenerate -m "msg"
alembic upgrade head
alembic downgrade -1
```
