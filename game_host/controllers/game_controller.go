package controllers

import (
	"game_host/lib"
	"game_host/repositories"
	gr "game_host/repositories/game_repository"
	"math"
	"time"
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
func (s *GameController) StartGame(user *lib.UserInfo, code string) (bool, error) {
	_, err := s.validateGame(user, code, true, gr.StatusCreated)
	if err != nil {
		return false, err
	}
	host := s.gameRepository.IsUserHost(code, user.Id)
	if !host {
		return false, &gr.NotHostOfGame{}
	}
	movies := s.gameRepository.GetAllMovies(code)
	s.gameRepository.SaveMovieRoster(code, movies)
	s.gameRepository.ChangeStatus(code, gr.StatusStarted)
	return true, nil
}

// WaitTillStart - wait till game start
func (s *GameController) WaitTillStart(user *lib.UserInfo, code string, timeout int) (bool, error) {
	_, err := s.validateGame(user, code, true, gr.StatusCreated)
	if err != nil {
		return false, err
	}
	for i := 0; i < timeout*10; i++ {
		switch s.gameRepository.GetStatus(code) {
		case gr.StatusCreated:
			time.Sleep(time.Millisecond * 100)
			continue
		case gr.StatusStarted:
			return true, nil
		case gr.StatusDeleted:
			return false, &gr.GameDeleted{}
		}
	}
	return false, nil
}

type RosterInfo struct {
	Movies     []repositories.Movie `json:"movies"`
	Page       int                  `json:"page"`
	TotalPages int                  `json:"total_pages"`
}

func (s *GameController) GetRoster(user *lib.UserInfo, code string, page int, locale string) (*RosterInfo, error) {
	_, err := s.validateGame(user, code, true, gr.StatusStarted)
	if err != nil {
		return nil, err
	}
	moviesId := s.gameRepository.GetRosterMovies(code, (page-1)*20, page*20)
	if len(moviesId) == 0 {
		return &RosterInfo{
			Movies:     []repositories.Movie{},
			Page:       page,
			TotalPages: int(math.Ceil(float64(s.gameRepository.GetRosterLen(code)) / 20.0)),
		}, nil
	}
	moviesInfo, err := s.movieRepository.GetMovies(moviesId, locale)
	if err != nil {
		return nil, err
	}
	movies := make([]repositories.Movie, len(moviesInfo))
	i := 0
	for _, id := range moviesId {
		movies[i] = moviesInfo[id]
		i++
	}
	return &RosterInfo{
		Movies:     movies,
		Page:       page,
		TotalPages: int(math.Ceil(float64(s.gameRepository.GetRosterLen(code)) / 20.0)),
	}, nil
}

type NotInRoster struct {
}

func (e *NotInRoster) Error() string {
	return "Movie is not in roster"
}
func (s *GameController) LikeMovie(user *lib.UserInfo, code string, movie int) (bool, error) {
	_, err := s.validateGame(user, code, true, gr.StatusStarted)
	if err != nil {
		return false, err
	}
	if !s.gameRepository.CheckIsInRoster(code, movie) {
		return false, &NotInRoster{}
	}
	s.gameRepository.AddLike(code, user.Id, movie)
	return true, nil
}

func (s *GameController) WaitTillMatch() {

}

func (s *GameController) DislikeMovie() {

}

func (s *GameController) GetStatistics() {

}
