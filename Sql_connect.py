import mysql.connector
from mysql.connector import Error
from werkzeug.security import generate_password_hash, check_password_hash

# Database connection configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '123456',
    'database': 'cyber_checker'
}

# Establish database connection
def create_db_connection():
    try:
        connection = mysql.connector.connect(
            host=db_config['host'],
            user=db_config['user'],
            password=db_config['password']
        )
        if connection.is_connected():
            print("Successfully connected to MySQL database")
            return connection
    except Error as e:
        print(f"Database connection failed: {e}")
        return None

# Create or modify database and tables
def initialize_database():
    connection = create_db_connection()
    if connection:
        cursor = connection.cursor()
        try:
            # Create database
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_config['database']}")
            print(f"Database {db_config['database']} created or already exists.")

            # Select database
            connection.database = db_config['database']

            # Create Users table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS Users (
                user_id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) NOT NULL UNIQUE,
                password VARCHAR(255) NOT NULL,
                total_games INT DEFAULT 0,
                wins INT DEFAULT 0,
                losses INT DEFAULT 0,
                win_rate DECIMAL(5,2) AS (CASE WHEN total_games > 0 THEN (wins / total_games) * 100 ELSE 0 END) STORED,
                registration_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                last_login DATETIME DEFAULT NULL
            ) ENGINE=InnoDB;
            """)

            # Create Games table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS Games (
                game_id INT AUTO_INCREMENT PRIMARY KEY,
                player1_id INT NOT NULL,
                player2_id INT NOT NULL,
                winner_id INT,
                player1_score INT DEFAULT 0,  -- Player 1 score
                player2_score INT DEFAULT 0,  -- Player 2 score
                start_time DATETIME DEFAULT CURRENT_TIMESTAMP,
                end_time DATETIME DEFAULT NULL,
                FOREIGN KEY (player1_id) REFERENCES Users(user_id),
                FOREIGN KEY (player2_id) REFERENCES Users(user_id),
                FOREIGN KEY (winner_id) REFERENCES Users(user_id)
            ) ENGINE=InnoDB;
            """)

            # Create Game_Moves table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS Game_Moves (
                move_id INT AUTO_INCREMENT PRIMARY KEY,
                game_id INT NOT NULL,
                move_number INT NOT NULL,
                player_id INT NOT NULL,
                from_row INT NOT NULL,
                from_col INT NOT NULL,
                to_row INT NOT NULL,
                to_col INT NOT NULL,
                player1_score INT DEFAULT 0,  -- Player 1 score
                player2_score INT DEFAULT 0,  -- Player 2 score
                move_time DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (game_id) REFERENCES Games(game_id),
                FOREIGN KEY (player_id) REFERENCES Users(user_id),
                INDEX idx_game_move (game_id, move_number)
            ) ENGINE=InnoDB;
            """)

            print("All tables created or already exist.")

        except Error as e:
            print(f"Database initialization failed: {e}")
        finally:
            cursor.close()
            connection.close()

# Establish database connection (with database)
def get_db_connection():
    try:
        connection = mysql.connector.connect(**db_config)
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Database connection failed: {e}")
        return None

# Insert new user
def insert_user(username, password):
    connection = get_db_connection()
    if connection:
        cursor = connection.cursor()
        try:
            sql = "INSERT INTO Users (username, password) VALUES (%s, %s)"
            values = (username, password)
            cursor.execute(sql, values)
            connection.commit()
            print(f"User {username} successfully registered.")
        except Error as e:
            print(f"Failed to insert user: {e}")
        finally:
            cursor.close()
            connection.close()

# Get user information
def get_user_by_username(username):
    connection = get_db_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)
        try:
            sql = "SELECT * FROM Users WHERE username = %s"
            cursor.execute(sql, (username,))
            user = cursor.fetchone()
            return user
        except Error as e:
            print(f"Failed to query user: {e}")
            return None
        finally:
            cursor.close()
            connection.close()

# User registration
def register_user(username, password):
    # Generate password hash
    password_hash = generate_password_hash(password)
    # Insert new user
    insert_user(username, password_hash)

# User login
def login_user(username, password):
    user = get_user_by_username(username)
    if user and check_password_hash(user['password'], password):
        print(f"User {username} logged in successfully!")
        # Update last login time
        connection = get_db_connection()
        if connection:
            cursor = connection.cursor()
            try:
                cursor.execute("UPDATE Users SET last_login = NOW() WHERE user_id = %s", (user['user_id'],))
                connection.commit()
            except Error as e:
                print(f"Failed to update last login time: {e}")
            finally:
                cursor.close()
                connection.close()
        return user
    else:
        print("Username or password incorrect!")
        return None

# Insert new game
def insert_game(player1_id, player2_id):
    connection = get_db_connection()
    if connection:
        cursor = connection.cursor()
        try:
            sql = "INSERT INTO Games (player1_id, player2_id) VALUES (%s, %s)"
            values = (player1_id, player2_id)
            cursor.execute(sql, values)
            connection.commit()
            game_id = cursor.lastrowid
            print(f"New game created, game ID is {game_id}.")
            return game_id
        except Error as e:
            print(f"Failed to insert game: {e}")
            return None
        finally:
            cursor.close()
            connection.close()

# Start a new game
def start_new_game(player1_username, player2_username):
    player1 = get_user_by_username(player1_username)
    player2 = get_user_by_username(player2_username)
    if player1 and player2:
        game_id = insert_game(player1['user_id'], player2['user_id'])
        return game_id
    else:
        print("Unable to start game, user does not exist.")
        return None

# Insert game move with player scores
def insert_game_move(game_id, move_number, player_id, from_row, from_col, to_row, to_col, player1_score, player2_score):
    connection = get_db_connection()
    if connection:
        cursor = connection.cursor()
        try:
            sql = """
            INSERT INTO Game_Moves
            (game_id, move_number, player_id, from_row, from_col, to_row, to_col, player1_score, player2_score)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            values = (game_id, move_number, player_id, from_row, from_col, to_row, to_col, player1_score, player2_score)
            cursor.execute(sql, values)
            connection.commit()
            print(f"Recorded move {move_number} in game {game_id} with scores: Player 1 = {player1_score}, Player 2 = {player2_score}.")
        except Error as e:
            print(f"Failed to insert move: {e}")
        finally:
            cursor.close()
            connection.close()

