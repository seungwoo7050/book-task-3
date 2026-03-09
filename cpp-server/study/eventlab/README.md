# eventlab

커널 이벤트 큐와 non-blocking socket의 수명주기를 따로 떼어 보는 lab이다.

## Focus

- listening socket 열기
- accept/read/write 이벤트 처리
- EOF와 disconnect 정리
- idle client keep-alive ping

## Open

- 문제 설명: [problem/README.md](problem/README.md)
- 구현: [cpp/README.md](cpp/README.md)
- 개념 노트: [docs/README.md](docs/README.md)
