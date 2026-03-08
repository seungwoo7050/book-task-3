FROM golang:1.22-alpine AS builder

RUN apk add --no-cache ca-certificates

WORKDIR /src

# Copy the target module only. This keeps the build aligned with the study tree
# instead of the legacy workspace.
COPY 01-backend-core/06-go-api-standard/go/go.mod ./go.mod
RUN go mod download

COPY 01-backend-core/06-go-api-standard/go/ ./

RUN CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build \
	-ldflags="-s -w" \
	-o /out/api ./cmd/api

FROM gcr.io/distroless/static-debian12

COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/
COPY --from=builder /out/api /api

EXPOSE 4000

USER nonroot:nonroot

ENTRYPOINT ["/api"]
