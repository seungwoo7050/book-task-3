package rpc

import (
	"context"
	"encoding/json"
	"errors"
	"fmt"
	"net"
	"sync"
	"sync/atomic"

	"study.local/go/ddia-distributed-systems/projects/01-rpc-framing/internal/framing"
)

type request struct {
	Type          string          `json:"type"`
	CorrelationID string          `json:"correlation_id"`
	Method        string          `json:"method"`
	Params        json.RawMessage `json:"params"`
}

type response struct {
	Type          string          `json:"type"`
	CorrelationID string          `json:"correlation_id"`
	Result        json.RawMessage `json:"result,omitempty"`
	Error         string          `json:"error,omitempty"`
}

type Handler func(context.Context, json.RawMessage) (any, error)

type Server struct {
	addr     string
	listener net.Listener
	handlers map[string]Handler
	conns    map[net.Conn]struct{}
	mu       sync.Mutex
}

func NewServer(addr string) *Server {
	return &Server{
		addr:     addr,
		handlers: map[string]Handler{},
		conns:    map[net.Conn]struct{}{},
	}
}

func (server *Server) Register(method string, handler Handler) {
	server.handlers[method] = handler
}

func (server *Server) Start() error {
	listener, err := net.Listen("tcp", server.addr)
	if err != nil {
		return err
	}
	server.listener = listener

	go func() {
		for {
			conn, err := listener.Accept()
			if err != nil {
				return
			}
			server.mu.Lock()
			server.conns[conn] = struct{}{}
			server.mu.Unlock()
			go server.handleConn(conn)
		}
	}()
	return nil
}

func (server *Server) Addr() string {
	if server.listener == nil {
		return ""
	}
	return server.listener.Addr().String()
}

func (server *Server) Close() error {
	server.mu.Lock()
	defer server.mu.Unlock()

	for conn := range server.conns {
		_ = conn.Close()
	}
	server.conns = map[net.Conn]struct{}{}
	if server.listener != nil {
		return server.listener.Close()
	}
	return nil
}

func (server *Server) handleConn(conn net.Conn) {
	defer func() {
		server.mu.Lock()
		delete(server.conns, conn)
		server.mu.Unlock()
		_ = conn.Close()
	}()

	decoder := &framing.Decoder{}
	buffer := make([]byte, 4096)
	for {
		n, err := conn.Read(buffer)
		if err != nil {
			return
		}
		payloads, err := decoder.Feed(buffer[:n])
		if err != nil {
			return
		}
		for _, payload := range payloads {
			var req request
			if err := json.Unmarshal(payload, &req); err != nil {
				continue
			}
			go server.dispatch(conn, req)
		}
	}
}

func (server *Server) dispatch(conn net.Conn, req request) {
	handler, ok := server.handlers[req.Method]
	resp := response{Type: "response", CorrelationID: req.CorrelationID}
	if !ok {
		resp.Error = fmt.Sprintf("unknown method: %s", req.Method)
		server.writeResponse(conn, resp)
		return
	}

	result, err := handler(context.Background(), req.Params)
	if err != nil {
		resp.Error = err.Error()
		server.writeResponse(conn, resp)
		return
	}
	if result != nil {
		buffer, err := json.Marshal(result)
		if err != nil {
			resp.Error = err.Error()
		} else {
			resp.Result = buffer
		}
	}
	server.writeResponse(conn, resp)
}

func (server *Server) writeResponse(conn net.Conn, resp response) {
	frame, err := framing.Encode(resp)
	if err != nil {
		return
	}
	_, _ = conn.Write(frame)
}

type pendingCall struct {
	response chan response
}

type Client struct {
	addr    string
	conn    net.Conn
	decoder *framing.Decoder

	mu      sync.Mutex
	pending map[string]pendingCall
	nextID  uint64
	closed  chan struct{}
}

func NewClient(addr string) *Client {
	return &Client{
		addr:    addr,
		decoder: &framing.Decoder{},
		pending: map[string]pendingCall{},
		closed:  make(chan struct{}),
	}
}

func (client *Client) Connect() error {
	conn, err := net.Dial("tcp", client.addr)
	if err != nil {
		return err
	}
	client.conn = conn
	go client.readLoop()
	return nil
}

func (client *Client) Close() error {
	if client.conn != nil {
		_ = client.conn.Close()
	}
	client.failAll(errors.New("connection closed"))
	select {
	case <-client.closed:
	default:
		close(client.closed)
	}
	return nil
}

func (client *Client) Call(ctx context.Context, method string, params any, out any) error {
	if client.conn == nil {
		return errors.New("rpc: client not connected")
	}

	paramBuffer, err := json.Marshal(params)
	if err != nil {
		return err
	}

	correlationID := fmt.Sprintf("req-%d", atomic.AddUint64(&client.nextID, 1))
	call := pendingCall{response: make(chan response, 1)}
	client.mu.Lock()
	client.pending[correlationID] = call
	client.mu.Unlock()

	frame, err := framing.Encode(request{
		Type:          "request",
		CorrelationID: correlationID,
		Method:        method,
		Params:        paramBuffer,
	})
	if err != nil {
		return err
	}
	if _, err := client.conn.Write(frame); err != nil {
		client.failPending(correlationID, err)
		return err
	}

	select {
	case resp := <-call.response:
		if resp.Error != "" {
			return errors.New(resp.Error)
		}
		if out == nil || len(resp.Result) == 0 {
			return nil
		}
		return json.Unmarshal(resp.Result, out)
	case <-ctx.Done():
		client.failPending(correlationID, ctx.Err())
		return ctx.Err()
	case <-client.closed:
		client.failPending(correlationID, errors.New("connection closed"))
		return errors.New("connection closed")
	}
}

func (client *Client) readLoop() {
	buffer := make([]byte, 4096)
	for {
		n, err := client.conn.Read(buffer)
		if err != nil {
			client.failAll(err)
			select {
			case <-client.closed:
			default:
				close(client.closed)
			}
			return
		}
		payloads, err := client.decoder.Feed(buffer[:n])
		if err != nil {
			client.failAll(err)
			return
		}
		for _, payload := range payloads {
			var resp response
			if err := json.Unmarshal(payload, &resp); err != nil {
				continue
			}
			client.mu.Lock()
			call, ok := client.pending[resp.CorrelationID]
			if ok {
				delete(client.pending, resp.CorrelationID)
			}
			client.mu.Unlock()
			if ok {
				call.response <- resp
			}
		}
	}
}

func (client *Client) failPending(correlationID string, err error) {
	client.mu.Lock()
	call, ok := client.pending[correlationID]
	if ok {
		delete(client.pending, correlationID)
	}
	client.mu.Unlock()
	if ok {
		call.response <- response{Type: "response", CorrelationID: correlationID, Error: err.Error()}
	}
}

func (client *Client) failAll(err error) {
	client.mu.Lock()
	defer client.mu.Unlock()
	for id, call := range client.pending {
		call.response <- response{Type: "response", CorrelationID: id, Error: err.Error()}
	}
	client.pending = map[string]pendingCall{}
}
