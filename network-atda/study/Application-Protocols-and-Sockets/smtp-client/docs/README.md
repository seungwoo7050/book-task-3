# 개념 문서 안내

    이 디렉터리는 `SMTP Client`를 공부하면서 반복해서 다시 볼 만한 개념 문서만 남겨 둔 곳입니다.

    ## 읽는 순서

    1. [`email-format.md`](concepts/email-format.md)
2. [`smtp-errors.md`](concepts/smtp-errors.md)
3. [`smtp.md`](concepts/smtp.md)
4. [`references/README.md`](references/README.md)

    ## 이 폴더가 답하려는 질문

    - 3자리 SMTP 응답 코드에 따른 제어 흐름
- `CRLF`와 `DATA` 종료 구분자 처리
- envelope 주소와 헤더 주소의 차이
- 예상하지 못한 응답 코드를 빠르게 중단시키는 fail-fast 구조

    ## 사용 원칙

    - 프로젝트 README와 중복되는 설명은 줄이고, 오래 남길 개념과 판단 근거를 우선합니다.
    - 이전 형식 노트는 `notion-archive/`에, 현재 읽을 작업 기록은 `notion/`에 둡니다.
    - 프로토콜 field 이름 같은 원문 용어는 필요할 때 그대로 유지합니다.
