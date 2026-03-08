package main

import (
	"log"
	"net/http"

	"github.com/woopinbell/go-backend/study/01-backend-core/05-http-rest-basics/internal/api"
)

func main() {
	server := api.NewServer()
	log.Println("listening on :4020")
	log.Fatal(http.ListenAndServe(":4020", server.Routes()))
}
