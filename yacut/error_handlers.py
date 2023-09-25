from http import HTTPStatus

from flask import jsonify, render_template
from typing import Union

from yacut import app
from models import URLMap


class InvalidAPIUsage(Exception):
    status_code = HTTPStatus.BAD_REQUEST

    def __init__(self, message: str, status_code: int = None) -> None:
        super().__init__()
        self.message = message
        if status_code is not None:
            self.status_code = status_code

    def to_dict(self) -> dict:
        return dict(message=self.message)


@app.errorhandler(InvalidAPIUsage)
def invalid_api_usage(error: InvalidAPIUsage) -> tuple:
    return jsonify(error.to_dict()), error.status_code


@app.errorhandler(HTTPStatus.NOT_FOUND)
def page_not_found(error: HTTPStatus) -> tuple:
    return render_template('404.html'), HTTPStatus.NOT_FOUND


def check_inique_short_url(custom_id: str) -> Union[str, None]:
    if URLMap.query.filter_by(short=custom_id).first():
        return custom_id
    return None