package controllers

type UserAlreadyInGame struct {
	Code string `json:"code"`
}

func (e UserAlreadyInGame) Error() string {
	return e.Code
}
