package controllers

import (
	"game_host/lib"
	"game_host/repositories"
)

type GameController struct {
	gameRepository  *repositories.GameRepository
	movieRepository *repositories.MovieRepository
}

func NewGameController() *GameController {
	return &GameController{
		gameRepository:  repositories.NewGameRepository(),
		movieRepository: repositories.NewMovieRepository(),
	}
}

func (s *GameController) CreateGame(user lib.UserInfo, name string) {

}

func (s *GameController) JoinGame() {

}

func (s *GameController) AddMoviesToRoster() {

}

func (s *GameController) RemoveMovieFromRoster() {

}

func (s *GameController) StartGame() {

}

func (s *GameController) GetRoster() {

}

func (s *GameController) WaitTillStart() {

}

func (s *GameController) WaitTillMatch() {

}

func (s *GameController) LikeMovie() {

}

func (s *GameController) DislikeMovie() {

}

func (s *GameController) GetStatistics() {

}
