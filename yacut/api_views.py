from http import HTTPStatus
from typing import Tuple
from flask import jsonify, request, Responce

from yacut import app, db
from yacut.error_handlers import InvalidAPIUsage, check_inique_short_url
from yacut.models import URLMap
from yacut.utils import check_symbols, get_unique_short_url
from yacut.settings import MAX_LENGTH


@app.route('/api/id/', methods=('POST',))
def add_url() -> Tuple[Responce, int]:
    data = request.get_json()
    if not data:
        raise InvalidAPIUsage('Отсутствует тело запроса', HTTPStatus.BAD_REQUEST)
    if 'url' not in data:
        raise InvalidAPIUsage('"url" является обязательным полем!')
    if 'custom_id' not in data or data['custom_id'] is None:
        data['custom_id'] = get_unique_short_url()
    custom_id = data['custom_id']
    if len(custom_id) > MAX_LENGTH or not check_symbols(custom_id):
        raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки')
    if check_inique_short_url(custom_id):
        raise InvalidAPIUsage(f'Имя "{custom_id}" уже занято.')
    url = URLMap()
    url.from_dict(data)
    db.session.add(url)
    db.session.commit()
    return jsonify(url.to_dict()), HTTPStatus.CREATED


@app.route('/api/id/<string:short_id>/', methods=('GET',))
def get_original_url(short_id: str) -> Responce:
    url = URLMap.query.filter_by(short=short_id).first()
    if not url:
        raise InvalidAPIUsage('Указанный id не найден', HTTPStatus.NOT_FOUND)
    return jsonify({'url': url.original})