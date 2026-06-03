import os
import pymysql
from datetime import datetime, timedelta
import hashlib
from dotenv import load_dotenv

# Load configuration from .env
load_dotenv()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", 3306))
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "root")
DB_NAME = os.getenv("DB_NAME", "movie_ticketing_db")

STATIC_IMAGES_DIR = os.path.join(os.path.dirname(__file__), 'static', 'images')

def generate_password_hash(password):
    salt = os.urandom(16)
    key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    return f"pbkdf2:sha256:100000${salt.hex()}${key.hex()}"

def init_db():
    # Make sure static directory exists
    os.makedirs(STATIC_IMAGES_DIR, exist_ok=True)
    
    print(f"Connecting to MySQL server at {DB_HOST}:{DB_PORT} as {DB_USER}...")
    
    # Connect without specifying database first to create it
    conn = pymysql.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD
    )
    
    cursor = conn.cursor()
    
    # Create database if not exists
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{DB_NAME}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
    conn.select_db(DB_NAME)
    print(f"Database `{DB_NAME}` selected.")
    
    # Disable foreign keys temporarily to drop tables
    cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
    cursor.execute("DROP TABLE IF EXISTS bookings;")
    cursor.execute("DROP TABLE IF EXISTS showtimes;")
    cursor.execute("DROP TABLE IF EXISTS theatres;")
    cursor.execute("DROP TABLE IF EXISTS movies;")
    cursor.execute("DROP TABLE IF EXISTS users;")
    cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")
    print("Old tables dropped.")

    # Create users table
    cursor.execute("""
    CREATE TABLE users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(255) UNIQUE NOT NULL,
        email VARCHAR(255) UNIQUE NOT NULL,
        password_hash VARCHAR(255) NOT NULL,
        is_admin INT DEFAULT 0
    ) ENGINE=InnoDB;
    """)

    # Create movies table
    cursor.execute("""
    CREATE TABLE movies (
        id INT AUTO_INCREMENT PRIMARY KEY,
        title VARCHAR(255) NOT NULL,
        description TEXT NOT NULL,
        genre VARCHAR(255) NOT NULL,
        duration INT NOT NULL,
        rating FLOAT NOT NULL,
        poster_path VARCHAR(255) NOT NULL,
        language VARCHAR(100) DEFAULT 'English',
        release_status VARCHAR(50) DEFAULT 'Released',
        release_date VARCHAR(50) DEFAULT NULL,
        formats VARCHAR(255) DEFAULT '2D'
    ) ENGINE=InnoDB;
    """)

    # Create theatres table
    cursor.execute("""
    CREATE TABLE theatres (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        location VARCHAR(255) NOT NULL,
        city VARCHAR(255) NOT NULL
    ) ENGINE=InnoDB;
    """)

    # Create showtimes table
    cursor.execute("""
    CREATE TABLE showtimes (
        id INT AUTO_INCREMENT PRIMARY KEY,
        movie_id INT NOT NULL,
        theatre_id INT NOT NULL,
        time VARCHAR(50) NOT NULL,
        date VARCHAR(50) NOT NULL,
        hall VARCHAR(50) NOT NULL,
        price DECIMAL(10,2) NOT NULL,
        vip_surcharge INT DEFAULT 3,
        recliner_surcharge INT DEFAULT 6,
        show_name VARCHAR(255) DEFAULT 'Regular Show',
        seating_layout VARCHAR(50) DEFAULT 'standard',
        format VARCHAR(50) DEFAULT '2D',
        FOREIGN KEY (movie_id) REFERENCES movies (id) ON DELETE CASCADE,
        FOREIGN KEY (theatre_id) REFERENCES theatres (id) ON DELETE CASCADE
    ) ENGINE=InnoDB;
    """)

    # Create bookings table
    cursor.execute("""
    CREATE TABLE bookings (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT NOT NULL,
        showtime_id INT NOT NULL,
        customer_name VARCHAR(255) NOT NULL,
        customer_email VARCHAR(255) NOT NULL,
        customer_phone VARCHAR(50) DEFAULT NULL,
        booking_code VARCHAR(50) UNIQUE NOT NULL,
        total_price DECIMAL(10,2) NOT NULL,
        seats VARCHAR(255) NOT NULL,
        status VARCHAR(50) DEFAULT 'Confirmed',
        payment_type VARCHAR(50) DEFAULT 'Online',
        FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
        FOREIGN KEY (showtime_id) REFERENCES showtimes (id) ON DELETE CASCADE
    ) ENGINE=InnoDB;
    """)
    print("Database tables created.")

    # Insert default users
    admin_pw = generate_password_hash("admin123")
    user_pw = generate_password_hash("user123")
    cursor.execute("INSERT INTO users (username, email, password_hash, is_admin) VALUES (%s, %s, %s, %s)",
                   ('admin', 'admin@cinema.com', admin_pw, 1))
    cursor.execute("INSERT INTO users (username, email, password_hash, is_admin) VALUES (%s, %s, %s, %s)",
                   ('user', 'user@cinema.com', user_pw, 0))

    # Let's seed some sample theatres, movies, and showtimes
    cursor.execute("INSERT INTO theatres (name, location, city) VALUES (%s, %s, %s)", ('Movie Ticket Booking Max', 'Downtown Center', 'Mumbai'))
    cursor.execute("INSERT INTO theatres (name, location, city) VALUES (%s, %s, %s)", ('Galaxy Cinema', 'Westside Mall', 'Delhi'))
    theatre_1_id = cursor.lastrowid
    
    # Add movies (Released and Upcoming)
    cursor.execute("""
        INSERT INTO movies (title, description, genre, duration, rating, poster_path, language, release_status, formats) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, 'Released', '2D, 3D, IMAX')
    """, ('Dune: Part Two', 'Paul Atreides unites with Chani and the Fremen while seeking revenge.', 'Sci-Fi', 166, 8.8, '/static/images/poster_dune.png', 'English'))
    movie_1_id = cursor.lastrowid

    cursor.execute("""
        INSERT INTO movies (title, description, genre, duration, rating, poster_path, language, release_status, formats) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, 'Released', '2D, 3D')
    """, ('Spider-Man: No Way Home', 'Peter Parker seeks the help of Doctor Strange to make his identity a secret again.', 'Action', 148, 9.0, '/static/images/spidermannwh_hardcover.jpg', 'English'))
    movie_2_id = cursor.lastrowid

    cursor.execute("""
        INSERT INTO movies (title, description, genre, duration, rating, poster_path, language, release_status, release_date, formats) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, 'Upcoming', 'Dec 18, 2026', '3D, IMAX')
    """, ('Avatar: Fire and Ash', 'The third installment in the epic sci-fi series exploring new biomes of Pandora.', 'Sci-Fi', 160, 9.2, '', 'English'))

    cursor.execute("""
        INSERT INTO movies (title, description, genre, duration, rating, poster_path, language, release_status, release_date, formats) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, 'Upcoming', 'Oct 02, 2026', '2D')
    """, ('The Batman Part II', 'The Dark Knight returns to face new criminal threats in Gotham City.', 'Action', 150, 8.7, '', 'English'))

    # Add showtimes
    today = datetime.now().strftime('%Y-%m-%d')
    tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')

    cursor.execute("""
        INSERT INTO showtimes (movie_id, theatre_id, date, time, hall, price, vip_surcharge, recliner_surcharge, show_name, format)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, '2D')
    """, (movie_1_id, 1, today, '14:00', 'Hall A', 12.00, 3, 6, 'Regular Show'))

    cursor.execute("""
        INSERT INTO showtimes (movie_id, theatre_id, date, time, hall, price, vip_surcharge, recliner_surcharge, show_name, format)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, '3D')
    """, (movie_1_id, 1, today, '18:30', 'Hall A', 14.50, 4, 8, 'Evening Show'))

    cursor.execute("""
        INSERT INTO showtimes (movie_id, theatre_id, date, time, hall, price, vip_surcharge, recliner_surcharge, show_name, format)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, 'IMAX')
    """, (movie_2_id, 2, tomorrow, '15:00', 'IMAX Hall', 15.00, 5, 10, '3D IMAX'))

    conn.commit()
    conn.close()
    print("Database initialized and populated successfully with sample data.")

if __name__ == '__main__':
    init_db()
