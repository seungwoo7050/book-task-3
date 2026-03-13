# Snapshot Visibility

- transaction은 시작 시점의 committed watermark를 snapshot으로 잡는다.
- read는 snapshot 이하의 committed version만 볼 수 있다.
- 자기 자신의 uncommitted write는 예외적으로 read-your-own-writes로 보인다.

