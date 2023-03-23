package main

import (
	"game_host/endpoints"
	"game_host/lib"
	"net/http"
)

func SetupRouting() {
	auth := lib.NewAuthService()
	ep := endpoints.NewGameEndpoints()

	http.HandleFunc(
		"/game-api/v1/create-game",
		lib.CatchHttpPanic(auth.AuthUser(ep.CreateGame)))
	http.HandleFunc("/game-api/v1/join-game", lib.CatchHttpPanic(auth.AuthUser(ep.JoinGame)))
	http.HandleFunc("/game-api/v1/game", lib.CatchHttpPanic(auth.AuthUser(ep.GetGame)))
}
