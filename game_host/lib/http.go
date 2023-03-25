package lib

import (
	"encoding/json"
	"net/http"
)

type ErrorRes struct {
	Detail string `json:"detail"`
}

func HttpError(w http.ResponseWriter, err any, statusCode int) {
	w.Header().Set("Content-Type", "application/json; charset=UTF-8")
	w.WriteHeader(statusCode)
	_ = json.NewEncoder(w).Encode(err)
}
func HttpOk(w http.ResponseWriter, res any) {
	w.Header().Set("Content-Type", "application/json; charset=UTF-8")
	w.WriteHeader(http.StatusOK)
	_ = json.NewEncoder(w).Encode(res)
}
func HttpServerError(w http.ResponseWriter) {
	err := ErrorRes{
		Detail: "Internal server error",
	}
	w.Header().Set("Content-Type", "application/json; charset=UTF-8")
	w.WriteHeader(http.StatusInternalServerError)
	_ = json.NewEncoder(w).Encode(err)
}

func CatchHttpPanic(f func(w http.ResponseWriter, r *http.Request)) func(w http.ResponseWriter, r *http.Request) {
	return func(w http.ResponseWriter, r *http.Request) {
		defer func() {
			if err := recover(); err != nil {
				HttpServerError(w)
			}
		}()
		f(w, r)
	}
}

func ParseJson[T any](w http.ResponseWriter, r *http.Request) (*T, error) {
	var body T
	err := json.NewDecoder(r.Body).Decode(&body)
	if err != nil {
		HttpError(
			w,
			ErrorRes{
				Detail: "Bad json",
			},
			http.StatusBadRequest,
		)
		return nil, err
	}
	return &body, nil
}
