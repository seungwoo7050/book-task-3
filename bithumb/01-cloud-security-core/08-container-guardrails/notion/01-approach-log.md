# 접근 기록

## 핵심 선택

- manifest 검사와 image metadata 검사를 분리했습니다. 빌드 시점과 배포 시점의 위험이 다를 수 있기 때문입니다.
- insecure/secure fixture를 두 쌍으로 만들어 양방향 검증이 가능하게 했습니다.
- YAML 파싱은 `yaml.safe_load_all`을 사용해 multi-document manifest도 처리하게 했습니다.

## 버린 대안

- 실제 EKS 클러스터를 띄우는 방식은 학습 비용이 너무 커서 제외했습니다.
- Admission controller나 runtime sensor까지 포함하는 구조는 현재 범위를 넘는다고 판단했습니다.
- 규칙 수를 더 늘리기보다, 주니어가 설명하기 좋은 대표 규칙 여덟 개에 집중했습니다.

## 다음 프로젝트와의 연결

이 프로젝트는 “클러스터 없이도 manifest 단에서 상당한 보안 설명이 가능하다”는 자신감을 줍니다.
capstone에서는 같은 scanner가 ingestion API 뒤에서 실행되므로, 지금 단계에서 어떤 입력을 어떤 finding으로 바꾸는지 명확해야 합니다.

## 다시 써도 유지할 기준

- 각 규칙이 어떤 운영 위험과 연결되는지 설명 가능해야 합니다.
- secure fixture 0건 검증을 유지해야 합니다.
- manifest와 image metadata의 역할 차이를 분명히 해야 합니다.
