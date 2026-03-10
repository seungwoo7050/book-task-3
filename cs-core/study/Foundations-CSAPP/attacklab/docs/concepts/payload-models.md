# Attack Lab payload 모델 지도

## 왜 모델로 다시 정리하는가

Attack Lab은 바이트 배열 하나가 어떤 제어 흐름을 만들 수 있는지를 묻습니다.
하지만 공개 저장소에서는 외부 타깃에 직접 재사용 가능한 해답 대신,
"어떤 구조를 만족해야 하는가"를 모델 형태로 정리하는 편이 안전하고도 교육적입니다.

## phase별 핵심 구조

| Phase | 공식 학습 포인트 | 저장소에서 모델로 고정한 것 |
|---|---|---|
| 1 | return address overwrite | 40바이트 frame fill 뒤 `touch1` 주소 |
| 2 | code injection으로 `touch2(cookie)` 호출 | shellcode 영역과 return-to-buffer 구조 |
| 3 | code injection으로 `touch3(cookie_string)` 호출 | shellcode와 문자열 배치의 동시 만족 |
| 4 | ROP로 `touch2(cookie)` 호출 | gadget 체인 순서와 인자 이동 |
| 5 | ROP로 `touch3(cookie_string)` 호출 | `%rsp` 기반 상대 주소 계산과 문자열 전달 |

## companion verifier가 보존하는 것

- little-endian 주소 인코딩
- frame 크기 계산
- cookie 처리 방식
- code injection과 ROP의 차이
- 마지막 phase의 상대 주소 계산

## companion verifier가 하지 않는 것

- 외부 타깃에서 실제 기계어를 실행하지 않는다
- 실제 `ctarget`/`rtarget` 통과를 대신 보장하지 않는다
- 비공개 타깃의 exploit recipe를 제공하지 않는다

## 이 문서를 어떻게 쓰면 좋은가

풀이를 기억하려 하지 말고,
"이 phase는 어떤 바이트 구조를 만족해야 하는가"를 기준으로 다시 읽는 것이 좋습니다.
