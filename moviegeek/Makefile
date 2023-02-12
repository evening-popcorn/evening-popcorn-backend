build-image:
	docker build -t moviegeek:latest .
	docker image tag moviegeek:latest registry.digitalocean.com/evening-popcorn-registry/moviegeek:latest
	docker push registry.digitalocean.com/evening-popcorn-registry/moviegeek:latest
build-on-arm:
	docker buildx create --use
	docker buildx build --platform linux/amd64 --push -t registry.digitalocean.com/evening-popcorn-registry/moviegeek:latest .

deploy:
	kubectl apply -f deploy/deploy.yaml