# Record move with updated scores
def record_move(game_id, move_number, player_username, from_row, from_col, to_row, to_col, player1_score, player2_score):
    player = get_user_by_username(player_username)
    if player:
        insert_game_move(game_id, move_number, player['user_id'], from_row, from_col, to_row, to_col, player1_score, player2_score)
    else:
        print("Unable to record move, user does not exist.")

# Update game result
def update_game_result(game_id, winner_id):
    connection = get_db_connection()
    if connection:
        cursor = connection.cursor()
        try:
            sql = "UPDATE Games SET winner_id = %s, end_time = NOW() WHERE game_id = %s"
            cursor.execute(sql, (winner_id, game_id))
            connection.commit()
            print(f"Game {game_id} ended, winner is user {winner_id}.")
        except Error as e:
            print(f"Failed to update game result: {e}")
        finally:
            cursor.close()
            connection.close()

# Update user statistics
def update_user_stats(user_id, win=False, loss=False):
    connection = get_db_connection()
    if connection:
        cursor = connection.cursor()
        try:
            if win:
                sql = "UPDATE Users SET wins = wins + 1, total_games = total_games + 1 WHERE user_id = %s"
            elif loss:
                sql = "UPDATE Users SET losses = losses + 1, total_games = total_games + 1 WHERE user_id = %s"
            else:
                return
            cursor.execute(sql, (user_id,))
            connection.commit()
            print(f"User {user_id}'s statistics updated.")
        except Error as e:
            print(f"Failed to update user statistics: {e}")
        finally:
            cursor.close()
            connection.close()

# End game
def end_game(game_id, winner_username=None):
    connection = get_db_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)
        try:
            cursor.execute("SELECT player1_id, player2_id FROM Games WHERE game_id = %s", (game_id,))
            game = cursor.fetchone()
            if not game:
                print(f"Game {game_id} does not exist.")
                return

            player1_id = game['player1_id']
            player2_id = game['player2_id']

            if winner_username:
                winner = get_user_by_username(winner_username)
                if winner:
                    winner_id = winner['user_id']
                    update_game_result(game_id, winner_id)
                    # Update statistics for winner and loser
                    loser_id = player2_id if player1_id == winner_id else player1_id
                    update_user_stats(winner_id, win=True)
                    update_user_stats(loser_id, loss=True)
                else:
                    print("Winner username does not exist.")
            else:
                # Draw
                update_game_result(game_id, None)
                # Update total games for both players
                update_user_stats(player1_id)
                update_user_stats(player2_id)
                print(f"Game {game_id} ended in a draw.")
        except Error as e:
            print(f"Failed to end game: {e}")
        finally:
            cursor.close()
            connection.close()

# Get game moves including player scores
def get_game_moves(game_id):
    connection = get_db_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)
        try:
            sql = """
            SELECT move_number, player_id, from_row, from_col, to_row, to_col, player1_score, player2_score, move_time
            FROM Game_Moves
            WHERE game_id = %s
            ORDER BY move_number ASC
            """
            cursor.execute(sql, (game_id,))
            moves = cursor.fetchall()
            print(f"Move records for game {game_id}:")
            for move in moves:
                print(move)
            return moves
        except Error as e:
            print(f"Failed to get game moves: {e}")
            return None
        finally:
            cursor.close()
            connection.close()

# Main program
if __name__ == "__main__":
    # Initialize database
    initialize_database()

    # User registration
    register_user('player1', 'password1')
    register_user('666666', '666666')

    # User login
    alice = login_user('player1', 'password1')
    bob = login_user('666666', '666666')

    if alice and bob:
        # Start a new game
        game_id = start_new_game('player1', '666666')

        if game_id:
            # Record moves (Assume simple scoring system for demo purposes)
            record_move(game_id, 1, 'player1', 1, 0, 2, 0, player1_score=1, player2_score=0)
            record_move(game_id, 2, '666666', 6, 0, 5, 0, player1_score=1, player2_score=1)
            record_move(game_id, 3, 'player1', 1, 1, 3, 1, player1_score=2, player2_score=1)
            record_move(game_id, 4, '666666', 6, 1, 4, 1, player1_score=2, player2_score=2)

            # End game
            end_game(game_id, winner_username='player1')

            # Get game move records with scores
            get_game_moves(game_id)
