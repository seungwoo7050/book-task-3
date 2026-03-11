> pre-migration path 기준 문서
> 현재 경로 매핑은 [`docs/catalog/path-migration-map.md`](../../../../../docs/catalog/path-migration-map.md)를 본다.

# Differentiation & Exposure Design — 지식 인덱스

## 핵심 개념

| 개념 | 설명 | 관련 파일 |
|------|------|-----------|
| exposure | 도구의 한국어 노출 정보를 담는 객체. `{ ko: { tagline, description, differentiator } }` | `shared/src/catalog.ts` |
| tagline | 15자 이내의 한국어 핵심 기능 요약 | catalog.ts → exposure.ko.tagline |
| differentiator | 비슷한 도구 대비 이 도구만의 장점 설명 | catalog.ts → exposure.ko.differentiator |
| reason template | 추천 근거를 생성하는 고정 패턴. 동사로 시작하는 한국어 문장 | `recommendation-service.ts` |
| reasonTrace | 추천 결과에 포함되는 추적 정보. 도구 선택 이유, 점수, exposure | `contracts.ts → reasonTraceSchema` |
| fallback display | exposure.ko가 없을 때 영문 description을 회색으로 표시하는 처리 | `mcp-dashboard.tsx` |

## 구현 위치

| 기능 | capstone 버전 | 파일 |
|------|--------------|------|
| 한국어 exposure 필드 | v0 | `shared/src/catalog.ts` |
| reason template 생성 | v0 | `node/src/services/recommendation-service.ts` |
| 대시보드 노출 카드 | v0 | `react/components/mcp-dashboard.tsx` |

## 다음 단계 연결

- **stage 04**: baseline selector가 exposure 포함 추천 결과를 반환
- **stage 07**: 대시보드에서 노출 카드를 CRUD 가능하게 확장
