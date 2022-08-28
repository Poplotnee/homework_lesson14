from flask import Blueprint

from utils import search_by_title, search_by_two_years, search_by_rating, search_by_genre

main_blueprint = Blueprint('main_blueprint', __name__)


@main_blueprint.route('/movie/<title>')
def search_by_title_page(title):
    return search_by_title(title)


@main_blueprint.route('/movie/<year_1>/to/<year_2>')
def search_by_years_page(year_1, year_2):
    return search_by_two_years(year_1, year_2)


@main_blueprint.route('/rating/<rating>')
def search_by_rating_page(rating):
    return search_by_rating(rating)


@main_blueprint.route('/genre/<genre>')
def search_by_genre_page(genre):
    return search_by_genre(genre)
