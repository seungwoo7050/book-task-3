# Problem Guide

이 문서는 01 RPC Framing 프로젝트에서 “무엇을 구현해야 하는가”를 현재 기준으로 다시 설명합니다. 과거 과제군에서 출발한 아이디어는 남기되, 현재 레포에 없는 로컬 경로를 전제로 설명하지는 않습니다.

## 문제 핵심

- 4-byte big-endian length prefix framing을 구현해야 합니다.
- split chunk와 multi-frame chunk를 모두 decode해야 합니다.
- pending call map 기반 동시 요청 처리가 필요합니다.
- unknown method, handler error, timeout, disconnect를 호출자에게 전파해야 합니다.

## 이번 범위에서 일부러 뺀 것

- TLS, 인증, streaming RPC는 포함하지 않습니다.
- 서비스 디스커버리나 로드 밸런싱은 다음 단계 범위입니다.

## 제공 자료

- 이 프로젝트는 별도 starter artifact 없이 `problem/README.md` 자체가 요구사항 문서 역할을 합니다.

## 역사적 출처와 현재 재구성

- 원래 속한 학습 주제: RPC Network
- 원래 구현 형태: JavaScript 기반 distributed-cluster 과제로, framing과 간단한 RPC 호출 흐름을 다루고 있었습니다.
- 현재 프로젝트에서의 재구성: Python 입문 트랙에서도 동일한 개념 범위를 유지하되, 이해하기 쉬운 단일 RPC 흐름에 집중합니다.
- 원본 소스 트리는 현재 레포에 포함돼 있지 않으며, 이 문서는 현재 공개 레포 기준으로 다시 정리한 설명입니다.
