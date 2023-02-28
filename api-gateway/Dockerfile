FROM registry.digitalocean.com/evening-popcorn-registry/ep-base:latest
WORKDIR /app
COPY ./ /app

RUN poetry install --no-root

CMD python -m api_gateway.main