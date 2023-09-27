from flask import flash, redirect, render_template, Response

from yacut import BASE_URL, app, db
from yacut.error_handlers import check_inique_short_url
from yacut.forms import URLForm
from yacut.models import URLMap
from yacut.utils import check_symbols, get_unique_short_url


@app.route('/', methods=('GET', 'POST',))
def main_page_view() -> str:
    form = URLForm()
    if not form.validate_on_submit():
        return render_template('main_page.html', form=form)
    original_link = form.original_link.data
    custom_id = form.custom_id.data
    if check_inique_short_url(custom_id):
        flash(f'Имя {custom_id} уже занято!')
        return render_template('main_page.html', form=form)
    if custom_id and not check_symbols(custom_id):
        flash('Допустимые символы: A-z, 0-9')
        return render_template('main_page.html', form=form)

    if custom_id is None:
        custom_id = get_unique_short_url()

    url = URLMap(
        original=original_link,
        short=custom_id,
    )
    db.session.add(url)
    db.session.commit()
    return render_template('main_page.html',
                           form=form,
                           short_url=BASE_URL + url.short,
                           original_link=url.original)


@app.route('/<string:short>', methods=('GET',))
def redirect_to_url_view(short: str) -> Response:
    url = URLMap.query.filter_by(short=short).first_or_404()
    return redirect(url.original)