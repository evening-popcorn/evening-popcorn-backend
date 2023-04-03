package repositories

import (
	"encoding/json"
	"fmt"
	"game_host/lib"
	"io"
	"log"
	"net/http"
	"net/url"
	"strconv"
)

type Movie struct {
	Id            int    `json:"id"`
	Title         string `json:"title"`
	Poster        string `json:"poster"`
	OriginalTitle string `json:"original_title"`
	ReleaseDate   string `json:"release_date"`
}

type UnexpectedError struct {
}

func (e *UnexpectedError) Error() string {
	return "Unexpected error"
}

type MovieRepository struct {
	baseUrl string
	client  http.Client
}

func NewMovieRepository() *MovieRepository {
	return &MovieRepository{
		baseUrl: lib.GetEnv("MOVIEGEEK_URL", "http://moviegeek"),
		client:  http.Client{},
	}
}

func (r MovieRepository) GetMovies(movieIds []int, locale string) (map[int]Movie, error) {
	baseURL := r.baseUrl
	resource := "/v1/movie/bulk"
	params := url.Values{}
	for _, id := range movieIds {
		params.Add("movie_ids", fmt.Sprintf("%d", id))
	}
	params.Add("locale", locale)

	u, _ := url.ParseRequestURI(baseURL)
	u.Path = resource
	u.RawQuery = params.Encode()
	urlStr := fmt.Sprintf("%v", u)

	res, err := http.Get(urlStr)
	if err != nil {
	}
	if res.StatusCode != http.StatusOK {
		body, _ := io.ReadAll(res.Body)
		log.Print("Unexpected status code: ", res.StatusCode, " Body: ", string(body))
		return nil, &UnexpectedError{}
	}

	body, err := io.ReadAll(res.Body)
	if err != nil {
		return nil, &UnexpectedError{}
	}
	var objmap map[string]json.RawMessage
	if err := json.Unmarshal(body, &objmap); err != nil {
		return nil, err
	}
	var movies = make(map[int]Movie)
	for id, movieInfo := range objmap {
		var movie Movie
		if err := json.Unmarshal(movieInfo, &movie); err != nil {
			continue
		}
		movieId, _ := strconv.Atoi(id)
		movies[movieId] = movie
	}
	return movies, nil
}
