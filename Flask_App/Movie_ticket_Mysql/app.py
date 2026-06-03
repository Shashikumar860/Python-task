import os
import pymysql
import random
import string
import hashlib
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session, flash, abort
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

# Load configuration from .env
load_dotenv()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", 3306))
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "root")
DB_NAME = os.getenv("DB_NAME", "movie_ticketing_db")

app = Flask(__name__)
app.secret_key = 'super_secret_movie_ticket_booking_session_key'

@app.template_filter('time_12hr')
def time_12hr_filter(time_str):
    if not time_str:
        return ''
    try:
        t = datetime.strptime(str(time_str), "%H:%M")
        return t.strftime("%I:%M %p").lstrip('0')
    except ValueError:
        try:
            t = datetime.strptime(str(time_str), "%H:%M:%S")
            return t.strftime("%I:%M %p").lstrip('0')
        except ValueError:
            return str(time_str)

def generate_password_hash(password):
    salt = os.urandom(16)
    key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    return f"pbkdf2:sha256:100000${salt.hex()}${key.hex()}"

def check_password_hash(password_hash, password):
    if not password_hash or '$' not in password_hash:
        return False
    try:
        method_part, salt_hex, key_hex = password_hash.split('$', 2)
        _, hash_name, iterations = method_part.split(':')
        salt = bytes.fromhex(salt_hex)
        calc_key = hashlib.pbkdf2_hmac(hash_name, password.encode('utf-8'), salt, int(iterations))
        return calc_key.hex() == key_hex
    except ValueError:
        return False

class MySQLRow:
    def __init__(self, cursor, row_tuple):
        self._keys = [desc[0] for desc in cursor.description]
        self._values = row_tuple
        self._dict = dict(zip(self._keys, row_tuple))

    def __getitem__(self, key):
        if isinstance(key, int):
            return self._values[key]
        return self._dict[key]

    def keys(self):
        return self._keys

    def __contains__(self, key):
        return key in self._dict

    def __iter__(self):
        return iter(self._values)

    def __len__(self):
        return len(self._values)

    def get(self, key, default=None):
        return self._dict.get(key, default)

    def items(self):
        return self._dict.items()

    def values(self):
        return self._values

class MySQLRowCursor(pymysql.cursors.Cursor):
    def fetchone(self):
        row = super().fetchone()
        if row is None:
            return None
        return MySQLRow(self, row)

    def fetchall(self):
        rows = super().fetchall()
        return [MySQLRow(self, r) for r in rows]

    def fetchmany(self, size=None):
        rows = super().fetchmany(size)
        return [MySQLRow(self, r) for r in rows]

def get_db():
    try:
        conn = pymysql.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            cursorclass=MySQLRowCursor
        )
        return conn
    except pymysql.err.OperationalError as exc:
        if exc.args and exc.args[0] == 1049:
            conn = pymysql.connect(
                host=DB_HOST,
                port=DB_PORT,
                user=DB_USER,
                password=DB_PASSWORD,
                cursorclass=MySQLRowCursor
            )
            cursor = conn.cursor()
            cursor.execute(
                f"CREATE DATABASE IF NOT EXISTS `{DB_NAME}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
            )
            conn.select_db(DB_NAME)
            return conn
        raise

