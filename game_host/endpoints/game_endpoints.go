package endpoints

import (
	"game_host/controllers"
	"game_host/lib"
	gr "game_host/repositories/game_repository"
	"net/http"
)

type GameEndpoints struct {
	gameController controllers.GameController
}

func NewGameEndpoints() *GameEndpoints {
	return &GameEndpoints{
		gameController: *controllers.NewGameController(),
	}
}

type NewGame struct {
	Name string `json:"name"`
}

func (e *GameEndpoints) CreateGame(w http.ResponseWriter, r *http.Request, user *lib.UserInfo) {
	if r.Method != "POST" {
		lib.HttpError(
			w, lib.ErrorRes{
				Detail: "Method not supported",
			}, http.StatusMethodNotAllowed)
	}
	body, err := lib.ParseJson[NewGame](w, r)
	if err != nil {
		return
	}
	res := e.gameController.CreateGame(user, body.Name)
	lib.HttpOk(w, res)
}

type GameMeta struct {
	Code string `json:"code"`
}

func (e GameEndpoints) JoinGame(w http.ResponseWriter, r *http.Request, user *lib.UserInfo) {
	if r.Method != "POST" {
		lib.HttpError(
			w, lib.ErrorRes{
				Detail: "Method not supported",
			}, http.StatusMethodNotAllowed)
	}
	body, err := lib.ParseJson[GameMeta](w, r)
	if err != nil {
		return
	}
	res, err := e.gameController.JoinGame(user, body.Code)
	if err != nil {
		switch err.(type) {
		case *gr.GameAlreadyStarted:
			lib.HttpError(w, lib.ErrorRes{
				Detail: err.Error(),
			}, http.StatusUnauthorized)
		case *gr.AlreadyInGame:
			lib.HttpError(w, lib.ErrorRes{
				Detail: err.Error(),
			}, http.StatusUnauthorized)
		case *gr.GameNotExist:
			lib.HttpError(w, lib.ErrorRes{
				Detail: err.Error(),
			}, http.StatusUnauthorized)
		default:
			lib.HttpServerError(w)
		}
		return
	}
	lib.HttpOk(w, res)
}

func (e GameEndpoints) GetGame(w http.ResponseWriter, r *http.Request, user *lib.UserInfo) {
	if r.Method != "GET" {
		lib.HttpError(
			w, lib.ErrorRes{
				Detail: "Method not supported",
			}, http.StatusMethodNotAllowed)
	}
	code := r.URL.Query().Get("code")
	if code == "" {
		lib.HttpError(
			w, lib.ErrorRes{Detail: "Code param required"}, http.StatusBadRequest)
	}
	res, err := e.gameController.GetGame(user, code)
	if err != nil {
		switch err.(type) {
		case *gr.NotMemberOfGame:
			lib.HttpError(w, lib.ErrorRes{
				Detail: err.Error(),
			}, http.StatusUnauthorized)
		case *gr.GameNotExist:
			lib.HttpError(w, lib.ErrorRes{
				Detail: err.Error(),
			}, http.StatusUnauthorized)
		default:
			lib.HttpServerError(w)
		}
		return
	}
	lib.HttpOk(w, res)
}
