# 04 지식 인덱스

## 핵심 용어
- **per-packet timer**: 패킷마다 timeout을 따로 추적하는 SR sender의 핵심 상태다.
- **receiver buffer**: 순서가 맞지 않아 아직 상위에 넘길 수 없는 패킷을 임시 저장하는 공간이다.
- **`recv_base`**: receiver가 다음으로 기대하는 가장 작은 시퀀스 번호다.
- **selective retransmission**: 실패한 패킷만 다시 보내는 SR의 핵심 동작이다.

## 다시 볼 파일
- [`../python/src/selective_repeat.py`](../python/src/selective_repeat.py): sender 타이머와 receiver 버퍼가 모두 들어 있는 핵심 구현 파일이다.
- [`../python/tests/test_selective_repeat.py`](../python/tests/test_selective_repeat.py): 기본 전달 보장과 fixture 가용성을 어떤 수준으로 보는지 보여준다.
- [`../docs/concepts/gbn-vs-sr.md`](../docs/concepts/gbn-vs-sr.md): GBN과 SR의 차이를 문장으로 다시 정리할 때 기준이 된다.
- [`../problem/code/selective_repeat_skeleton.py`](../problem/code/selective_repeat_skeleton.py): 제공된 인터페이스와 구현 책임 경계를 다시 확인할 때 본다.

## 자주 쓰는 확인 명령
- `make -C study/02-Reliable-Transport/selective-repeat/problem test`
- `cd study/02-Reliable-Transport/selective-repeat/python/tests && python3 -m pytest test_selective_repeat.py -v`

## 참고 자료
- [`../docs/references/README.md`](../docs/references/README.md): 공개 문서를 정리할 때 다시 확인한 근거 모음
