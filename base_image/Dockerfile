FROM python:3.11
COPY ep_client /lib/ep_client
COPY ep_utils /lib/ep_client
RUN pip install poetry
RUN poetry config virtualenvs.create false

RUN cd /lib/ep_client && poetry install
RUN pip install /lib/ep_client

RUN cd /lib/ep_utils && poetry install
RUN pip install /lib/ep_utils