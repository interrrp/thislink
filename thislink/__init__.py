from http import HTTPStatus
from secrets import token_urlsafe
from typing import Annotated, Any

from fastapi import FastAPI, Form, Request, Response
from fastapi.exceptions import RequestValidationError
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import HttpUrl

app = FastAPI()
templates = Jinja2Templates(directory="templates")
links: dict[str, str] = {}


@app.get("/")
def index(request: Request) -> Response:
    return render_template(request, "index")


@app.get("/{link_id}")
def get(request: Request, link_id: str) -> Response:
    try:
        return RedirectResponse(links[link_id], HTTPStatus.SEE_OTHER)
    except KeyError:
        return render_template(request, "index", {"error": "Unknown link"})


@app.post("/")
def create(request: Request, url: Annotated[HttpUrl, Form(embed=True)]) -> Response:
    link_id = token_urlsafe(6)
    links[link_id] = str(url)
    return render_template(request, "index", {"shortened": f"/{link_id}"})


@app.exception_handler(RequestValidationError)
def handle_validation_error(request: Request, exception: RequestValidationError) -> Response:
    error_str = ""
    for err in exception.errors():
        error_str += f"{err['msg']}\n"
    return render_template(request, "index", {"error": error_str})


def render_template(
    request: Request,
    name: str,
    context: dict[str, Any] | None = None,
) -> Response:
    return templates.TemplateResponse(request, f"{name}.html.jinja", context)
