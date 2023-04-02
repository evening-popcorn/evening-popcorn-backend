package controllers

import (
	"game_host/lib"
	"game_host/repositories"
	gr "game_host/repositories/game_repository"
)

// GameController - controller fo games logic
type GameController struct {
	gameRepository  *gr.GameRepository
	movieRepository *repositories.MovieRepository
}

// NewGameController - constructor for game controller
func NewGameController() *GameController {
	return &GameController{
		gameRepository:  gr.NewGameRepository(),
		movieRepository: repositories.NewMovieRepository(),
	}
}

func (s *GameController) validateGame(
	user *lib.UserInfo,
	code string,
	checkIsMember bool,
	allowedStatus string,
) (*gr.GamePackage, error) {
	game, err := s.gameRepository.GetGame(code)
	if err != nil {
		return nil, err
	}
	if checkIsMember {
		inGame := s.gameRepository.IsInGame(code, user.Id)
		if !inGame {
			return nil, &gr.NotMemberOfGame{}
		}
	}
	if allowedStatus != "" {
		if game.Status != allowedStatus {
			switch game.Status {
			case gr.StatusStarted:
				return nil, &gr.GameAlreadyStarted{}
			case gr.StatusDeleted:
				return nil, &gr.GameDeleted{}
			}
		}
	}
	return game, nil
}

// CreateGame - create new game
func (s *GameController) CreateGame(user *lib.UserInfo, name string) (*gr.GameInfo, error) {
	code := s.gameRepository.CheckUserLock(user.Id)
	if code != "" {
		return nil, &UserAlreadyInGame{Code: code}
	}
	newGame := s.gameRepository.CreateGame(user, name)
	s.gameRepository.CreateUserLock(user.Id, newGame.Code)
	return &newGame, nil
}

// JoinGame - join to game by code
func (s *GameController) JoinGame(user *lib.UserInfo, code string) (*gr.GamePackage, error) {
	otherCode := s.gameRepository.CheckUserLock(user.Id)
	if otherCode != "" {
		return nil, &UserAlreadyInGame{Code: code}
	}
	game, err := s.validateGame(user, code, false, gr.StatusCreated)
	if err != nil {
		return nil, err
	}
	inGame := s.gameRepository.IsInGame(code, user.Id)
	if inGame {
		return nil, &gr.AlreadyInGame{}
	}
	if err != nil {
		return nil, err
	}
	s.gameRepository.AddPlayer(code, user)
	s.gameRepository.CreateUserLock(user.Id, code)
	game, _ = s.gameRepository.GetGame(code)
	return game, nil
}

// GetGame - get game by code
func (s *GameController) GetGame(user *lib.UserInfo, code string) (*gr.GamePackage, error) {
	game, err := s.validateGame(user, code, true, "")
	if err != nil {
		return nil, err
	}
	return game, nil
}

// LeaveGame - leave game by code
func (s *GameController) LeaveGame(user *lib.UserInfo, code string) (bool, error) {
	_, err := s.validateGame(user, code, true, "")
	if err != nil {
		return false, err
	}
	s.gameRepository.ReleaseUserLock(user.Id)
	host := s.gameRepository.IsUserHost(code, user.Id)
	if host {
		s.gameRepository.DeleteGame(code)
		return true, nil
	}
	s.gameRepository.RemoveUser(code, user.Id)
	return true, nil
}

// AddMoviesToRoster - add movies to roster
func (s *GameController) AddMoviesToRoster(user *lib.UserInfo, code string, movie int) (bool, error) {
	_, err := s.validateGame(user, code, true, gr.StatusCreated)
	if err != nil {
		return false, err
	}
	s.gameRepository.AddMovie(code, user.Id, movie)
	return true, nil
}

// RemoveMovieFromRoster - remove movie from user's roster
func (s *GameController) RemoveMovieFromRoster(user *lib.UserInfo, code string, movie int) (bool, error) {
	_, err := s.validateGame(user, code, true, gr.StatusCreated)
	if err != nil {
		return false, err
	}
	s.gameRepository.RemoveMovie(code, user.Id, movie)
	return true, nil
}

// GetUserRoster - get roster of game
func (s *GameController) GetUserRoster(user *lib.UserInfo, code string, locale string) ([]repositories.Movie, error) {
	_, err := s.validateGame(user, code, true, gr.StatusCreated)
	if err != nil {
		return nil, err
	}
	roster := s.gameRepository.GetMovies(code, user.Id)
	moviesInfo, err := s.movieRepository.GetMovies(roster, locale)
	if err != nil {
		return nil, err
	}
	var movies = make([]repositories.Movie, len(moviesInfo))
	i := 0
	for _, movie := range moviesInfo {
		movies[i] = movie
		i++
	}
	return movies, nil
}

// StartGame - start game
func (s *GameController) StartGame(user *lib.UserInfo, code string, movie string) (bool, error) {
	_, err := s.validateGame(user, code, true, gr.StatusCreated)
	if err != nil {
		return false, err
	}
	host := s.gameRepository.IsUserHost(code, user.Id)
	if !host {
		return false, &gr.NotHostOfGame{}
	}
	s.gameRepository.ChangeStatus(code, gr.StatusStarted)
	return true, nil
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
