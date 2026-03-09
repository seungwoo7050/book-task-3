# 05-clustered-kv-capstone — notion 폴더 가이드

이 폴더는 Clustered KV Capstone 프로젝트의 학습 과정과 설계 사고를 기록한 문서 모음입니다.

## 문서 구성

| 문서 | 내용 | 언제 읽으면 좋은가 |
|------|------|-------------------|
| [essay.md](essay.md) | 샤드 라우팅, 디스크 저장소, 리더-팔로워 복제를 하나의 흐름으로 통합하는 과정의 에세이 | 분산 KV 스토어의 전체 아키텍처를 조감하고 싶을 때 |
| [timeline.md](timeline.md) | 프로젝트 개발의 전체 과정을 시간순으로 재현한 타임라인 | 동일한 프로젝트를 처음부터 따라 구현하고 싶을 때 |

## 프로젝트 한 줄 요약

정적 샤드 토폴로지에서 consistent hash ring 라우팅, JSON append-only log 기반 디스크 저장소, leader-follower watermark 복제를 하나의 Cluster로 통합하는 캡스톤 프로젝트.

## 키워드

`capstone` · `clustered-kv` · `shard-routing` · `disk-backed-store` · `leader-follower` · `watermark` · `catch-up` · `restart-recovery` · `static-topology`