def create_tables():
    conn = get_db()
    cursor = conn.cursor()
    
    def table_has_column(cursor, table_name, column_name):
        cursor.execute("SHOW COLUMNS FROM `{}` LIKE %s".format(table_name), (column_name,))
        return cursor.fetchone() is not None

    def table_has_primary_key(cursor, table_name):
        cursor.execute(
            "SELECT COUNT(*) AS pk_count FROM INFORMATION_SCHEMA.TABLE_CONSTRAINTS "
            "WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = %s AND CONSTRAINT_TYPE = 'PRIMARY KEY'",
            (table_name,)
        )
        row = cursor.fetchone()
        return row and row['pk_count'] > 0

    def ensure_primary_key_id(cursor, table_name):
        if not table_has_column(cursor, table_name, 'id'):
            if table_has_primary_key(cursor, table_name):
                cursor.execute(
                    f"ALTER TABLE `{table_name}` ADD COLUMN id INT NOT NULL AUTO_INCREMENT FIRST, "
                    f"ADD UNIQUE KEY `uniq_{table_name}_id` (`id`)"
                )
            else:
                cursor.execute(
                    f"ALTER TABLE `{table_name}` ADD COLUMN id INT NOT NULL AUTO_INCREMENT PRIMARY KEY FIRST"
                )

    # Users Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(255) UNIQUE NOT NULL,
        email VARCHAR(255) UNIQUE NOT NULL,
        password_hash VARCHAR(255) NOT NULL,
        is_admin INT DEFAULT 0
    ) ENGINE=InnoDB;
    """)
    
    # Movies Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS movies (
        id INT AUTO_INCREMENT PRIMARY KEY,
        title VARCHAR(255) NOT NULL,
        description TEXT NOT NULL,
        genre VARCHAR(255) NOT NULL,
        duration INT NOT NULL,
        rating FLOAT NOT NULL,
        poster_path VARCHAR(255) NOT NULL,
        language VARCHAR(100) DEFAULT 'English',
        release_status VARCHAR(50) DEFAULT 'Released',
        release_date VARCHAR(50) DEFAULT NULL
    ) ENGINE=InnoDB;
    """)
    ensure_primary_key_id(cursor, 'movies')
    
    if not table_has_column(cursor, 'movies', 'release_status'):
        cursor.execute("ALTER TABLE movies ADD COLUMN release_status VARCHAR(50) DEFAULT 'Released'")
    if not table_has_column(cursor, 'movies', 'release_date'):
        cursor.execute("ALTER TABLE movies ADD COLUMN release_date VARCHAR(50) DEFAULT NULL")
    if not table_has_column(cursor, 'movies', 'formats'):
        cursor.execute("ALTER TABLE movies ADD COLUMN formats VARCHAR(255) DEFAULT '2D'")
    
    # Check if rating column is float or varchar
    cursor.execute("SHOW COLUMNS FROM movies LIKE 'rating'")
    col_info = cursor.fetchone()
    if col_info and 'varchar' in col_info['Type'].lower():
        # Update any existing non-numeric text values to default float string
        cursor.execute("UPDATE movies SET rating = '8.5' WHERE rating REGEXP '^[^0-9.]+$' OR rating = ''")
        cursor.execute("ALTER TABLE movies MODIFY COLUMN rating FLOAT NOT NULL")
        conn.commit()
    
    # Theatres Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS theatres (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        location VARCHAR(255) NOT NULL,
        city VARCHAR(255) NOT NULL
    ) ENGINE=InnoDB;
    """)
    ensure_primary_key_id(cursor, 'theatres')
    if not table_has_column(cursor, 'theatres', 'city'):
        cursor.execute("ALTER TABLE theatres ADD COLUMN city VARCHAR(255) DEFAULT ''")
    
    # Showtimes Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS showtimes (
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
    if not table_has_column(cursor, 'showtimes', 'seating_layout'):
        cursor.execute("ALTER TABLE showtimes ADD COLUMN seating_layout VARCHAR(50) DEFAULT 'standard'")
    if not table_has_column(cursor, 'showtimes', 'format'):
        cursor.execute("ALTER TABLE showtimes ADD COLUMN format VARCHAR(50) DEFAULT '2D'")
    
    # Bookings Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS bookings (
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
    if not table_has_column(cursor, 'bookings', 'payment_type'):
        cursor.execute("ALTER TABLE bookings ADD COLUMN payment_type VARCHAR(50) DEFAULT 'Online'")
    if not table_has_column(cursor, 'bookings', 'customer_phone'):
        cursor.execute("ALTER TABLE bookings ADD COLUMN customer_phone VARCHAR(50) DEFAULT NULL")
    conn.commit()
    conn.close()

# Helper decorators
def login_required(f):
    def wrapper(*args, **kwargs):
        if 'user_id' not in session:
            flash("Please log in to continue.", "error")
            return redirect(url_for('login', next=request.url))
        
        # Verify user still exists in database (handles DB resets)
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE id = %s", (session['user_id'],))
        user_exists = cursor.fetchone()
        conn.close()
        
        if not user_exists:
            session.clear()
            flash("Your session has expired. Please log in again.", "error")
            return redirect(url_for('login', next=request.url))
            
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper

def admin_required(f):
    def wrapper(*args, **kwargs):
        if 'user_id' not in session or not session.get('is_admin'):
            abort(403)
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper

# User Routes
@app.route('/')
def welcome():
    return render_template('welcome.html')

@app.route('/movies')
def browse_movies():
    search_query = request.args.get('search', '').strip()
    selected_genre = request.args.get('genre', '').strip()
    selected_city = request.args.get('city', '').strip()
    
    conn = get_db()
    cursor = conn.cursor()
    
    # Query distinct cities
    cursor.execute("SELECT DISTINCT city FROM theatres WHERE city != '' ORDER BY city")
    cities = [r['city'] for r in cursor.fetchall()]
    
    # Query Released movies (Now Showing)
    if selected_city:
        query_released = """
            SELECT DISTINCT m.* 
            FROM movies m
            JOIN showtimes s ON m.id = s.movie_id
            JOIN theatres t ON s.theatre_id = t.id
            WHERE m.release_status IN ('Released', 'Re-Release') AND t.city = %s
        """
        params_released = [selected_city]
    else:
        query_released = "SELECT * FROM movies WHERE release_status IN ('Released', 'Re-Release')"
        params_released = []
        
    if search_query:
        query_released += " AND m.title LIKE %s" if selected_city else " AND title LIKE %s"
        params_released.append(f"%{search_query}%")
        
    if selected_genre:
        query_released += " AND m.genre = %s" if selected_city else " AND genre = %s"
        params_released.append(selected_genre)
        
    cursor.execute(query_released, params_released)
    now_showing = cursor.fetchall()
    
    # Query Upcoming movies (Coming Soon)
    query_upcoming = "SELECT * FROM movies WHERE release_status = 'Upcoming'"
    params_upcoming = []
    
    if search_query:
        query_upcoming += " AND title LIKE %s"
        params_upcoming.append(f"%{search_query}%")
        
    if selected_genre:
        query_upcoming += " AND genre = %s"
        params_upcoming.append(selected_genre)
        
    cursor.execute(query_upcoming, params_upcoming)
    upcoming = cursor.fetchall()
    
    conn.close()
    
    featured_movie = now_showing[0] if now_showing else None
    
    return render_template('index.html', now_showing=now_showing, upcoming=upcoming, 
                           featured_movie=featured_movie, search_query=search_query, 
                           selected_genre=selected_genre, cities=cities, selected_city=selected_city)


@app.route('/live-status')
@login_required
def live_status():
    conn = get_db()
    cursor = conn.cursor()
    
    # Query all active showtimes for currently released movies
    cursor.execute("""
        SELECT s.id, s.time, s.date, s.hall, s.price, s.show_name, s.seating_layout,
               m.id as movie_id, m.title as movie_title, m.poster_path, m.genre,
               t.name as theatre_name, t.location, t.city
        FROM showtimes s
        JOIN movies m ON s.movie_id = m.id
        JOIN theatres t ON s.theatre_id = t.id
        WHERE m.release_status IN ('Released', 'Re-Release')
        ORDER BY s.date, s.time
    """)
    active_showtimes_raw = cursor.fetchall()
    
    active_shows = []
    for row in active_showtimes_raw:
        show_id = row['id']
        cursor.execute("SELECT seats FROM bookings WHERE showtime_id = %s AND status != 'Cancelled'", (show_id,))
        bookings_for_show = cursor.fetchall()
        
        booked_count = 0
        for b in bookings_for_show:
            seats_list = [s.strip() for s in b['seats'].split(',') if s.strip()]
            booked_count += len(seats_list)
            
        layout = row.get('seating_layout', 'standard')
        total_seats = 48 if layout == 'standard' else 64
        remaining_seats = max(0, total_seats - booked_count)
        
        active_shows.append({
            'id': show_id,
            'movie_id': row['movie_id'],
            'movie_title': row['movie_title'],
            'poster_path': row['poster_path'],
            'genre': row['genre'],
            'time': row['time'],
            'date': row['date'],
            'hall': row['hall'],
            'price': float(row['price']),
            'show_name': row['show_name'],
            'theatre_name': row['theatre_name'],
            'location': f"{row['location']}, {row['city']}" if 'city' in row and row['city'] else row['location'],
            'remaining_seats': remaining_seats,
            'booked_seats': booked_count,
            'total_seats': total_seats,
            'fill_percentage': round((booked_count / total_seats) * 100)
        })
    
    conn.close()
    return render_template('live_status.html', active_shows=active_shows)



@app.route('/movie/<int:movie_id>')
def movie_details(movie_id):
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM movies WHERE id = %s", (movie_id,))
    movie = cursor.fetchone()
    
    if not movie:
        conn.close()
        flash("Movie not found.", "error")
        return redirect(url_for('browse_movies'))
        
    cursor.execute("""
        SELECT s.id, s.time, s.date, s.hall, s.price, s.vip_surcharge, s.recliner_surcharge, s.show_name, s.seating_layout, s.format,
               t.name as theatre_name, t.location, t.city 
        FROM showtimes s
        JOIN theatres t ON s.theatre_id = t.id
        WHERE s.movie_id = %s
        ORDER BY t.name, s.date, s.time
    """, (movie_id,))
    showtimes_raw = cursor.fetchall()
    
    showtimes_seats = {}
    for row in showtimes_raw:
        show_id = row['id']
        cursor.execute("SELECT seats FROM bookings WHERE showtime_id = %s AND status != 'Cancelled'", (show_id,))
        bookings_for_show = cursor.fetchall()
        
        silver_booked = 0
        gold_booked = 0
        recliner_booked = 0
        layout = row.get('seating_layout', 'standard')
        
        if layout == 'standard':
            silver_rows = ['A', 'B', 'C']
            gold_rows = ['D', 'E']
            recliner_row = 'F'
            total_seats = 48
            silver_cap = 24
            gold_cap = 16
            recliner_cap = 8
        else:
            silver_rows = ['A', 'B', 'C', 'D', 'E']
            gold_rows = ['F', 'G']
            recliner_row = 'H'
            total_seats = 64
            silver_cap = 40
            gold_cap = 16
            recliner_cap = 8
            
        for b in bookings_for_show:
            seats_list = [s.strip() for s in b['seats'].split(',') if s.strip()]
            for seat in seats_list:
                if not seat:
                    continue
                row_char = seat[0].upper()
                if row_char in silver_rows:
                    silver_booked += 1
                elif row_char in gold_rows:
                    gold_booked += 1
                elif row_char == recliner_row:
                    recliner_booked += 1
                    
        showtimes_seats[show_id] = {
            'total_left': max(0, total_seats - (silver_booked + gold_booked + recliner_booked)),
            'silver_left': max(0, silver_cap - silver_booked),
            'gold_left': max(0, gold_cap - gold_booked),
            'recliner_left': max(0, recliner_cap - recliner_booked)
        }
    conn.close()
    
    showtimes_grouped = {}
    for row in showtimes_raw:
        show_id = row['id']
        time = row['time']
        date = row['date']
        hall = row['hall']
        price = row['price']
        t_name = row['theatre_name']
        t_loc = f"{row['location']}, {row['city']}" if 'city' in row and row['city'] else row['location']
        vip_surch = row['vip_surcharge']
        recliner_surch = row['recliner_surcharge']
        show_name = row['show_name']
        
        if t_name not in showtimes_grouped:
            showtimes_grouped[t_name] = {
                'location': t_loc,
                'dates': {}
            }
        if date not in showtimes_grouped[t_name]['dates']:
            showtimes_grouped[t_name]['dates'][date] = []
            
        showtimes_grouped[t_name]['dates'][date].append({
            'id': show_id,
            'time': time,
            'hall': hall,
            'price': price,
            'vip_surcharge': vip_surch,
            'recliner_surcharge': recliner_surch,
            'show_name': show_name,
            'format': row.get('format', '2D'),
            'remaining_seats': showtimes_seats[show_id]['total_left'],
            'silver_left': showtimes_seats[show_id]['silver_left'],
            'gold_left': showtimes_seats[show_id]['gold_left'],
            'recliner_left': showtimes_seats[show_id]['recliner_left']
        })
        
    return render_template('movie_details.html', movie=movie, showtimes_grouped=showtimes_grouped)

@app.route('/book/<int:showtime_id>')
@login_required
def book_seats(showtime_id):
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT s.id, s.movie_id, s.theatre_id, s.time, s.date, s.hall, s.price, 
               t.name, t.location, m.title, s.vip_surcharge, s.recliner_surcharge, s.show_name, s.seating_layout, t.city
        FROM showtimes s
        JOIN theatres t ON s.theatre_id = t.id
        JOIN movies m ON s.movie_id = m.id
        WHERE s.id = %s
    """, (showtime_id,))
    showtime = cursor.fetchone()
    
    if not showtime:
        conn.close()
        flash("Showtime not found.", "error")
        return redirect(url_for('browse_movies'))
        
    cursor.execute("SELECT seats FROM bookings WHERE showtime_id = %s AND status != 'Cancelled'", (showtime_id,))
    bookings = cursor.fetchall()
    conn.close()
    
    occupied_seats = []
    for b in bookings:
        seats_list = b['seats'].split(',')
        occupied_seats.extend([s.strip() for s in seats_list if s.strip()])
        
    layout = showtime.get('seating_layout', 'standard')
    total_seats = 48 if layout == 'standard' else 64
    remaining_seats = max(0, total_seats - len(occupied_seats))
    return render_template('book_seats.html', showtime=showtime, occupied_seats=occupied_seats, remaining_seats=remaining_seats)

