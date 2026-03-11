# 접근 로그

## 1. register 모델을 일부러 작게 잡았습니다
multi-key storage 대신 single-version register로 줄여서, 핵심 질문을 `W/R/N` 겹침으로 제한했습니다.

## 2. responder 선택은 결정적으로 고정했습니다
실행마다 다른 replica를 고르면 stale read 데모가 흔들립니다. 그래서 cluster order를 고정하고, read quorum은 항상 그 순서대로 responder를 선택하게 했습니다.

## 3. write 실패는 partial success로 남기지 않았습니다
이번 단계에서는 “quorum이 없으면 version도, local apply도 전진하지 않는다”는 규칙을 택했습니다. 현실 시스템의 partial write 정리는 08 장애 주입 단계에서 다시 다룹니다.
