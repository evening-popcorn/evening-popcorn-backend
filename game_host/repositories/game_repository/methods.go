package game_repository

import (
	"encoding/json"
	"game_host/lib"
	"github.com/redis/go-redis/v9"
	"strconv"
	"time"
)

// GameRepository - keys for redis
// game.{code} - game info
// game.{code}.players - players in game
// game.{code}.player.{id} - player info
// game.{code}.movies.{id} - movies in game of user
// game.{code}.status - status of game
// game.{code}.likes.{id} - likes for movie
// game.{code}.dislikes.{id} - dislikes for movie
// lock.{id} - lock for user

// CreateGame - create new game
func (r *GameRepository) CreateGame(info *lib.UserInfo, name string) GameInfo {
	var code string
	for {
		code = lib.GenerateRandString(8)
		exist := r.redisClient.Exists(r.ctx, "game."+code)
		if exist.Val() == 0 {
			break
		}
	}
	gameInfo := GameInfo{
		Code:     code,
		Host:     *info,
		Name:     name,
		CreateAt: time.Now().String(),
	}
	obj, _ := json.Marshal(gameInfo)
	r.redisClient.Set(r.ctx, "game."+code, obj, time.Hour*24)

	r.redisClient.SAdd(r.ctx, "game."+code+".players", info.Id)
	r.redisClient.Expire(r.ctx, "game."+code+".players", time.Hour*24)

	host, _ := json.Marshal(PlayerInfo{
		Id:     info.Id,
		Email:  info.Email,
		Name:   info.Name,
		IsHost: true,
	})
	r.redisClient.Set(r.ctx, "game."+code+".player."+info.Id, host, time.Hour*24)

	r.redisClient.Set(r.ctx, "game."+code+".status", StatusCreated, time.Hour*24)
	return gameInfo
}

// CreateUserLock - create lock for user
func (r *GameRepository) CreateUserLock(userId string, code string) {
	r.redisClient.Set(r.ctx, "lock."+userId, code, 24*time.Hour)
}

// CheckUserLock - check if user has lock
func (r *GameRepository) CheckUserLock(userId string) string {
	return r.redisClient.Get(r.ctx, "lock."+userId).Val()
}

// ReleaseUserLock - release lock for user
func (r *GameRepository) ReleaseUserLock(userId string) {
	r.redisClient.Del(r.ctx, "lock."+userId)
}

// AddPlayer - add player to game
func (r *GameRepository) AddPlayer(code string, info *lib.UserInfo) {
	r.redisClient.SAdd(r.ctx, "game."+code+".players", info.Id)
	host, _ := json.Marshal(PlayerInfo{
		Id:     info.Id,
		Email:  info.Email,
		Name:   info.Name,
		IsHost: false,
	})
	r.redisClient.Set(r.ctx, "game."+code+".player."+info.Id, host, time.Hour*24)
}

// GetPlayers - get players in game
func (r *GameRepository) GetPlayers(code string) []PlayerInfo {
	players := r.redisClient.SMembers(r.ctx, "game."+code+".players").Val()
	playersInfo := make([]PlayerInfo, len(players))
	for i, player := range players {
		data := r.redisClient.Get(r.ctx, "game."+code+".player."+player).Val()
		var info PlayerInfo
		_ = json.Unmarshal([]byte(data), &info)
		playersInfo[i] = info
	}
	return playersInfo
}

// IsInGame - check if player is in game
func (r *GameRepository) IsInGame(code string, playerId string) bool {
	res := r.redisClient.SIsMember(r.ctx, "game."+code+".players", playerId).Val()
	return res
}

// GetGame - get game info
func (r *GameRepository) GetGame(code string) (*GamePackage, error) {
	exist := r.redisClient.Exists(r.ctx, "game."+code)
	if exist.Val() == 0 {
		return nil, &GameNotExist{}
	}
	infoObj := r.redisClient.Get(r.ctx, "game."+code)
	var info GameInfo
	err := json.Unmarshal([]byte(infoObj.Val()), &info)
	if err != nil {
		return nil, err
	}
	status := r.GetStatus(code)
	return &GamePackage{
		Info:    info,
		Players: r.GetPlayers(code),
		Status:  status,
	}, nil
}

// ChangeStatus - change status of game
func (r *GameRepository) ChangeStatus(code string, status string) {
	r.redisClient.Set(r.ctx, "game."+code+".status", status, redis.KeepTTL)
}

// GetStatus - get status of game
func (r *GameRepository) GetStatus(code string) string {
	return r.redisClient.Get(r.ctx, "game."+code+".status").Val()
}

// IsUserHost - check if user is host
func (r *GameRepository) IsUserHost(code string, userId string) bool {
	data := r.redisClient.Get(r.ctx, "game."+code+".player."+userId).Val()
	var info PlayerInfo
	_ = json.Unmarshal([]byte(data), &info)
	return info.IsHost
}

// RemoveUser - remove user from game
func (r *GameRepository) RemoveUser(code string, userId string) {
	r.redisClient.SRem(r.ctx, "game."+code+".players", userId)
	r.redisClient.Del(r.ctx, "game."+code+".player."+userId)
	r.redisClient.Del(r.ctx, "game."+code+".likes."+userId)
	r.redisClient.Del(r.ctx, "game."+code+".movies."+userId)
	r.ReleaseUserLock(userId)
}

// DeleteGame - delete game
func (r *GameRepository) DeleteGame(code string) {
	players := r.redisClient.SMembers(r.ctx, "game."+code+".players").Val()
	for _, player := range players {
		r.redisClient.Del(r.ctx, "game."+code+".player."+player)
		r.redisClient.Del(r.ctx, "game."+code+".likes."+player)
		r.redisClient.Del(r.ctx, "game."+code+".movies."+player)
		r.ReleaseUserLock(player)
	}
	r.redisClient.Del(r.ctx, "game."+code+".players")
	r.redisClient.Set(r.ctx, "game."+code+".status", StatusDeleted, time.Hour*24)

}

// AddMovie - add movies to player's roster
func (r *GameRepository) AddMovie(code string, playerId string, movie int) {
	exist := r.redisClient.Exists(r.ctx, "game."+code+".movies."+playerId).Val()
	r.redisClient.SAdd(r.ctx, "game."+code+".movies."+playerId, strconv.Itoa(movie))
	if exist == 0 {
		r.redisClient.Expire(r.ctx, "game."+code+".movies."+playerId, 24*time.Hour)
	}
}

// RemoveMovie - remove movie from player's roster
func (r *GameRepository) RemoveMovie(code string, playerId string, movie int) {
	r.redisClient.SRem(r.ctx, "game."+code+".movies."+playerId, strconv.Itoa(movie))
}

// GetMovies - get movies from player's roster
func (r GameRepository) GetMovies(code string, playerId string) []int {
	movies := r.redisClient.SMembers(r.ctx, "game."+code+".movies."+playerId).Val()
	moviesInt := make([]int, len(movies))
	for i, movie := range movies {
		movieInt, _ := strconv.Atoi(movie)
		moviesInt[i] = movieInt
	}
	return moviesInt
}

// AddLike - add like to movie
func (r *GameRepository) AddLike(code string, playerId string, movieId int) error {
	exist := r.redisClient.Exists(r.ctx, "game."+code+".likes."+playerId).Val()
	r.redisClient.SAdd(r.ctx, "game."+code+".likes."+playerId, movieId)
	if exist == 0 {
		r.redisClient.Expire(r.ctx, "game."+code+".likes."+playerId, time.Hour*24)
	}
	return nil
}