@app.route('/checkout', methods=['POST'])
@login_required
def checkout():
    showtime_id = request.form.get('showtime_id')
    selected_seats_str = request.form.get('selected_seats', '').strip()
    customer_name = request.form.get('customer_name', '').strip()
    customer_email = request.form.get('customer_email', '').strip()
    customer_phone = request.form.get('customer_phone', '').strip()
    payment_type = request.form.get('payment_type', 'Online').strip()
    
    if not selected_seats_str:
        flash("No seats selected. Please choose your seats.", "error")
        return redirect(url_for('book_seats', showtime_id=showtime_id))
        
    seats_list = [s.strip() for s in selected_seats_str.split(',') if s.strip()]
    
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT price, vip_surcharge, recliner_surcharge, seating_layout FROM showtimes WHERE id = %s", (showtime_id,))
    showtime = cursor.fetchone()
    
    if not showtime:
        conn.close()
        flash("Showtime not found.", "error")
        return redirect(url_for('browse_movies'))
        
    base_price = float(showtime['price'])
    vip_surch = showtime['vip_surcharge']
    recliner_surch = showtime['recliner_surcharge']
    layout = showtime.get('seating_layout', 'standard')
    
    recliner_row = 'F' if layout == 'standard' else 'H'
    gold_rows = ['D', 'E'] if layout == 'standard' else ['F', 'G']
    
    total_price = 0.0
    for seat in seats_list:
        row = seat[0].upper()
        if row == recliner_row:
            total_price += base_price + recliner_surch
        elif row in gold_rows:
            total_price += base_price + vip_surch
        else:
            total_price += base_price
            
    random_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    booking_code = f"CP-{random_str}"
    
    try:
        cursor.execute("""
            INSERT INTO bookings (user_id, showtime_id, customer_name, customer_email, customer_phone, booking_code, total_price, seats, status, payment_type)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 'Confirmed', %s)
        """, (session['user_id'], showtime_id, customer_name, customer_email, customer_phone, booking_code, total_price, selected_seats_str, payment_type))
        conn.commit()
    except Exception as e:
        conn.close()
        flash(f"Booking error: {e}", "error")
        return redirect(url_for('book_seats', showtime_id=showtime_id))
        
    conn.close()
    flash("Booking completed successfully!", "success")
    return redirect(url_for('confirmation', booking_code=booking_code))

