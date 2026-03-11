import threading
import time

from rpc_framing import FrameDecoder, RPCClient, RPCServer, encode_frame


def test_decoder_handles_single_message():
    frame = encode_frame({"method": "ping"})
    decoder = FrameDecoder()
    payloads = decoder.feed(frame)
    assert len(payloads) == 1


def test_decoder_handles_split_chunks():
    frame = encode_frame({"hello": "world"})
    decoder = FrameDecoder()
    half = len(frame) // 2
    assert decoder.feed(frame[:half]) == []
    payloads = decoder.feed(frame[half:])
    assert len(payloads) == 1


def test_rpc_server_client_round_trip():
    server = RPCServer()
    server.register("echo", lambda params: params)
    server.start()
    client = RPCClient(server.address)
    client.connect()
    result = client.call("echo", {"msg": "hello"}, timeout=1.0)
    assert result["msg"] == "hello"
    client.close()
    server.close()


def test_rpc_handles_concurrent_calls():
    server = RPCServer()
    server.register("add", lambda params: {"sum": params["a"] + params["b"]})
    server.start()
    client = RPCClient(server.address)
    client.connect()

    sums = [0, 0, 0]
    threads = []
    for index, pair in enumerate(((1, 2), (10, 20), (100, 200))):
        def worker(slot=index, a=pair[0], b=pair[1]):
            sums[slot] = client.call("add", {"a": a, "b": b}, timeout=1.0)["sum"]

        thread = threading.Thread(target=worker)
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    assert sums == [3, 30, 300]
    client.close()
    server.close()


def test_rpc_propagates_server_errors_and_timeout():
    server = RPCServer()

    def fail(_params):
        raise ValueError("intentional failure")

    def slow(_params):
        time.sleep(0.2)
        return {"status": "done"}

    server.register("fail", fail)
    server.register("slow", slow)
    server.start()
    client = RPCClient(server.address)
    client.connect()

    try:
        client.call("fail", {}, timeout=1.0)
    except RuntimeError as error:
        assert "intentional failure" in str(error)
    else:
        raise AssertionError("expected server error")

    try:
        client.call("slow", {}, timeout=0.02)
    except TimeoutError:
        pass
    else:
        raise AssertionError("expected timeout")

    client.close()
    server.close()
