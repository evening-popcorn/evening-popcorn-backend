package game_repository

import (
	"encoding/json"
	"game_host/lib"
	"github.com/redis/go-redis/v9"
	"time"
)

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

func (r *GameRepository) CreateUserLock(userId string, code string) {
	r.redisClient.Set(r.ctx, "lock."+userId, code, 24*time.Hour)
}

func (r *GameRepository) CheckUserLock(userId string) string {
	return r.redisClient.Get(r.ctx, "lock."+userId).Val()
}

func (r *GameRepository) ReleaseUserLock(userId string) {
	r.redisClient.Del(r.ctx, "lock."+userId)
}

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
func (r *GameRepository) IsInGame(code string, playerId string) bool {
	res := r.redisClient.SIsMember(r.ctx, "game."+code+".players", playerId).Val()
	return res
}

func (r *GameRepository) GetGame(code string) (*GamePackage, error) {
	exist := r.redisClient.Exists(r.ctx, "game."+code)
	if exist.Val() == 0 {
		return nil, &GameNotExist{}
	}
	infoObj := r.redisClient.Get(r.ctx, "game."+code)
	var info GameInfo
	//fmt.Println(info_obj.Val())
	err := json.Unmarshal([]byte(infoObj.Val()), &info)
	if err != nil {
		return nil, err
	}
	status := r.redisClient.Get(r.ctx, "game."+code+".status").Val()
	return &GamePackage{
		Info:    info,
		Players: r.GetPlayers(code),
		Status:  status,
	}, nil
}

func (r *GameRepository) ChangeStatus(code string, status string) {
	r.redisClient.Set(r.ctx, "game."+code+".status", status, redis.KeepTTL)
}

func (r *GameRepository) GetStatus(code string) string {
	return r.redisClient.Get(r.ctx, "game."+code+".status").Val()
}

func (r *GameRepository) IsUserHost(code string, userId string) bool {
	data := r.redisClient.Get(r.ctx, "game."+code+".player."+userId).Val()
	var info PlayerInfo
	_ = json.Unmarshal([]byte(data), &info)
	return info.IsHost
}

func (r *GameRepository) RemoveUser(code string, userId string) {

}

func (r *GameRepository) DeleteGame(code string) {
	r.redisClient.Del(r.ctx, "game."+code)
	players := r.redisClient.SMembers(r.ctx, "game."+code+".players").Val()
	for _, player := range players {
		r.redisClient.Del(r.ctx, "game."+code+".player."+player).Val()
		r.ReleaseUserLock(player)
	}
	r.redisClient.Del(r.ctx, "game."+code+".players")
	r.redisClient.Del(r.ctx, "game."+code+".status")

}

func (r *GameRepository) AddLike(code string, playerId string, movieId int) error {
	exist := r.redisClient.Exists(r.ctx, "game."+code+".likes."+playerId).Val()
	r.redisClient.SAdd(r.ctx, "game."+code+".likes."+playerId, movieId)
	if exist == 0 {
		r.redisClient.Expire(r.ctx, "game."+code+".likes."+playerId, time.Hour*24)
	}
	return nil
}