@app.route('/confirmation/<string:booking_code>')
@login_required
def confirmation(booking_code):
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT b.id, b.user_id, b.booking_code, s.time, s.date, b.total_price, b.seats,
               m.title, t.name, s.hall, b.customer_name, b.status, b.payment_type, b.customer_phone
        FROM bookings b
        JOIN showtimes s ON b.showtime_id = s.id
        JOIN movies m ON s.movie_id = m.id
        JOIN theatres t ON s.theatre_id = t.id
        WHERE b.booking_code = %s
    """, (booking_code,))
    ticket = cursor.fetchone()
    conn.close()
    
    if not ticket:
        flash("Ticket not found.", "error")
        return redirect(url_for('browse_movies'))
        
    if ticket['user_id'] != session['user_id'] and not session.get('is_admin'):
        abort(403)
        
    return render_template('confirmation.html', ticket=ticket)

@app.route('/my-bookings')
@login_required
def my_bookings():
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT b.id, b.showtime_id, b.customer_name, b.customer_email, b.total_price, 
               b.booking_code, b.seats, s.time, s.date, b.status, m.title, t.name, s.hall,
               b.payment_type, b.customer_phone
        FROM bookings b
        JOIN showtimes s ON b.showtime_id = s.id
        JOIN movies m ON s.movie_id = m.id
        JOIN theatres t ON s.theatre_id = t.id
        WHERE b.user_id = %s
        ORDER BY s.date DESC, s.time DESC
    """, (session['user_id'],))
    bookings = cursor.fetchall()
    conn.close()
    
    return render_template('my_bookings.html', bookings=bookings)

