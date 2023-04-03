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
	http.HandleFunc("/game-api/v1/game/join", lib.CatchHttpPanic(auth.AuthUser(ep.JoinGame)))
	http.HandleFunc("/game-api/v1/game", lib.CatchHttpPanic(auth.AuthUser(ep.GetGame)))
	http.HandleFunc("/game-api/v1/game/movie", lib.CatchHttpPanic(auth.AuthUser(ep.GameMovie)))
	http.HandleFunc("/game-api/v1/game/wait-start", lib.CatchHttpPanic(auth.AuthUser(ep.WaitUntilGameStart)))
	http.HandleFunc("/game-api/v1/game/start", lib.CatchHttpPanic(auth.AuthUser(ep.StartGame)))
	http.HandleFunc("/game-api/v1/game/roster", lib.CatchHttpPanic(auth.AuthUser(ep.GetMovieRoster)))
	http.HandleFunc("/game-api/v1/game/like", lib.CatchHttpPanic(auth.AuthUser(ep.LikeMovie)))
}
