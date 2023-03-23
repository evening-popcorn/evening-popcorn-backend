package game_repository

import "game_host/lib"

type GameInfo struct {
	Code     string       `json:"id"`
	Host     lib.UserInfo `json:"host"`
	Name     string       `json:"name"`
	CreateAt string       `json:"createAt"`
}

type PlayerInfo struct {
	Id     string `json:"id"`
	Email  string `json:"email"`
	Name   string `json:"name"`
	IsHost bool   `json:"isHost"`
}

type GamePackage struct {
	Info    GameInfo     `json:"info"`
	Players []PlayerInfo `json:"players"`
	Status  string       `json:"status"`
}

type GameNotExist struct {
}

func (e *GameNotExist) Error() string {
	return "Game does not exist"
}

type GameAlreadyStarted struct {
}

func (e *GameAlreadyStarted) Error() string {
	return "Game already started"
}

type AlreadyInGame struct {
}

func (e *AlreadyInGame) Error() string {
	return "Already in game"
}

type NotMemberOfGame struct {
}

func (e *NotMemberOfGame) Error() string {
	return "You not part of this game"
}

const (
	StatusCreated = "Created"
)
