import os
import re
import pymysql
from dotenv import load_dotenv

# Load environment variables
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", 3306))
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "root")
DB_NAME = os.getenv("DB_NAME", "movie_ticketing_db")

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

    def to_dict(self):
        return self._dict

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

def get_db_connection():
    """Establishes connection to the MySQL database."""
    return pymysql.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        cursorclass=MySQLRowCursor
    )

def strip_string_literals(sql: str) -> str:
    """Removes single and double quoted string literals to prevent keyword collision inside text values."""
    sql_no_single = re.sub(r"'[^'\\]*(?:\\.[^'\\]*)*'", "'STR'", sql)
    sql_no_both = re.sub(r'"[^"\\]*(?:\\.[^"\\]*)*"', '"STR"', sql_no_single)
    return sql_no_both

def is_safe_read_only_query(query: str) -> bool:
    """Validates if a SQL query is strictly read-only and safe to execute."""
    if not query:
        return False
        
    q = query.strip()
    
    # Strip SQL comments: both -- style and /* */ style
    q_no_comments = re.sub(r'--.*$', '', q, flags=re.MULTILINE)
    q_no_comments = re.sub(r'/\*.*?\*/', '', q_no_comments, flags=re.DOTALL)
    
    q_clean = q_no_comments.strip()
    q_upper = q_clean.upper()
    
    # Check for multiple statements (semicolon injection)
    if ';' in q_clean:
        parts = q_clean.split(';')
        non_empty_parts = [p.strip() for p in parts if p.strip()]
        if len(non_empty_parts) > 1:
            return False  # Multi-statement detected
            
    # Check if the query starts with allowed read-only commands
    allowed_starts = ('SELECT', 'SHOW', 'DESCRIBE', 'EXPLAIN')
    if not any(q_upper.startswith(start) for start in allowed_starts):
        return False
        
    # Strip out string literals before checking for forbidden keywords to avoid false positives
    q_without_strings = strip_string_literals(q_upper)
    
    # Check for forbidden writing/modifying keywords anywhere in the query (with word boundaries)
    forbidden_keywords = [
        r'\bINSERT\b', r'\bUPDATE\b', r'\bDELETE\b', r'\bDROP\b', r'\bALTER\b', 
        r'\bCREATE\b', r'\bRENAME\b', r'\bTRUNCATE\b', r'\bREPLACE\b', r'\bGRANT\b', 
        r'\bREVOKE\b', r'\bLOAD\b', r'\bINTO\s+OUTFILE\b', r'\bINTO\s+DUMPFILE\b', 
        r'\bFOR\s+UPDATE\b', r'\bLOCK\s+IN\s+SHARE\s+MODE\b'
    ]
    
    for pattern in forbidden_keywords:
        if re.search(pattern, q_without_strings):
            return False
            
    return True

def execute_read_query(sql_query: str, params=None):
    """Executes a read-only SQL query safely after validation."""
    if not is_safe_read_only_query(sql_query):
        raise PermissionError("Write or unsafe database operations are strictly prohibited.")
        
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(sql_query, params)
            result = cursor.fetchall()
            return [row.to_dict() for row in result]
    finally:
        conn.close()

def get_schema_info():
    """Generates schema description of the database to feed into the LLM system prompt."""
    schema_desc = """
Database Name: movie_ticketing_db

### Table Details:

1. **users**
   - id (INT, PRIMARY KEY, AUTO_INCREMENT)
   - username (VARCHAR(255), UNIQUE) - User's display name/login
   - email (VARCHAR(255), UNIQUE)
   - password_hash (VARCHAR(255))
   - is_admin (INT, 1 for Admin, 0 for standard user)

2. **movies**
   - id (INT, PRIMARY KEY, AUTO_INCREMENT)
   - title (VARCHAR(255)) - Movie title
   - description (TEXT) - Summary of the movie
   - genre (VARCHAR(255)) - Genre(s) (e.g. Sci-Fi, Action)
   - duration (INT) - Run time in minutes
   - rating (FLOAT) - IMDb/user rating (out of 10)
   - poster_path (VARCHAR(255)) - Path to poster image file
   - language (VARCHAR(100)) - Language of show (e.g. English, Hindi)
   - release_status (VARCHAR(50)) - 'Released' or 'Upcoming'
   - release_date (VARCHAR(50)) - Optional release date for upcoming movies
   - formats (VARCHAR(255)) - Available formats (e.g. '2D, 3D, IMAX')
   - certification (VARCHAR(50)) - Age rating (e.g. 'U', 'UA', 'A')

3. **theatres**
   - id (INT, PRIMARY KEY, AUTO_INCREMENT)
   - name (VARCHAR(255)) - Theatre name
   - location (VARCHAR(255)) - Local address/area
   - city (VARCHAR(255)) - City location (e.g. Mumbai, Delhi)

4. **showtimes**
   - id (INT, PRIMARY KEY, AUTO_INCREMENT)
   - movie_id (INT, FOREIGN KEY referencing movies.id)
   - theatre_id (INT, FOREIGN KEY referencing theatres.id)
   - time (VARCHAR(50)) - Start time of the show (24-hour HH:MM format, e.g. '14:00')
   - date (VARCHAR(50)) - Date of the show (YYYY-MM-DD format)
   - hall (VARCHAR(50)) - Hall label (e.g. 'Hall A', 'IMAX Hall')
   - price (DECIMAL(10,2)) - Base price for silver class seats
   - vip_surcharge (INT) - Extra price for gold class seats (default: 3)
   - recliner_surcharge (INT) - Extra price for recliner class seats (default: 6)
   - show_name (VARCHAR(255)) - Show name/type (e.g. 'Regular Show', '3D IMAX')
   - seating_layout (VARCHAR(50)) - 'standard' or 'premium'
   - format (VARCHAR(50)) - Format of this specific show (e.g. '2D', '3D', 'IMAX')
   - language (VARCHAR(100)) - Language of this specific show

5. **bookings**
   - id (INT, PRIMARY KEY, AUTO_INCREMENT)
   - user_id (INT, FOREIGN KEY referencing users.id)
   - showtime_id (INT, FOREIGN KEY referencing showtimes.id)
   - customer_name (VARCHAR(255)) - Name of person who booked
   - customer_email (VARCHAR(255))
   - customer_phone (VARCHAR(50))
   - booking_code (VARCHAR(50), UNIQUE) - Confirmation code (e.g. 'CP-XXXXXX')
   - total_price (DECIMAL(10,2)) - Final price paid
   - seats (VARCHAR(255)) - Comma-separated list of seat labels booked (e.g. 'A1, A2')
   - status (VARCHAR(50)) - Booking status ('Confirmed' or 'Cancelled')
   - payment_type (VARCHAR(50)) - Payment method ('Online', 'Cash', etc.)

6. **contact_submissions**
   - id (INT, PRIMARY KEY, AUTO_INCREMENT)
   - name (VARCHAR(255)) - Sender name
   - email (VARCHAR(255))
   - issue_type (VARCHAR(255)) - Category of inquiry
   - message (TEXT) - Detail content
   - ticket_number (VARCHAR(255)) - Support tracking code
   - created_at (TIMESTAMP) - Submission date and time

### Relationship Joins:
- `showtimes.movie_id` joins with `movies.id`
- `showtimes.theatre_id` joins with `theatres.id`
- `bookings.user_id` joins with `users.id`
- `bookings.showtime_id` joins with `showtimes.id`
"""
    return schema_desc
