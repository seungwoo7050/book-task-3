# 디버그 로그

## 1. hex 입력과 utf-8 입력을 같은 필드로 받으면 의미가 흐려진다

처음부터 raw bytes만 받으면 학습자가 각 vector가 무엇을 의미하는지 읽기 어려워집니다. 반대로 문자열만 받으면 RFC
벡터처럼 hex 기반 입력을 재현하기 어렵습니다. 그래서 manifest마다 `encoding`을 명시해 둘 다 지원하도록 고정했습니다.

## 2. HKDF는 단순 hash 체인이 아니라 HMAC 기반 extract/expand다

digest만 여러 번 돌리는 방식으로 구현하면 RFC 5869 벡터를 맞출 수 없습니다. `salt -> PRK -> OKM` 두 단계가 드러나야
key expansion KDF라는 의미도 함께 설명됩니다.

