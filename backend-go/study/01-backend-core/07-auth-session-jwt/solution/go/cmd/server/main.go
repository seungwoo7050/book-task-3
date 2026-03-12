package main

import (
	"log"
	"net/http"

	"github.com/woopinbell/go-backend/study/01-backend-core/07-auth-session-jwt/internal/auth"
)

func main() {
	server, err := auth.NewServer(nil)
	if err != nil {
		log.Fatal(err)
	}
	log.Println("listening on :4030")
	log.Fatal(http.ListenAndServe(":4030", server.Routes()))
}
