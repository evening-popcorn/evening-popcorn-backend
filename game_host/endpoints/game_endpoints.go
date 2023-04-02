package endpoints

import (
	"game_host/controllers"
	"game_host/lib"
	gr "game_host/repositories/game_repository"
	"net/http"
	"strconv"
)

// GameEndpoints - game endpoints
type GameEndpoints struct {
	gameController controllers.GameController
}

type SimpleResponse struct {
	Success bool `json:"success"`
}

// NewGameEndpoints - create new game endpoints
func NewGameEndpoints() *GameEndpoints {
	return &GameEndpoints{
		gameController: *controllers.NewGameController(),
	}
}

type NewGame struct {
	Name string `json:"name"`
}

// AlreadyInOtherGameError - error when user already in other game
type AlreadyInOtherGameError struct {
	Detail string `json:"detail"`
	Code   string `json:"code"`
}

// CreateGame - create new game
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
	res, err := e.gameController.CreateGame(user, body.Name)
	if err != nil {
		switch err.(type) {
		case *controllers.UserAlreadyInGame:
			lib.HttpError(w, AlreadyInOtherGameError{
				Detail: "Already in other game",
				Code:   err.Error(),
			}, http.StatusConflict)
		default:
			lib.HttpServerError(w)
		}
		return
	}
	lib.HttpOk(w, res)
}

type GameMeta struct {
	Code string `json:"code"`
}

// JoinGame - join game by code
func (e *GameEndpoints) JoinGame(w http.ResponseWriter, r *http.Request, user *lib.UserInfo) {
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
		case *controllers.UserAlreadyInGame:
			lib.HttpError(w, AlreadyInOtherGameError{
				Detail: "Already in other game",
				Code:   err.Error(),
			}, http.StatusConflict)
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

// GetGame - get game by code
func (e *GameEndpoints) GetGame(w http.ResponseWriter, r *http.Request, user *lib.UserInfo) {
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

type AddMovieBody struct {
	Code    string `json:"code"`
	MovieId int    `json:"movie_id"`
}

func (e *GameEndpoints) GameMovie(w http.ResponseWriter, r *http.Request, user *lib.UserInfo) {
	switch r.Method {
	case "GET":
		e.GetMovies(w, r, user)
	case "POST":
		e.AddMovie(w, r, user)
	case "DELETE":
		e.RemoveMovie(w, r, user)
	default:
		lib.HttpError(
			w, lib.ErrorRes{
				Detail: "Method not supported",
			}, http.StatusMethodNotAllowed)
	}
}

// AddMovie - add movie to game
func (e *GameEndpoints) AddMovie(w http.ResponseWriter, r *http.Request, user *lib.UserInfo) {
	body, err := lib.ParseJson[AddMovieBody](w, r)
	if err != nil {
		return
	}
	res, err := e.gameController.AddMoviesToRoster(user, body.Code, body.MovieId)
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
		case *gr.GameAlreadyStarted:
			lib.HttpError(w, lib.ErrorRes{
				Detail: err.Error(),
			}, http.StatusUnauthorized)
		default:
			lib.HttpServerError(w)
		}
		return
	}
	lib.HttpOk(w, SimpleResponse{
		Success: res,
	})

}

func (e *GameEndpoints) GetMovies(w http.ResponseWriter, r *http.Request, user *lib.UserInfo) {
	code := r.URL.Query().Get("code")
	if code == "" {
		lib.HttpError(
			w, lib.ErrorRes{Detail: "Code param required"}, http.StatusBadRequest)
	}
	locale := r.Header.Get("X-Language")
	if locale == "" {
		locale = "en"
	}
	res, err := e.gameController.GetUserRoster(user, code, locale)
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

func (e *GameEndpoints) RemoveMovie(w http.ResponseWriter, r *http.Request, user *lib.UserInfo) {
	code := r.URL.Query().Get("code")
	movie, err := strconv.Atoi(r.URL.Query().Get("movie_id"))
	if err != nil {
		lib.HttpError(
			w, lib.ErrorRes{Detail: "Movie id param required"}, http.StatusBadRequest)
	}
	if code == "" {
		lib.HttpError(
			w, lib.ErrorRes{Detail: "Code param required"}, http.StatusBadRequest)
	}
	locale := r.Header.Get("X-Language")
	if locale == "" {
		locale = "en"
	}
	res, err := e.gameController.RemoveMovieFromRoster(user, code, movie)
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
	lib.HttpOk(w, SimpleResponse{
		Success: res,
	})
}
