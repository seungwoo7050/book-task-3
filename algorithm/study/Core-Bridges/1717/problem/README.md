# Problem: 집합의 표현 (BOJ 1717)

## Problem Statement

서로소 집합(disjoint set union)을 구현하는 연습 문제다. 연산은 두 가지다.

- `0 a b`: 원소 `a`, `b`가 속한 집합을 합친다.
- `1 a b`: 두 원소가 같은 집합에 속하면 `YES`, 아니면 `NO`를 출력한다.

## Input

- 첫 줄에 `n m`이 주어진다.
- 이어지는 `m`개의 줄은 `0 a b` 또는 `1 a b` 형식의 질의다.

## Output

- 질의가 `1 a b`인 경우에만 결과를 출력한다.

## Note

이 디렉터리의 fixture는 legacy에서 가져온 공식 자료가 아니라, bridge 프로젝트를 위해 직접 만든 학습용 fixture다.

## Source

https://www.acmicpc.net/problem/1717
