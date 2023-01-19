# pylint: disable=C0103, missing-docstring

def detailed_movies(db):
    '''return the list of movies with their genres and director name'''
    query = """SELECT movies.title, movies.genres, directors.name
            FROM movies
            JOIN directors ON movies.director_id = directors.id"""
    db.execute(query)
    movies = db.fetchall()
    return movies


def late_released_movies(db):
    '''return the list of all movies released after their director death'''
    query = """SELECT movies.title FROM movies
            JOIN directors ON movies.director_id = directors.id
            WHERE movies.start_year > directors.death_year"""
    db.execute(query)
    they_died = db.fetchall()
    return [d[0] for d in they_died]

def stats_on(db, genre_name):
    '''return a dict of stats for a given genre'''
    query = f"""SELECT genres, COUNT(*), ROUND(AVG(minutes),2)
            FROM movies
            WHERE genres LIKE '{genre_name}'"""
    db.execute(query)
    genre_stats = db.fetchone()
    return dict(genre = genre_stats[0],
                number_of_movies =  genre_stats[1],
                avg_length = genre_stats[2])


def top_five_directors_for(db, genre_name):
    '''return the top 5 of the directors with the most movies for a given genre'''
    query = f"""SELECT directors.name, COUNT(movies.genres) FROM movies
            JOIN directors ON movies.director_id = directors.id
            WHERE movies.genres LIKE '{genre_name}'
            GROUP BY directors.name
            ORDER BY COUNT(movies.genres) DESC, directors.name ASC"""
    db.execute(query)
    top_five = db.fetchmany(5)
    return top_five

def movie_duration_buckets(db):
    '''return the movie counts grouped by bucket of 30 min duration'''
    query = """SELECT 30*CAST(minutes/30 AS INTEGER)+30 AS bin, COUNT(*)
        FROM movies
        WHERE minutes IS NOT NULL
        GROUP BY bin"""
    db.execute(query)
    bins = db.fetchall()
    return bins

def top_five_youngest_newly_directors(db):
    '''return the top 5 youngest directors when they direct their first movie'''
    query = """SELECT directors.name, (movies.start_year-directors.birth_year) AS age
        FROM directors
        JOIN movies ON directors.id = movies.director_id
        WHERE directors.birth_year IS NOT NULL
        ORDER BY age ASC"""
    db.execute(query)
    younglings = db.fetchmany(5)
    return younglings
