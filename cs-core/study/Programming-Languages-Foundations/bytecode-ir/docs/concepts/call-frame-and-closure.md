# Call Frame과 Closure

tree-walk interpreter에서는 environment chain이 바로 runtime 구조였지만, VM에서는 그 구조를 더 명시적으로 쪼갭니다.

## current runtime model

- call frame는 `locals`, `stack`, `ip`를 가집니다.
- closure는 `FunctionProto`와 `captures` tuple을 가집니다.
- nested function을 만들 때 compiler는 free variable을 `capture_sources`로 기록하고, runtime은 그 값을 실제 capture slot에 채웁니다.

## explicit capture slot을 두는 이유

- "어떤 outer 값이 이 함수에 들어왔는가"를 instruction과 데이터 구조 양쪽에서 추적하기 쉽습니다.
- 이후 optimizer나 closure conversion 개념으로 확장하기 좋은 표면이 됩니다.
