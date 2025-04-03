FROM python:3.13-alpine
WORKDIR /app
RUN pip install uv
COPY pyproject.toml .
RUN uv sync
COPY . .
ENV THISLINK_PORT 8000
EXPOSE ${THISLINK_PORT}
CMD [ "sh", "-c", "uv run fastapi run thislink --port ${THISLINK_PORT}" ]
