# Realtime Collab Workspace 발표 문서

이 문서는 `Realtime Collab Workspace`를 면접이나 포트폴리오 리뷰에서 설명할 때 쓰는 발표 구조다.

## 발표 목표

- 협업 UI에서 무엇을 일부러 보이게 했는지 설명한다.
- optimistic patch, reconnect replay, conflict surface를 제품 관점에서 이야기한다.
- 앞선 포트폴리오 앱들과 다른 판단 포인트를 보여 준다.

## 6-8분 데모 흐름

1. 두 탭을 열고 presence가 서로 보이는지 먼저 보여 준다.
2. 한 탭에서 board card를 수정해 다른 탭으로 즉시 반영되는 장면을 보여 준다.
3. 한 탭을 disconnect한 뒤 수정하고, reconnect 시 queued patch가 replay되는 흐름을 보여 준다.
4. 같은 card를 두 탭에서 서로 다르게 수정해 conflict banner가 뜨는 장면으로 마무리한다.
5. 마지막으로 `/case-study`에서 왜 backend-less mock transport를 택했는지 짧게 정리한다.

## 발표 포인트

- optimistic UI는 빠른 화면이 아니라 복구 가능한 상태 모델이다.
- presence와 activity log는 장식이 아니라 신뢰 회복 장치다.
- mock transport만으로도 실시간 제품의 핵심 tradeoff를 설명할 수 있다.
