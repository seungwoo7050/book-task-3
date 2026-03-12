# Problem: Native Modules

> Status: VERIFIED
> Scope: spec + codegen + consumer app
> Last Checked: 2026-03-12

## 문제 요약

Battery, Haptics, Sensor 세 모듈의 TypeScript public spec을 고정하고,
codegen summary와 consumer app을 통해 JS/native 경계를 설명하는 과제다.

## 왜 이 문제가 커리큘럼에 필요한가

RN architecture를 이해한 뒤에는 경계를 실제 모듈 계약으로 내려와야 한다.
이 프로젝트는 "네이티브 연동을 기능 구현이 아니라 public contract 설계 문제로 다룰 수 있는가"를 확인한다.

## 제공 자료

- 기존 native-modules 과제 요구사항
- `problem/code/README.md`의 spec/codegen scaffold
- `problem/data/README.md`의 참고 자료

## 필수 요구사항

1. typed module specs
2. codegen summary export
3. consumer screen
4. platform parity 설명 문서

## 의도적 비범위

- production native package 배포
- sensor streaming 고도화
- 플랫폼별 권한 UX 완성도 개선

## 평가/검증 기준

```bash
make test
make codegen
make app-build
make app-test
```

- spec이 TypeScript 수준에서 명확히 드러나야 한다.
- codegen summary가 재생성 가능해야 한다.
- consumer app이 module contract를 설명하는 데 충분해야 한다.

## 원문/출처 보존 위치

- [SOURCE-PROVENANCE.md](SOURCE-PROVENANCE.md)
- [code/README.md](code/README.md)
- [data/README.md](data/README.md)
