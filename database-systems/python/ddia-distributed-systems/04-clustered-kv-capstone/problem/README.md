# Problem Guide

이 문서는 04 Clustered KV Capstone 프로젝트에서 “무엇을 구현해야 하는가”를 현재 기준으로 다시 설명합니다. 과거 과제군에서 출발한 아이디어는 남기되, 현재 레포에 없는 로컬 경로를 전제로 설명하지는 않습니다.

## 문제 핵심

- key를 shard로 라우팅하고 shard별 leader/follower group을 선택해야 합니다.
- leader write가 log-backed 또는 disk-backed store에 기록돼야 합니다.
- follower가 watermark 이후 entry만 catch-up해야 합니다.
- node restart 뒤에도 disk에서 상태를 복원해야 합니다.
- leader read와 follower read가 모두 가능해야 합니다.

## 이번 범위에서 일부러 뺀 것

- dynamic membership, automatic failover, consensus 기반 leader election은 포함하지 않습니다.
- production deployment와 운영 자동화는 포트폴리오 확장 범위로 남깁니다.

## 제공 자료

- 이 프로젝트는 별도 starter artifact 없이 `problem/README.md` 자체가 요구사항 문서 역할을 합니다.

## 역사적 출처와 현재 재구성

- 원래 속한 학습 주제: Bridge project added by this repository
- 원래 구현 형태: 직접 대응하는 단일 과거 과제는 없고, routing·replication·storage 과제를 이어 붙이기 위해 현재 레포가 새로 만든 캡스톤입니다.
- 현재 프로젝트에서의 재구성: Python 트랙에서는 FastAPI를 외부 서비스 경계에만 사용하면서, 정적 topology 기반 분산 KV의 최소 흐름을 self-contained하게 보여 줍니다.
- 원본 소스 트리는 현재 레포에 포함돼 있지 않으며, 이 문서는 현재 공개 레포 기준으로 다시 정리한 설명입니다.
