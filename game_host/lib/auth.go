package lib

import (
	"encoding/json"
	"fmt"
	"io"
	"net/http"
)

type UserInfo struct {
	Id    string `json:"id"`
	Email string `json:"email"`
	Name  string `json:"name"`
}

type AuthService struct {
	client http.Client
}

type AuthError struct {
}

func (e *AuthError) Error() string {
	return "Unable to authenticate user"
}

type UnexpectedError struct {
}

func (e *UnexpectedError) Error() string {
	return "User"
}

func NewAuthService() *AuthService {
	return &AuthService{
		client: http.Client{},
	}
}
func (s *AuthService) getUser(token string) (*UserInfo, error) {
	req, err := http.NewRequest(
		"GET",
		GetEnv("API_GATEWAY_URL", "http://api-gateway")+"/api/v1/auth/me",
		nil,
	)
	if err != nil {
		return nil, err
	}
	req.Header.Add("X-Token", token)
	res, err := s.client.Do(req)
	if err != nil {
		return nil, err
	}
	if res.StatusCode == 401 {
		return nil, &AuthError{}
	}
	if res.StatusCode != 200 {
		return nil, &UnexpectedError{}
	}
	body, err := io.ReadAll(res.Body)
	var user UserInfo
	if err := json.Unmarshal(body, &user); err != nil {
		return nil, &UnexpectedError{}
	}
	return &user, nil
}

func (s *AuthService) AuthUser(f func(w http.ResponseWriter, r *http.Request, user *UserInfo)) func(w http.ResponseWriter, r *http.Request) {
	return func(w http.ResponseWriter, r *http.Request) {
		user, err := s.getUser(r.Header.Get("X-Token"))
		if err != nil {
			switch err.(type) {
			case *AuthError:
				HttpError(w, ErrorRes{Detail: "Method needs auth"}, http.StatusUnauthorized)
			default:
				fmt.Println(err)
				HttpServerError(w)
			}
			return
		}
		f(w, r, user)
	}
}
