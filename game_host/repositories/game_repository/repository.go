package game_repository

import (
	"context"
	"game_host/lib"
	"github.com/redis/go-redis/v9"
	"os"
	"strconv"
)

type GameRepository struct {
	ctx         context.Context
	redisClient *redis.Client
}

func NewGameRepository() *GameRepository {
	db, err := strconv.Atoi(lib.GetEnv("REDIS_DB", "0"))
	if err != nil {
		panic(err)
	}
	return &GameRepository{
		ctx: context.Background(),
		redisClient: redis.NewClient(
			&redis.Options{
				Addr:     os.Getenv("REDIS_ADDR"),
				Password: lib.GetEnv("REDIS_PASSWORD", ""),
				DB:       db,
			},
		),
	}
}