@app.route('/cancel-booking/<int:booking_id>', methods=['POST'])
@login_required
def cancel_booking(booking_id):
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT user_id, status FROM bookings WHERE id = %s", (booking_id,))
    booking = cursor.fetchone()
    
    if not booking:
        conn.close()
        flash("Booking record not found.", "error")
        return redirect(url_for('my_bookings'))
        
    if booking['user_id'] != session['user_id'] and not session.get('is_admin'):
        conn.close()
        abort(403)
        
    if booking['status'] == 'Cancelled':
        conn.close()
        flash("Booking is already cancelled.", "error")
        return redirect(url_for('my_bookings'))
        
    cursor.execute("UPDATE bookings SET status = 'Cancelled' WHERE id = %s", (booking_id,))
    conn.commit()
    conn.close()
    
    flash("Booking successfully cancelled. Seats have been released.", "success")
    
    if session.get('is_admin') and request.referrer and 'admin' in request.referrer:
        return redirect(url_for('admin_dashboard'))
    return redirect(url_for('my_bookings'))

@app.route('/delete-booking/<int:booking_id>', methods=['POST'])
@login_required
def delete_booking(booking_id):
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT user_id, status FROM bookings WHERE id = %s", (booking_id,))
    booking = cursor.fetchone()
    
    if not booking:
        conn.close()
        flash("Booking record not found.", "error")
        return redirect(url_for('my_bookings'))
        
    if booking['user_id'] != session['user_id'] and not session.get('is_admin'):
        conn.close()
        abort(403)
        
    if booking['status'] != 'Cancelled':
        conn.close()
        flash("Only cancelled bookings can be deleted from history.", "error")
        return redirect(url_for('my_bookings'))
        
    cursor.execute("DELETE FROM bookings WHERE id = %s", (booking_id,))
    conn.commit()
    conn.close()
    
    flash("Booking record permanently deleted from your history.", "success")
    return redirect(url_for('my_bookings'))

