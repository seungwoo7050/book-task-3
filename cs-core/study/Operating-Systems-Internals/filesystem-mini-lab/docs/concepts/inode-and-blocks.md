# Inode And Blocks

## 최소 filesystem에서 꼭 남는 구조

- inode는 파일 메타데이터와 block pointer를 가진다.
- block bitmap은 어떤 data block이 사용 중인지 표현한다.
- inode bitmap은 어떤 inode slot이 이미 파일에 할당됐는지 표현한다.

## 이 toy model에서의 단순화

- root directory 하나만 두고, 파일 이름을 inode index에 바로 매핑한다.
- permission bit, owner, timestamp 같은 메타데이터는 생략한다.
- 그래도 “이름 -> inode -> blocks” 흐름은 그대로 남기 때문에 allocation 학습에는 충분하다.

## 이 프로젝트에서 확인할 포인트

1. `create`는 inode bitmap을 먼저 바꾼다.
2. `write`는 data block을 새로 확보하고 inode의 block list를 갱신한다.
3. `unlink`는 inode와 block을 모두 free list로 돌려보낸다.
