# hash vs MAC vs KDF

## 1. Hash

hash는 입력을 고정 길이 digest로 압축합니다. 입력이 공개 정보여도 쓸 수 있고, 같은 입력이면 항상 같은 출력이 나옵니다.
그래서 파일 fingerprint나 캐시 key처럼 “같은 데이터를 다시 알아보는” 용도에는 좋지만, 비밀을 증명하는 도구는 아닙니다.

## 2. MAC

MAC(Message Authentication Code)는 secret key와 message를 함께 넣어 출력값을 만듭니다. 같은 message라도 key가 바뀌면
출력이 달라집니다. 그래서 “이 메시지를 key를 아는 쪽이 만들었는가”를 검증할 수 있습니다. plain hash가 인증을 대신하지
못하는 이유가 바로 여기에 있습니다. hash에는 비밀이 없기 때문입니다.

## 3. KDF

KDF(Key Derivation Function)는 입력 secret에서 새 key material을 뽑아냅니다. 같은 KDF라도 목적이 다르면 설계 질문이
달라집니다.

- password KDF: 사람 비밀번호처럼 entropy가 낮은 입력을 brute-force 비용이 큰 형태로 바꿉니다.
- key expansion KDF: 이미 secret인 key material에서 context별 하위 키를 분리합니다.

이 프로젝트에서 PBKDF2-HMAC-SHA1은 전자에, HKDF-SHA256은 후자에 해당합니다.

## 4. 왜 plain hash로 인증하면 안 되는가

`sha256(message)`는 누구나 계산할 수 있습니다. 공격자도 같은 입력을 넣으면 같은 출력이 나옵니다. 그래서 메시지 무결성을
검사하는 척할 수는 있어도, “authorized sender가 만들었다”는 뜻은 되지 않습니다. 이때 필요한 것이 HMAC 같은 keyed MAC입니다.

