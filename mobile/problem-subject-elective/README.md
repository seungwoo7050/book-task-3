# mobile 비필수 문제지

여기서 `elective`는 핵심 경로 다음에 읽는 확장 문제라는 뜻입니다. 아키텍처 경계와 배포 규율처럼, 제품 앱을 더 깊게 다루기 위한 항목만 남깁니다.

| lab | 한 줄 문제 요약 | 검증 시작점 |
| --- | --- | --- |
| [01-bridge-vs-jsi-react-native](01-bridge-vs-jsi-react-native.md) | RN 0.84 기준으로 runtime 자체를 토글하는 대신, Promise + serialized payload 표면과 sync direct-call 표면을 같은 workload로 비교하는 benchmark를 만든다. | `make test && make app-build && make app-test` |
| [02-native-modules-react-native](02-native-modules-react-native.md) | Battery, Haptics, Sensor 세 모듈의 TypeScript public spec을 고정하고, codegen summary와 consumer app을 통해 JS/native 경계를 설명하는 과제다. | `make test && make codegen && make app-build && make app-test` |
| [03-app-distribution-react-native](03-app-distribution-react-native.md) | 검증된 realtime-chat snapshot을 release candidate로 가져와, 실제 credential을 저장소에 넣지 않고도 packaging, env separation, automation rehearsal을 증명하는 과제다. | `make test && make app-build && make app-test && make release-rehearsal` |

## 스포일러 경계

각 lab의 정답 코드, 공식 구현 진입점, 해설은 같은 이름의 sibling `_answer.md` 문서에서 확인한다.
