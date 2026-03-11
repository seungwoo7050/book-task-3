# 06-quorum-and-consistency — notion 폴더 가이드

이 폴더는 Quorum and Consistency 프로젝트의 이전 세대 장문 기록을 보관하는 자리입니다.

## 문서 구성

| 문서 | 내용 | 언제 읽으면 좋은가 |
|------|------|-------------------|
| [essay.md](essay.md) | quorum overlap, stale read, versioned register를 서사적으로 설명한 에세이 | consistency trade-off를 큰 그림으로 다시 읽고 싶을 때 |
| [timeline.md](timeline.md) | 프로젝트 개발의 전체 과정을 시간순으로 재현한 타임라인 | 같은 프로젝트를 처음부터 다시 구현하고 싶을 때 |

## 프로젝트 한 줄 요약

`N/W/R` 조합에 따라 최신 읽기와 stale read가 어떻게 갈리는지 versioned register로 재현합니다.

## 키워드

`quorum` · `consistency` · `stale-read` · `versioned-register` · `read-quorum` · `write-quorum`
