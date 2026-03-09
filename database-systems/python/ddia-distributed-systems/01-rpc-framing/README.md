# 01 RPC Framing

## Summary

length-prefixed TCP framing 위에 간단한 request/response RPC를 올리고, correlation id와 pending map으로 동시 요청을 처리한다. Python 분산 트랙의 첫 단계다.

## Status

- 상태: `verified`
- 구현 언어: `Python 3.14`
- 범위: decoder, RPC server, RPC client, timeout/error propagation

## Commands

```bash
python3 -m pip install -U pytest
PYTHONPATH=src python3 -m pytest
PYTHONPATH=src python3 -m rpc_framing
```
