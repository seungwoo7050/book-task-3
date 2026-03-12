# Problem: Bridge Vs JSI Benchmark

> Status: VERIFIED
> Scope: async vs sync surface benchmark
> Last Checked: 2026-03-12

## 문제 요약

RN 0.84 기준으로 runtime 자체를 토글하는 대신,
`Promise + serialized payload` 표면과 `sync direct-call` 표면을 같은 workload로 비교하는 benchmark를 만든다.

## 왜 이 문제가 커리큘럼에 필요한가

architecture 이야기를 실제 앱과 분리해 배우면 쉽게 추상론이 된다.
이 프로젝트는 "runtime boundary의 비용 차이를 어떤 측정 단위와 결과물로 남길 것인가"를 묻는다.

## 제공 자료

- 기존 bridge-vs-jsi 과제 요구사항
- `problem/code/README.md`의 benchmark scaffold
- `problem/data/README.md`의 sample payload 자료

## 필수 요구사항

1. async interop-style surface
2. sync TurboModule/JSI-style surface
3. 5-run statistics
4. dashboard summary
5. deterministic JSON export

## 의도적 비범위

- legacy/new runtime toggle 실험
- 실제 C++ JSI binding 확장
- 네이티브 profiling 툴 통합

## 평가/검증 기준

```bash
make test
make app-build
make app-test
```

- 평균과 표준편차 계산이 정확해야 한다.
- 두 surface가 같은 payload 크기를 사용해야 한다.
- docs가 왜 surface benchmark를 택했는지 설명해야 한다.

## 원문/출처 보존 위치

- [SOURCE-PROVENANCE.md](SOURCE-PROVENANCE.md)
- [code/README.md](code/README.md)
- [data/README.md](data/README.md)
