package endpoints

import (
	"game_host/controllers"
	"net/http"
)

var gameController = controllers.NewGameController()

func CreateGame(w http.ResponseWriter, r *http.Request) {
	//r.URL.Query().Get()
}
