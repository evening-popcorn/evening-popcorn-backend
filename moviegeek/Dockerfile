FROM python:3.11
WORKDIR /app
COPY ./ /app

RUN curl -sSL https://install.python-poetry.org | python3 -
RUN /root/.local/bin/poetry config virtualenvs.create false
RUN /root/.local/bin/poetry install

EXPOSE 8080
CMD python api_gateway/main.py