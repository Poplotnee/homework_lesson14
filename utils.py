import sqlite3
import json


def search_by_title(query_title: str) -> json:
    con = sqlite3.connect("netflix.db")
    cur = con.cursor()
    sqlite_query = (f"""
        SELECT title, country, release_year, listed_in, description
        FROM netflix
        WHERE "title" LIKE "%{query_title}%"
        ORDER BY release_year DESC
        LIMIT 1
                    """)
    cur.execute(sqlite_query)
    executed_query = cur.fetchall()
    if executed_query == []:
        return 'По данному запросу ничего не найдено'
    executed_query = next(iter(executed_query))
    executed_query_dict = {
        "title": executed_query[0],
        "country": executed_query[1],
        "release_year": executed_query[2],
        "genre": executed_query[3],
        "description": executed_query[4]
    }
    executed_query_json = json.dumps(executed_query_dict)
    return executed_query_json


def search_by_two_years(year_1: int, year_2: int) -> json:
    con = sqlite3.connect("netflix.db")
    cur = con.cursor()
    sqlite_query = (f"""
        SELECT title, release_year
        FROM netflix
        WHERE {year_1} <= release_year <= {year_2}
        AND type = 'Movie'
        LIMIT 100;
                    """)
    cur.execute(sqlite_query)
    executed_query = cur.fetchall()
    list_films_in_range_years = []
    for film in executed_query:
        list_films_in_range_years.append({"title": film[0], "release_year": film[1]})
    executed_query_json = json.dumps(list_films_in_range_years)
    return executed_query_json


def search_by_rating(rating: str) -> json:
    if rating == 'children':
        rating = ('G', 'что бы работало')
    elif rating == 'family':
        rating = ('G', 'PG', 'PG-13')
    elif rating == 'adult':
        rating = ('R', 'NC-17')
    else:
        return 'нет такого рейтинга'

    con = sqlite3.connect("netflix.db")
    cur = con.cursor()
    sqlite_query = (f"""
        SELECT title, rating, description
        FROM netflix
        WHERE rating IN {rating};
                    """)
    cur.execute(sqlite_query)
    executed_query = cur.fetchall()
    rating_list_films = []
    for film in executed_query:
        rating_list_films.append({"title": film[0], "rating": film[1], "description": film[2]})
    executed_query_json = json.dumps(rating_list_films)
    return executed_query_json


def search_by_genre(genre: str) -> json:
    con = sqlite3.connect("netflix.db")
    cur = con.cursor()
    sqlite_query = (f"""
        SELECT title, description
        FROM netflix
        WHERE listed_in LIKE '%{genre}%'
        ORDER BY release_year DESC
        LIMIT 10;
                    """)
    cur.execute(sqlite_query)
    executed_query = cur.fetchall()
    genre_list_films = []
    for film in executed_query:
        genre_list_films.append({"title": film[0], "description": film[1]})
    executed_query_json = json.dumps(genre_list_films)
    return executed_query_json


def plays_with_them_more_than_twice(actor_1: str, actor_2: str) -> list:
    con = sqlite3.connect("netflix.db")
    cur = con.cursor()
    sqlite_query = (f"""
        SELECT "cast"
        FROM netflix
        WHERE "cast" LIKE '%{actor_1}%'
        OR "cast" LIKE '%{actor_2}';
                    """)
    cur.execute(sqlite_query)
    executed_query = cur.fetchall()
    list_actors = []
    for actors in executed_query:
        if len(actors) > 0:
            list_actors.append(*actors)
    list_actors_2 = []
    for actors in list_actors:
        if len(actors) > 0:
            for actor in actors.split(', '):
                list_actors_2.append(actor)
    list_actors_more_2 = []
    for actor in list_actors_2:
        if list_actors_2.count(actor) > 2 and actor != actor_1 \
                and actor != actor_2 and actor not in list_actors_more_2:
            list_actors_more_2.append(actor)

    return list_actors_more_2


# print(plays_with_them_more_than_twice('Rose McIver', 'Ben Lamb'))
# print(plays_with_them_more_than_twice('Jack Black', 'Dustin Hoffman'))

def search_by_multiple_parameters(type: str, year: int, genre: str) -> json:
    con = sqlite3.connect("netflix.db")
    cur = con.cursor()
    sqlite_query = (f"""
        SELECT title, description
        FROM netflix
        WHERE type LIKE '%{type}%'
        AND release_year LIKE '%{year}%'
        AND listed_in LIKE '%{genre}%';
                    """)
    cur.execute(sqlite_query)
    executed_query = cur.fetchall()
    multiple_parameters_list_films = []
    for film in executed_query:
        multiple_parameters_list_films.append({"title": film[0], "description": film[1]})
    executed_query_json = json.dumps(multiple_parameters_list_films)
    return executed_query_json

# print(search_by_multiple_parameters('Movie', 1998, 'Dramas'))
