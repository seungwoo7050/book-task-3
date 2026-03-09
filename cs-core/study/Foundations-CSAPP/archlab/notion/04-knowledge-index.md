# Architecture Lab — 지식 인덱스

## Y86-64 ISA

### 명령어 세트 특징
- x86-64의 축소된 교육용 부분집합
- 레지스터: 15개 범용 레지스터(%rax ~ %r14), 조건 코드(ZF, SF, OF)
- 메모리 접근: `mrmovq`, `rmmovq`만 사용 (주소 모드가 base-only)
- 산술/논리: `addq`, `subq`, `andq`, `xorq` (OPq 계열만)
- `cmpq`, `test`, `imulq` 등이 없음 — 0 비교는 `andq %r, %r` 패턴으로 대체
- 즉시값-레지스터 연산 없음 (공식 ISA 기준) → `iaddq` 추가가 Part B 과제

### 명령어 인코딩
- 1바이트: `halt`, `nop`, `ret`
- 2바이트: `rrmovq`, `OPq`, `cmovXX`, `pushq`, `popq`
- 10바이트: `irmovq`, `rmmovq`, `mrmovq` (8바이트 즉시값/변위 포함)
- `iaddq`: regids(1바이트) + valC(8바이트) = 총 10바이트

### Y86-64 어셈블리 패턴

| 패턴 | 용도 | 예시 |
|---|---|---|
| `andq %r, %r; je label` | NULL/0 체크 | 연결 리스트 순회 종료 |
| `pushq %rbx; call fn; popq %rbx` | callee-save 보존 | 재귀 호출 |
| `irmovq $C, %rN` | 상수 로드 | 포인터 증분, 카운터 초기값 |
| `xorq %rA, %rB` | XOR 체크섬 | copy_block |

## 프로세서 스테이지와 제어 신호

### SEQ 5단계

| 스테이지 | 역할 | iaddq에서의 동작 |
|---|---|---|
| Fetch | 명령어 읽기, 길이 판정 | `need_regids=1`, `need_valC=1` → PC+10 |
| Decode | 레지스터 읽기 | `srcB = rB` → valB 획득 |
| Execute | ALU 연산 | `aluA = valC`, `aluB = valB` → valE = valB + valC, CC 갱신 |
| Memory | 메모리 접근 | 없음 |
| Write-back | 레지스터 쓰기 | `dstE = rB` ← valE |

### PIPE vs SEQ 차이
- 같은 논리적 신호가 스테이지별 접두사를 가짐: `icode` → `f_icode`, `D_icode`, `E_icode`
- `set_cc`는 PIPE에서 `E_icode in { IOPQ, IIADDQ } && ...` 형태 (조건부 갱신)
- 파이프라인 해저드: 데이터 해저드(포워딩), 제어 해저드(분기 예측)

## 조건 코드와 오버플로

### ZF, SF, OF 계산
- ZF (Zero Flag): `result == 0`
- SF (Sign Flag): `result < 0`
- OF (Overflow Flag): `((a ^ result) & (b ^ result)) < 0`
  - 양수 + 양수 = 음수, 또는 음수 + 음수 = 양수일 때 발생
  - XOR 기법으로 캐리 없이 판정

## 파이프라인 최적화

### 루프 언롤링
- 기본: 원소당 ~9사이클 (루프 오버헤드 포함)
- 8-way: 루프 오버헤드를 8개 원소가 분담 → CPE 감소
- 핵심: 정확성 불변 — 같은 결과를 내면서 사이클만 줄임

### cmovg 패턴 (분기 제거)
```
xorq %rcx, %rcx     # 0으로 초기화
andq %r8, %r8       # CC 설정
cmovg %rbp, %rcx    # 양수이면 1을 %rcx에 이동
addq %rcx, %rax     # 0 또는 1을 count에 누적
```
- 분기 예측 실패 페널티(2~3사이클) 완전 제거
- `%rbp`에 상수 1을 미리 로드하는 셋업 필요

### 폴스루 테일 디스패치
- 남은 원소 수를 `iaddq $-1, %rdx; je TailN`으로 판정
- Tail7 → Tail6 → ... → Tail1으로 폴스루
- Duff's device와 유사한 접근

### CPE 벤치마크
- 공식 결과: Average CPE 9.16, Score 26.8/60.0
- 컴패니언 pseudo-CPE: `optimized_cpe < baseline_cpe` 성립 확인

## HCL 패치 자동화

### apply_hcl_patches.py
- `patch_seq()`: SEQ HCL 8개 치환
- `patch_pipe()`: PIPE HCL 8개 치환 (파이프라인 접두사 반영)
- `replace_exact_once()`: 멱등성 보장 — 이미 적용된 패치는 재적용하지 않음
- 용도: `make sync-official` 시 복원된 공식 HCL에 패치 적용

## 도구 참조

| 도구 | 용도 |
|---|---|
| `yas` | Y86-64 어셈블러 (.ys → .yo) |
| `yis` | Y86-64 명령어 시뮬레이터 |
| `ssim` | SEQ 프로세서 시뮬레이터 |
| `psim` | PIPE 프로세서 시뮬레이터 |
| `ptest` | HCL 회귀 테스트 (모든 명령어 조합) |
| `correctness.pl` | ncopy 정확성 테스트 |
| `benchmark.pl` | ncopy 성능 벤치마크 |
| Docker + linux/amd64 | Apple Silicon에서 시뮬레이터 실행 |
