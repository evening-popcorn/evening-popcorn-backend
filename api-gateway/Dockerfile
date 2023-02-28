FROM python:3.11
WORKDIR /app
COPY ./ /app

RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-root

CMD python -m api_gateway.main