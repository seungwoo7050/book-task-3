# Quorum Read/Write

quorum의 핵심은 “모든 replica가 최신이어야 한다”가 아니라, read quorum과 write quorum이 반드시 한 번은 겹치게 만드는 것입니다.

## 이 프로젝트에서 고정한 모델

- replica 수 `N = 3`
- write는 quorum 이상 replica가 살아 있을 때만 성공
- read는 결정적 순서로 고른 `R`개 responder만 본다
- responder 안에서 가장 높은 version을 최신값으로 채택한다

## 왜 `W + R > N`이면 최신 읽기가 가능한가

write가 성공했다면 최소 `W`개 replica가 최신 version을 들고 있습니다. read가 `R`개 replica를 본다면, `W + R > N`일 때 read quorum과 write quorum은 적어도 한 replica 이상 겹칩니다. 그 한 replica가 최신 version을 들고 있으므로 read merge는 최신 version을 볼 수 있습니다.

## 왜 `W + R <= N`이면 stale read가 생길 수 있는가

write quorum과 read quorum이 완전히 분리될 수 있습니다. 이때 read는 write를 보지 못한 stale replica만 보고도 성공하므로, 오래된 version이나 missing value를 반환할 수 있습니다.

## 이 프로젝트가 일부러 단순화한 점

- 실제 시스템의 latency나 cross-region fanout은 다루지 않습니다.
- sloppy quorum, hinted handoff, read repair도 없습니다.
- 핵심 질문은 오직 “겹침이 있느냐 없느냐”입니다.