# User Auth Routes
@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('browse_movies'))
        
    conn = get_db()
    cursor = conn.cursor()
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        
        cursor.execute("SELECT * FROM users WHERE username = %s OR email = %s", (username, username))
        user = cursor.fetchone()
        
        if user and check_password_hash(user['password_hash'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['email'] = user['email']
            session['is_admin'] = bool(user['is_admin'])
            
            conn.close()
            flash("Welcome back!", "success")
            next_url = request.args.get('next')
            return redirect(next_url or url_for('browse_movies'))
        else:
            flash("Invalid username or password.", "error")
            
    conn.close()
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'user_id' in session:
        return redirect(url_for('browse_movies'))
        
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()
        
        conn = get_db()
        cursor = conn.cursor()
        
        cursor.execute("SELECT id FROM users WHERE username = %s OR email = %s", (username, email))
        if cursor.fetchone():
            conn.close()
            flash("Username or Email is already registered.", "error")
            return render_template('register.html')
            
        is_admin = 1 if username.lower() == 'admin' else 0
        password_hash = generate_password_hash(password)
        
        try:
            cursor.execute("""
                INSERT INTO users (username, email, password_hash, is_admin)
                VALUES (%s, %s, %s, %s)
            """, (username, email, password_hash, is_admin))
            conn.commit()
            flash("Registration successful! Please log in.", "success")
            return redirect(url_for('login'))
        except Exception as e:
            flash(f"Error during registration: {e}", "error")
        finally:
            conn.close()
            
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    flash("You have logged out.", "success")
    return redirect(url_for('welcome'))

# Admin Dashboard
@app.route('/admin')
@admin_required
def admin_dashboard():
    conn = get_db()
    cursor = conn.cursor()
    
    # metrics
    cursor.execute("SELECT SUM(total_price) AS total_rev FROM bookings WHERE status != 'Cancelled'")
    total_rev = float(cursor.fetchone()['total_rev'] or 0.0)
    
    cursor.execute("SELECT COUNT(id) AS active_b FROM bookings WHERE status != 'Cancelled'")
    active_b = cursor.fetchone()['active_b']
    
    cursor.execute("SELECT COUNT(id) AS cancelled_b FROM bookings WHERE status = 'Cancelled'")
    cancelled_b = cursor.fetchone()['cancelled_b']
    
    cursor.execute("SELECT COUNT(id) AS total_u FROM users")
    total_u = cursor.fetchone()['total_u']
    
    metrics = {
        'total_revenue': total_rev,
        'active_bookings': active_b,
        'cancelled_bookings': cancelled_b,
        'total_users': total_u
    }
    
    # movies_list
    cursor.execute("""
        SELECT m.id, m.title, m.genre, m.duration, m.rating, m.poster_path, COUNT(s.id) as showtimes_count
        FROM movies m
        LEFT JOIN showtimes s ON m.id = s.movie_id
        GROUP BY m.id
    """)

    movies_list = cursor.fetchall()
    
    # theatres_list
    cursor.execute("SELECT id, name, location, city FROM theatres ORDER BY name")
    theatres_list = cursor.fetchall()
    
    # showtimes_list
    cursor.execute("""
        SELECT s.id, s.hall, s.date, s.time, s.price, 
               m.title as movie_title, t.name as theatre_name
        FROM showtimes s
        JOIN movies m ON s.movie_id = m.id
        JOIN theatres t ON s.theatre_id = t.id
        ORDER BY s.date DESC, s.time DESC
    """)
    showtimes_list = cursor.fetchall()
    
    # revenue_list
    cursor.execute("SELECT id, title, genre FROM movies")
    movies_all = cursor.fetchall()
    
    revenue_list = []
    for m in movies_all:
        cursor.execute("""
            SELECT seats, status, total_price 
            FROM bookings b
            JOIN showtimes s ON b.showtime_id = s.id
            WHERE s.movie_id = %s
        """, (m['id'],))
        movie_bookings = cursor.fetchall()
        
        tickets_sold = 0
        active_count = 0
        cancelled_count = 0
        movie_revenue = 0.0
        
        for mb in movie_bookings:
            seats_num = len([x for x in mb['seats'].split(',') if x.strip()])
            if mb['status'] != 'Cancelled':
                tickets_sold += seats_num
                active_count += 1
                movie_revenue += float(mb['total_price'])
            else:
                cancelled_count += 1
                
        revenue_list.append({
            'id': m['id'],
            'title': m['title'],
            'genre': m['genre'],
            'tickets_sold': tickets_sold,
            'active_bookings': active_count,
            'cancelled_bookings': cancelled_count,
            'total_revenue': movie_revenue
        })
        
    # bookings_list
    cursor.execute("""
        SELECT b.id, b.booking_code, b.customer_name, b.customer_email, b.seats, b.total_price, b.status,
               m.title as movie_title, t.name as theatre_name, s.hall, s.date as show_date, s.time as show_time,
               b.payment_type, b.customer_phone
        FROM bookings b
        JOIN showtimes s ON b.showtime_id = s.id
        JOIN movies m ON s.movie_id = m.id
        JOIN theatres t ON s.theatre_id = t.id
        ORDER BY s.date DESC, s.time DESC, b.id DESC
    """)
    bookings_list = cursor.fetchall()
    conn.close()
    
    return render_template('admin.html', metrics=metrics, movies_list=movies_list, 
                           theatres_list=theatres_list, showtimes_list=showtimes_list,
                           revenue_list=revenue_list, bookings_list=bookings_list)

@app.route('/admin/update-booking-status/<int:booking_id>', methods=['POST'])
@admin_required
def admin_update_booking_status(booking_id):
    new_status = request.form.get('status')
    
    if new_status not in ['Confirmed', 'Cancelled', 'Attended']:
        flash("Invalid status choice.", "error")
        return redirect(url_for('admin_dashboard'))
        
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE bookings SET status = %s WHERE id = %s", (new_status, booking_id))
    conn.commit()
    conn.close()
    
    flash(f"Booking status updated to '{new_status}' successfully.", "success")
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/movie/add', methods=['GET', 'POST'])
@admin_required
def admin_movie_add():
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        genre = request.form.get('genre', '').strip()
        duration = int(request.form.get('duration', 0))
        rating_str = request.form.get('rating', '').strip()
        try:
            rating = float(rating_str)
        except ValueError:
            rating = 0.0
        description = request.form.get('description', '').strip()
        language = request.form.get('language', 'English').strip()
        
        # Check for uploaded file
        file = request.files.get('poster_file')
        if file and file.filename != '':
            upload_dir = os.path.join(os.path.dirname(__file__), 'static', 'images')
            os.makedirs(upload_dir, exist_ok=True)
            filename = secure_filename(file.filename)
            filepath = os.path.join(upload_dir, filename)
            file.save(filepath)
            poster_path = f"/static/images/{filename}"
        else:
            poster_path = request.form.get('poster_path', '').strip()


        
        theatre_id = request.form.get('theatre_id')
        date = request.form.get('date', '').strip()
        time = request.form.get('time', '').strip()
        hall = request.form.get('hall', '').strip()
        price_str = request.form.get('price', '').strip()
        vip_surcharge_str = request.form.get('vip_surcharge', '').strip()
        recliner_surcharge_str = request.form.get('recliner_surcharge', '').strip()
        release_status = request.form.get('release_status', 'Released').strip()
        release_date = request.form.get('release_date', '').strip() if release_status == 'Upcoming' else None
        
        formats_list = request.form.getlist('formats')
        formats = ', '.join(formats_list) if formats_list else '2D'
        
        conn = get_db()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO movies (title, description, genre, duration, rating, poster_path, language, release_status, release_date, formats)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (title, description, genre, duration, rating, poster_path, language, release_status, release_date, formats))
            movie_id = cursor.lastrowid
            
            if theatre_id:
                price = float(price_str) if price_str else 0.0
                vip_price_input = int(vip_surcharge_str) if vip_surcharge_str else 0
                recliner_price_input = int(recliner_surcharge_str) if recliner_surcharge_str else 0
                
                # Calculate surcharges by subtracting base price (safeguarding at least 0)
                vip_surcharge = max(0, vip_price_input - int(price)) if vip_surcharge_str else 3
                recliner_surcharge = max(0, recliner_price_input - int(price)) if recliner_surcharge_str else 6
                cursor.execute("""
                    INSERT INTO showtimes (movie_id, theatre_id, date, time, hall, price, vip_surcharge, recliner_surcharge, show_name)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 'Regular Show')
                """, (movie_id, theatre_id, date, time, hall, price, vip_surcharge, recliner_surcharge))
                
            conn.commit()
            flash("Movie added successfully!", "success")
            return redirect(url_for('admin_dashboard'))
        except Exception as e:
            flash(f"Error adding movie: {e}", "error")
        finally:
            conn.close()
            
    else:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, location, city FROM theatres ORDER BY name")
        theatres = cursor.fetchall()
        conn.close()
        return render_template('admin_movie_form.html', title_text="Add New Movie", action="/admin/movie/add", movie=None, theatres=theatres)

@app.route('/admin/movie/edit/<int:movie_id>', methods=['GET', 'POST'])
@admin_required
def admin_movie_edit(movie_id):
    conn = get_db()
    cursor = conn.cursor()
    
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        genre = request.form.get('genre', '').strip()
        duration = int(request.form.get('duration', 0))
        rating_str = request.form.get('rating', '').strip()
        try:
            rating = float(rating_str)
        except ValueError:
            rating = 0.0
        description = request.form.get('description', '').strip()
        language = request.form.get('language', 'English').strip()
        
        # Check for uploaded file
        file = request.files.get('poster_file')
        if file and file.filename != '':
            upload_dir = os.path.join(os.path.dirname(__file__), 'static', 'images')
            os.makedirs(upload_dir, exist_ok=True)
            filename = secure_filename(file.filename)
            filepath = os.path.join(upload_dir, filename)
            file.save(filepath)
            poster_path = f"/static/images/{filename}"
        else:
            poster_path = request.form.get('poster_path', '').strip()

        if not poster_path:
            cursor.execute("SELECT poster_path FROM movies WHERE id = %s", (movie_id,))
            prev_movie = cursor.fetchone()
            poster_path = prev_movie['poster_path'] if prev_movie else ''

        release_status = request.form.get('release_status', 'Released').strip()
        release_date = request.form.get('release_date', '').strip() if release_status == 'Upcoming' else None
        
        formats_list = request.form.getlist('formats')
        formats = ', '.join(formats_list) if formats_list else '2D'

        try:
            cursor.execute("""
                UPDATE movies 
                SET title = %s, description = %s, genre = %s, duration = %s, rating = %s, poster_path = %s, language = %s, release_status = %s, release_date = %s, formats = %s
                WHERE id = %s
            """, (title, description, genre, duration, rating, poster_path, language, release_status, release_date, formats, movie_id))
            conn.commit()
            flash("Movie updated successfully!", "success")
            return redirect(url_for('admin_dashboard'))
        except Exception as e:
            flash(f"Error updating movie: {e}", "error")
        finally:
            conn.close()
            
    else:
        cursor.execute("SELECT * FROM movies WHERE id = %s", (movie_id,))
        movie = cursor.fetchone()
        conn.close()
        
        if not movie:
            flash("Movie not found.", "error")
            return redirect(url_for('admin_dashboard'))
            
        return render_template('admin_movie_form.html', title_text="Edit Movie Details", 
                               action=url_for('admin_movie_edit', movie_id=movie_id), movie=movie)

@app.route('/admin/movie/delete/<int:movie_id>', methods=['POST'])
@admin_required
def admin_movie_delete(movie_id):
    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM movies WHERE id = %s", (movie_id,))
        conn.commit()
        flash("Movie deleted successfully. All associated showtimes and tickets were cleared.", "success")
    except Exception as e:
        flash(f"Error deleting movie: {e}", "error")
    finally:
        conn.close()
        
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/showtime/add', methods=['GET', 'POST'])
@admin_required
def admin_showtime_add():
    conn = get_db()
    cursor = conn.cursor()
    
    if request.method == 'POST':
        movie_id = request.form.get('movie_id')
        theatre_id = request.form.get('theatre_id')
        date = request.form.get('date', '').strip()
        time = request.form.get('time', '').strip()
        hall = request.form.get('hall', '').strip()
        show_name = request.form.get('show_name', 'Regular Show').strip()
        price = float(request.form.get('price', 0.0))
        vip_surch_raw = request.form.get('vip_surcharge', '').strip()
        recliner_surch_raw = request.form.get('recliner_surcharge', '').strip()
        seating_layout = request.form.get('seating_layout', 'standard').strip()
        format = request.form.get('format', '2D').strip()
        
        vip_surcharge = max(0, int(vip_surch_raw) - int(price)) if vip_surch_raw else 3
        recliner_surcharge = max(0, int(recliner_surch_raw) - int(price)) if recliner_surch_raw else 6
        
        try:
            cursor.execute("""
                INSERT INTO showtimes (movie_id, theatre_id, date, time, hall, price, vip_surcharge, recliner_surcharge, show_name, seating_layout, format)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (movie_id, theatre_id, date, time, hall, price, vip_surcharge, recliner_surcharge, show_name, seating_layout, format))
            conn.commit()
            flash("Showtime scheduled successfully!", "success")
            return redirect(url_for('admin_dashboard'))
        except Exception as e:
            flash(f"Error scheduling showtime: {e}", "error")
        finally:
            conn.close()
            
    else:
        selected_movie_id = request.args.get('movie_id', type=int)
        cursor.execute("SELECT id, title, genre FROM movies ORDER BY title")
        movies = cursor.fetchall()
        
        cursor.execute("SELECT id, name, location, city FROM theatres ORDER BY name")
        theatres = cursor.fetchall()
        conn.close()
        
        return render_template('admin_showtime_form.html', movies=movies, theatres=theatres, selected_movie_id=selected_movie_id)

@app.route('/admin/showtime/delete/<int:showtime_id>', methods=['POST'])
@admin_required
def admin_showtime_delete(showtime_id):
    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM showtimes WHERE id = %s", (showtime_id,))
        conn.commit()
        flash("Showtime deleted successfully.", "success")
    except Exception as e:
        flash(f"Error deleting showtime: {e}", "error")
    finally:
        conn.close()
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/theatre/add', methods=['GET', 'POST'])
@admin_required
def admin_theatre_add():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        location = request.form.get('location', '').strip()
        city = request.form.get('city', '').strip()
        
        movie_id = request.form.get('movie_id')
        show_name = request.form.get('show_name', 'Regular Show').strip()
        date = request.form.get('date', '').strip()
        time = request.form.get('time', '').strip()
        hall = request.form.get('hall', '').strip()
        price_str = request.form.get('price', '').strip()
        vip_surcharge_str = request.form.get('vip_surcharge', '').strip()
        recliner_surcharge_str = request.form.get('recliner_surcharge', '').strip()
        
        conn = get_db()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO theatres (name, location, city)
                VALUES (%s, %s, %s)
            """, (name, location, city))
            theatre_id = cursor.lastrowid
            
            if movie_id:
                price = float(price_str) if price_str else 0.0
                vip_price_input = int(vip_surcharge_str) if vip_surcharge_str else 0
                recliner_price_input = int(recliner_surcharge_str) if recliner_surcharge_str else 0
                
                # Calculate surcharges by subtracting base price (safeguarding at least 0)
                vip_surcharge = max(0, vip_price_input - int(price)) if vip_surcharge_str else 3
                recliner_surcharge = max(0, recliner_price_input - int(price)) if recliner_surcharge_str else 6
                cursor.execute("""
                    INSERT INTO showtimes (movie_id, theatre_id, date, time, hall, price, vip_surcharge, recliner_surcharge, show_name)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (movie_id, theatre_id, date, time, hall, price, vip_surcharge, recliner_surcharge, show_name))
            
            conn.commit()
            flash("Theatre location added successfully!", "success")
            return redirect(url_for('admin_dashboard'))
        except Exception as e:
            flash(f"Error adding theatre: {e}", "error")
        finally:
            conn.close()
            
    else:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT id, title FROM movies ORDER BY title")
        movies = cursor.fetchall()
        conn.close()
        return render_template('admin_theatre_form.html', movies=movies)

@app.route('/admin/theatre/delete/<int:theatre_id>', methods=['POST'])
@admin_required
def admin_theatre_delete(theatre_id):
    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM theatres WHERE id = %s", (theatre_id,))
        conn.commit()
        flash("Theatre deleted successfully.", "success")
    except Exception as e:
        flash(f"Error deleting theatre: {e}", "error")
    finally:
        conn.close()
    return redirect(url_for('admin_dashboard'))

if __name__ == '__main__':
    create_tables()
    app.run(debug=True, port=5000)