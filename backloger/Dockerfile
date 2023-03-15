FROM registry.digitalocean.com/evening-popcorn-registry/ep-base:latest
WORKDIR /app
COPY ./ /app

RUN poetry install

EXPOSE 8082
CMD python -m backloger.main