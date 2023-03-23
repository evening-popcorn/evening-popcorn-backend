package controllers

import (
	"game_host/lib"
	"game_host/repositories"
	gr "game_host/repositories/game_repository"
)

type GameController struct {
	gameRepository  *gr.GameRepository
	movieRepository *repositories.MovieRepository
}

func NewGameController() *GameController {
	return &GameController{
		gameRepository:  gr.NewGameRepository(),
		movieRepository: repositories.NewMovieRepository(),
	}
}

func (s *GameController) CreateGame(user *lib.UserInfo, name string) gr.GameInfo {
	newGame := s.gameRepository.CreateGame(user, name)
	return newGame
}

func (s *GameController) JoinGame(user *lib.UserInfo, code string) (*gr.GamePackage, error) {
	game, err := s.gameRepository.GetGame(code)
	//if err != nil {
	//	return nil, err
	//}
	if game.Status != gr.StatusCreated {
		return nil, &gr.GameAlreadyStarted{}
	}
	inGame := s.gameRepository.IsInGame(code, user.Id)
	if inGame {
		return nil, &gr.AlreadyInGame{}
	}
	if err != nil {
		return nil, err
	}
	s.gameRepository.AddPlayer(code, user)
	game, _ = s.gameRepository.GetGame(code)
	return game, nil
}

func (s *GameController) GetGame(user *lib.UserInfo, code string) (*gr.GamePackage, error) {
	game, err := s.gameRepository.GetGame(code)
	if err != nil {
		return nil, err
	}
	inGame := s.gameRepository.IsInGame(code, user.Id)
	if !inGame {
		return nil, &gr.NotMemberOfGame{}
	}
	return game, nil
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
