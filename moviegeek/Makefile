build-image:
	docker build -t moviegeek:latest .
	docker image tag  moviegeek:latest registry.digitalocean.com/moviegeek:latest
	docker push registry.digitalocean.com/evening-popcorn-registry/moviegeek:latest

deploy:
	kubectl apply -f deploy/deploy.yaml
