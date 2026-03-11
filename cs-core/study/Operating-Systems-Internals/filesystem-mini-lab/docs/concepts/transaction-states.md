# Transaction States

## 왜 상태를 두 단계로 나누는가

journal entry를 한 번에 “있다/없다”로만 보면 recovery가 애매해진다. commit 직전 crash와 commit 직후 crash를 구분하려면 최소한 두 상태가 필요하다.

- `prepared`: intent는 기록됐지만 아직 commit되지 않은 상태
- `committed`: metadata update를 replay해도 되는 상태

## 이 프로젝트의 recovery 규칙

- `prepared` entry는 미완료 작업으로 보고 버린다.
- `committed` entry는 apply 후 journal에서 제거한다.
- write에서 이미 확보했던 새 block은 `prepared` discard 시 회수해야 leaked block이 남지 않는다.
