package repositories

import (
	"game_host/lib"
	"net/http"
)

type MovieRepository struct {
	baseUrl string
	client  http.Client
}

func NewMovieRepository() *MovieRepository {
	return &MovieRepository{
		baseUrl: lib.GetEnv("MOVIEGEEK_BASE_URL", "http://moviegeek"),
		client:  http.Client{},
	}
}
