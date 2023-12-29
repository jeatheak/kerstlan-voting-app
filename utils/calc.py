from database.database import get_rated_users_for_game, get_ratings_for_game


def calculate_total_rating_for_game(game_id):
    ratings = get_ratings_for_game(game_id)
    
    if ratings:
        total_sum = sum(ratings)
        total_count = len(ratings)
        return total_sum / total_count

    return 0

def get_voted_users(game_id):
    users = get_rated_users_for_game(game_id)
    if users:
        return users

    return []