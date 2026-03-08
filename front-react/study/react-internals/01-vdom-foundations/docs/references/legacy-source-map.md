# Legacy Source Map

프로비넌스: `authored`

이 문서는 `legacy/virtual-dom`의 어떤 자산이 `01-vdom-foundations`의 어디로 옮겨졌는지 기록한다.

| 새 위치 | 프로비넌스 | 레거시 소스 |
| --- | --- | --- |
| `problem/original/README.md` | original | `legacy/virtual-dom/problem/README.md` |
| `problem/code/*` | original | `legacy/virtual-dom/problem/code/*` |
| `problem/script/Makefile` | adapted | `legacy/virtual-dom/problem/Makefile` |
| `ts/src/*` | adapted | `legacy/virtual-dom/solve/solution/*` |
| `ts/tests/*` | adapted | `legacy/virtual-dom/solve/test/*` |
| `docs/concepts/vdom-and-rendering.md` | authored | `legacy/virtual-dom/docs/virtual-dom.md`, `legacy/virtual-dom/docs/dom-rendering-pipeline.md` 참고 |
| `docs/concepts/jsx-to-vnode.md` | authored | `legacy/virtual-dom/docs/jsx-transform.md` 참고 |

## 제외한 자산

- `legacy/virtual-dom/devlog/*`: branch/commit 등 현재 확인 불가능한 메타데이터가 섞여 있어 `notion/` 재구성 대상으로 돌렸다.
- `legacy/virtual-dom/node_modules`: 신뢰할 수 없는 설치 산출물이므로 새 워크스페이스 검증에서 제외했다.
