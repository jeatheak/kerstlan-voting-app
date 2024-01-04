# database.py
import sqlite3
import os
from config import database_path

DB_NAME = database_path

def create_tables():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS games (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                description TEXT,
                link TEXT,
                image_path TEXT
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS riddles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                riddle TEXT,
                hint TEXT,
                answer TEXT,
                used_hints INTEGER,
                username TEXT,
                solved INTEGER
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_ratings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT,
                game_id INTEGER,
                rating INTEGER,
                FOREIGN KEY (game_id) REFERENCES games(id)
            )
        ''')

def add_game(name, description, link, image_path):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO games (name, description, link, image_path)
            VALUES (?, ?, ?, ?)
        ''', (name, description, link, image_path))

def get_games():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM games')
        games = cursor.fetchall()
    return games

def get_riddles():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM riddles')
        riddles = cursor.fetchall()
    return riddles

def add_riddle_hint(riddle_id, used_hints: int):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    used_hints += 1

    # Update other game details
    cursor.execute('''
        UPDATE riddles
        SET used_hints=?
        WHERE id=?
    ''', (used_hints, riddle_id))

    conn.commit()
    conn.close()

def add_riddle_answer(riddle_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    solved = 1

    # Update other game details
    cursor.execute('''
        UPDATE riddles
        SET solved=?
        WHERE id=?
    ''', (solved,riddle_id))

    conn.commit()
    conn.close()

def delete_game(name):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM games WHERE name = ?', (name,))
    conn.commit()
    conn.close()

def delete_riddle(id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM riddles WHERE id = ?', (id,))
    conn.commit()
    conn.close()

def update_game(name, new_name, new_description, new_link, new_image_path=None):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Check if a new image is provided
    if new_image_path:
        # Remove the old image file if it exists
        cursor.execute('SELECT image_path FROM games WHERE name=?', (name,))
        old_image_path = cursor.fetchone()[0]
        if old_image_path and os.path.exists(old_image_path):
            os.remove(old_image_path)

        # Update the image path in the database
        cursor.execute('''
            UPDATE games
            SET image_path=?
            WHERE name=?
        ''', (new_image_path, name))

    # Update other game details
    cursor.execute('''
        UPDATE games
        SET name=?, description=?, link=?
        WHERE name=?
    ''', (new_name, new_description, new_link, name))

    conn.commit()
    conn.close()

def update_riddle(id, new_name, new_riddle, new_hint, new_answer, used_hints, new_username, solved):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Update other game details
    cursor.execute('''
        UPDATE riddles
        SET name=?, riddle=?, hint=?, answer=?, used_hints=?, username=?, solved=?
        WHERE id=?
    ''', (new_name, new_riddle, new_hint, new_answer, used_hints, new_username, solved, id))

    conn.commit()
    conn.close()

def add_user_rating(username, game_id, rating):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO user_ratings (username, game_id, rating)
        VALUES (?, ?, ?)
    ''', (username, game_id, rating))
    conn.commit()
    conn.close()

def add_riddle(name, riddle, hint, answer, username):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO riddles (name, riddle, hint, answer, username, used_hints, solved)
        VALUES (?, ?, ?, ?, ?, 0, false)
    ''', (name, riddle, hint, answer, username))
    conn.commit()
    conn.close()

def get_ratings_for_game(game_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT rating FROM user_ratings WHERE game_id = ?', (game_id,))
    ratings = cursor.fetchall()
    conn.close()

    return [rating[0] for rating in ratings]

def get_user_ratings_for_game(game_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT username, rating FROM user_ratings WHERE game_id = ?', (game_id,))
    ratings = cursor.fetchall()
    conn.close()

    return ratings


def get_rated_users_for_game(game_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT username FROM user_ratings WHERE game_id = ?', (game_id,))
    ratings = cursor.fetchall()
    conn.close()

    return [rating[0] for rating in ratings]

def get_users():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT DISTINCT username FROM user_ratings')
    users = cursor.fetchall()
    conn.close()

    return users

def has_user_voted(username, game_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM user_ratings WHERE username = ? AND game_id = ?', (username, game_id))
    result = cursor.fetchone()
    conn.close()

    if result == None:
        return None, None

    return result is not None, result[3]

def update_user_rating(username, game_id, rating):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('UPDATE user_ratings SET rating = ? WHERE username = ? AND game_id = ?', (rating, username, game_id))
    conn.commit()
    conn.close()