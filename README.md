# Evening Popcorn - Backend

---
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Evening Popcorn(EP) is basically Tinder for movie night. Also, it's allowing to log your backlog.

EP built with microservice structure for better scalability separate parts. 
Everything deployed on DigitalOcean infrastructure, but not depends on it.

**Used technologies**
- Python 3.11
  - [poerty](https://python-poetry.org) 
  - [FastAPI](https://fastapi.tiangolo.com)
  - [tortoise-orm](https://tortoise.github.io)
  - [yoyo](https://ollycope.com/software/yoyo/latest/)
  - [motor](https://motor.readthedocs.io/en/stable/)
  - [dotenv](https://github.com/theskumar/python-dotenv)
- Go
  - net/http
  - dotenv
- Docker + K8s
- PostgreSQL
- MongoDB
- Redis
- GitHub Actions

## Project overview

### API Gateway (api_gateway)