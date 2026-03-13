# msglab blog

이 디렉터리는 `msglab`을 `source-first` 방식으로 다시 읽는 프로젝트 단위 blog 시리즈다. chronology는 프로젝트 README, `problem/README.md`, `cpp/README.md`, `cpp/Makefile`, `cpp/include/inc/Message.hpp`, `cpp/include/inc/Parser.hpp`, `cpp/src/Parser.cpp`, `cpp/tests/test_parser.cpp`를 기준으로 복원했다.

## source set

- [../../../shared-core/02-msglab/README.md](../../../shared-core/02-msglab/README.md)
- [../../../shared-core/02-msglab/problem/README.md](../../../shared-core/02-msglab/problem/README.md)
- [../../../shared-core/02-msglab/cpp/README.md](../../../shared-core/02-msglab/cpp/README.md)
- [../../../shared-core/02-msglab/cpp/Makefile](../../../shared-core/02-msglab/cpp/Makefile)
- [../../../shared-core/02-msglab/cpp/include/inc/Message.hpp](../../../shared-core/02-msglab/cpp/include/inc/Message.hpp)
- [../../../shared-core/02-msglab/cpp/include/inc/Parser.hpp](../../../shared-core/02-msglab/cpp/include/inc/Parser.hpp)
- [../../../shared-core/02-msglab/cpp/src/Parser.cpp](../../../shared-core/02-msglab/cpp/src/Parser.cpp)
- [../../../shared-core/02-msglab/cpp/tests/test_parser.cpp](../../../shared-core/02-msglab/cpp/tests/test_parser.cpp)

## 읽는 순서

1. [00-series-map.md](00-series-map.md)
2. [10-chronology-message-model-and-framing.md](10-chronology-message-model-and-framing.md)
3. [20-chronology-validation-and-command-normalization.md](20-chronology-validation-and-command-normalization.md)
4. [30-chronology-transcript-coverage-and-boundaries.md](30-chronology-transcript-coverage-and-boundaries.md)
5. [../../../shared-core/02-msglab/README.md](../../../shared-core/02-msglab/README.md)

## 검증 진입점

```bash
cd ../../../shared-core/02-msglab/cpp
make clean && make test
```

## chronology 메모

- `msglab`도 per-project git history가 얇아 대부분 `Day / Session` 형식으로 썼다.
- 현재 검증 신호는 `msglab parser tests passed.`와 README의 `verified` 표면으로만 잡는다.
- `Parser`는 IRC command와 arena command를 모두 받아들이지만, 여기서는 "실행"이 아니라 "구조화"까지만 다루는 점을 계속 기준으로 삼았다.

