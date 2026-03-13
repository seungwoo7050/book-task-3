# 16 GitOps Deploy Evidence Ledger

## 10 docker-build-surface

- 시간 표지: 1단계: Dockerfile 작성 -> 2단계: .dockerignore 작성 -> 3단계: Helm Chart 스캐폴딩
- 당시 목표: Go 서비스용 multi-stage Dockerfile을 작성해야 한다.
- 변경 단위: `**/*_test.go`
- 처음 가설: 학습 포인트를 배포 자산 자체에 두기 위해 단일 서비스 배포 기준선만 다룬다.
- 실제 조치: Dockerfile 작성: 빌드 테스트: 빌드 컨텍스트 크기 감소 → 빌드 속도 향상. Chart.yaml

CLI:

```bash
cd 16-gitops-deploy/infra

# 빌드 컨텍스트를 study/ 루트로 설정
docker build -f solution/infra/Dockerfile -t go-backend-api:dev ../../

# 이미지 크기 확인
docker images go-backend-api:dev
# ~15-20MB

# 실행 테스트
docker run -p 4000:4000 go-backend-api:dev
```

- 검증 신호:
- 이 구간에서 실행 진입점과 검증 명령이 처음 함께 닫혔다.
- 핵심 코드 앵커: `solution/infra/Dockerfile`
- 새로 배운 것: multi-stage Docker build는 빌드 환경과 런타임 환경을 분리한다.
- 다음: 다음 글에서는 `20-helm-chart-and-runtime-shape.md`에서 이어지는 경계를 다룬다.
