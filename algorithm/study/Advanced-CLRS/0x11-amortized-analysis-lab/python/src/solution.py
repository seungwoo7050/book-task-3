import sys
input = sys.stdin.readline

def run_stack(q):
    stack = []
    cost = 0
    for _ in range(q):
        parts = input().split()
        if parts[0] == "PUSH":
            stack.append(int(parts[1]))
            cost += 1
        elif parts[0] == "POP":
            if stack:
                stack.pop()
                cost += 1
        elif parts[0] == "MULTIPOP":
            k = int(parts[1])
            pops = min(k, len(stack))
            cost += pops
            for _ in range(pops):
                stack.pop()
    return f"actual_cost={cost}\nsize={len(stack)}"

def run_counter(q):
    value = 0
    cost = 0
    for _ in range(q):
        if input().strip() != "INC":
            continue
        nxt = value + 1
        cost += (value ^ nxt).bit_count()
        value = nxt
    bits = bin(value)[2:] if value else "0"
    return f"actual_cost={cost}\nvalue={value}\nbits={bits}"

def solve():
    mode = input().strip().upper()
    if not mode:
        return
    q = int(input())
    if mode == "STACK":
        print(run_stack(q))
    elif mode == "COUNTER":
        print(run_counter(q))
    else:
        raise ValueError(mode)

if __name__ == "__main__":
    solve()
