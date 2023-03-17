package repositories

import (
	"context"
	"encoding/json"
	"game_host/lib"
	"github.com/redis/go-redis/v9"
	"os"
	"strconv"
	"time"
)

var ctx = context.Background()

type GameRepository struct {
	redisClient *redis.Client
}

func NewGameRepository() *GameRepository {
	db, err := strconv.Atoi(lib.GetEnv("REDIS_DB", "0"))
	if err != nil {
		panic(err)
	}
	return &GameRepository{
		redisClient: redis.NewClient(
			&redis.Options{
				Addr:     os.Getenv("REDIS_ADDR"),
				Password: lib.GetEnv("REDIS_PASSWORD", ""),
				DB:       db,
			},
		),
	}
}

type GameInfo struct {
	Code     string       `json:"id"`
	Host     lib.UserInfo `json:"host"`
	Name     string       `json:"name"`
	CreateAt string       `json:"createAt"`
}

type GameStatus string

type GamePackage struct {
	Info    GameInfo
	Players []string
	Status  GameStatus
}

type GameNotExist struct {
}

func (e *GameNotExist) Error() string {
	return "Game does not exist"
}

func (r *GameRepository) CreateGame(info *lib.UserInfo, name string) GameInfo {
	var code string
	for {
		code = lib.GenerateRandString(8)
		exist := r.redisClient.Exists(ctx, "game."+code)
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
	r.redisClient.Set(ctx, "game."+code, obj, time.Hour*24)

	r.redisClient.SAdd(ctx, "game."+code+".players", info.Id)
	r.redisClient.Expire(ctx, "game."+code+".players", time.Hour*24)

	r.redisClient.Set(ctx, "game."+code+".status", "Created", time.Hour*24)
	return gameInfo
}

func (r *GameRepository) GetGame(code string) (*GamePackage, error) {
	exist := r.redisClient.Exists(ctx, "game."+code)
	if exist.Val() == 0 {
		return nil, &GameNotExist{}
	}
	info_obj := r.redisClient.Get(ctx, "game."+code)
	var info GameInfo
	//fmt.Println(info_obj.Val())
	err := json.Unmarshal([]byte(info_obj.Val()), &info)
	if err != nil {
		return nil, err
	}
	players := r.redisClient.SMembers(ctx, "game."+code+".players")
	status := r.redisClient.Get(ctx, "game."+code+".status").Val()
	if err != nil {
		return nil, err
	}
	return &GamePackage{
		Info:    info,
		Players: players.Val(),
		Status:  GameStatus(status),
	}, nil
}

func (r *GameRepository) ChangeStatus(code string, status string) {
	r.redisClient.Set(ctx, "game."+code+".status", status, redis.KeepTTL)
}

func (r GameRepository) GetStatus(code string) string {
	return r.redisClient.Get(ctx, "game."+code+".status").Val()
}

func (r GameRepository) AddLike(code string, playerId string, movieId int) error {
	exist := r.redisClient.Exists(ctx, "game."+code+".likes."+playerId).Val()
	r.redisClient.SAdd(ctx, "game."+code+".likes."+playerId, movieId)
	if exist == 0 {
		r.redisClient.Expire(ctx, "game."+code+".likes."+playerId, time.Hour*24)
	}
	return nil
}
