package main

import (
	"context"
	"errors"
	"fmt"
	"github.com/joho/godotenv"
	"github.com/redis/go-redis/v9"
	"net/http"
	"os"
	"time"
)

type ResID struct {
	Id string `json:"id"`
}

func main() {
	err := godotenv.Load()
	if err != nil {
		panic(err)
	}

	SetupRouting()

	err = http.ListenAndServe(":8083", nil)
	if errors.Is(err, http.ErrServerClosed) {
		fmt.Printf("server closed\n")
	} else if err != nil {
		fmt.Printf("error starting server: %s\n", err)
		os.Exit(1)
	}
	//repo := rep.NewGameRepository()
	//res := repo.CreateGame(
	//	&lib.UserInfo{Name: "Иван Дмитриев", Id: "123", Email: "van4011@gmail.com"},
	//	"Test",
	//)
	//fmt.Println(res)
	//fmt.Println(repo.GetGame(res.Code))
	//repo.ChangeStatus(res.Code, "Started")
	//repo.AddLike(res.Code, "123", 161)
}

var ctx = context.Background()

func getRoot(w http.ResponseWriter, r *http.Request) {
	rdb := redis.NewClient(&redis.Options{
		Addr:     "localhost:6379",
		Password: "", // no password set
		DB:       0,  // use default DB
	})

	var res *ResID
	for i := 0; i < 100; i++ {
		val := rdb.SInter(ctx, "game1.p1", "game1.p2", "game1.p3").Val()
		skip := rdb.SMembers(ctx, "game1.skip").Val()
		var filtered *string
		for _, id := range val {
			if !inArray(id, skip) {
				filtered = &id
				break
			}
		}
		if filtered == nil {
			time.Sleep(time.Millisecond * 300)
			continue
		}
		res = &ResID{Id: *filtered}
	}
	if res != nil {
		//httpOk(w, *res)
	}
}
func inArray(s string, arr []string) bool {
	for _, a := range arr {
		if s == a {
			return true
		}
	}
	return false
}
