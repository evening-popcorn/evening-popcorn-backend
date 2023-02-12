FROM python:3.11
WORKDIR /app
COPY ./ /app

RUN curl -sSL https://install.python-poetry.org | python3 -
RUN /root/.local/bin/poetry install --no-interaction --no-ansi -vvv

CMD python src/main.py