# ============================================================
# 🎬 MOVIE TICKET BOOKING SYSTEM
# FastAPI + SQLite + SQLAlchemy
# ============================================================

# INSTALL:
# pip install fastapi uvicorn sqlalchemy

# RUN:
# uvicorn main:app --reload

# ============================================================

from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Float,
    ForeignKey
)

from sqlalchemy.orm import (
    declarative_base,
    sessionmaker,
    relationship,
    Session
)

# ============================================================
# DATABASE CONNECTION - SQLITE
# ============================================================

DATABASE_URL = "sqlite:///./movie_bookings.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

# ============================================================
# FASTAPI APP
# ============================================================

app = FastAPI(
    title="Movie Ticket Booking System",
    version="2.0"
)

# ============================================================
# DATABASE SESSION
# ============================================================

def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()

# ============================================================
# MODELS
# ============================================================

class Movie(Base):

    __tablename__ = "movies"

    movie_id = Column(Integer, primary_key=True, index=True)

    movie_name = Column(String(100))
    genre = Column(String(50))
    rating = Column(Float)
    duration = Column(String(20))


class Theatre(Base):

    __tablename__ = "theatres"

    theatre_id = Column(Integer, primary_key=True, index=True)

    theatre_name = Column(String(100))
    location = Column(String(100))


class Show(Base):

    __tablename__ = "shows"

    show_id = Column(Integer, primary_key=True, index=True)

    movie_id = Column(
        Integer,
        ForeignKey("movies.movie_id")
    )

    theatre_id = Column(
        Integer,
        ForeignKey("theatres.theatre_id")
    )

    screen_name = Column(String(50))

    show_name = Column(String(50))

    timing = Column(String(50))

    show_date = Column(String(50))

    # GOLD

    gold_seats = Column(Integer)
    gold_price = Column(Integer)

    booked_gold = Column(Integer, default=0)
    cancelled_gold = Column(Integer, default=0)
    remaining_gold = Column(Integer)

    # SILVER

    silver_seats = Column(Integer)
    silver_price = Column(Integer)

    booked_silver = Column(Integer, default=0)
    cancelled_silver = Column(Integer, default=0)
    remaining_silver = Column(Integer)

    # RECLINER

    recliner_seats = Column(Integer)
    recliner_price = Column(Integer)

    booked_recliner = Column(Integer, default=0)
    cancelled_recliner = Column(Integer, default=0)
    remaining_recliner = Column(Integer)

    movie = relationship("Movie")
    theatre = relationship("Theatre")


class Booking(Base):

    __tablename__ = "bookings"

    booking_id = Column(Integer, primary_key=True, index=True)

    customer_name = Column(String(100))

    show_id = Column(
        Integer,
        ForeignKey("shows.show_id")
    )

    seat_type = Column(String(50))

    seats_booked = Column(Integer)

    total_price = Column(Integer)

    booking_status = Column(
        String(20),
        default="BOOKED"
    )

    show = relationship("Show")

# ============================================================
# CREATE TABLES
# ============================================================

Base.metadata.create_all(bind=engine)

# ============================================================
# PYDANTIC SCHEMAS
# ============================================================

class MovieSchema(BaseModel):

    movie_id: int
    movie_name: str
    genre: str
    rating: float
    duration: str


class TheatreSchema(BaseModel):

    theatre_id: int
    theatre_name: str
    location: str


class ShowSchema(BaseModel):

    movie_id: int
    theatre_id: int

    screen_name: str

    show_name: str
    timing: str

    show_date: str

    silver_seats: int
    silver_price: int

    gold_seats: int
    gold_price: int

    recliner_seats: int
    recliner_price: int


class BookingSchema(BaseModel):

    customer_name: str

    show_id: int

    seat_type: str

    seats: int

# ============================================================
# HOME
# ============================================================

@app.get("/")
def home():

    return {
        "message": "Movie Ticket Booking System Using SQLite"
    }

# ============================================================
# 1. ADD MOVIE
# ============================================================

@app.post("/movies")
def add_movie(
    movie: MovieSchema,
    db: Session = Depends(get_db)
):

    existing_movie = db.query(Movie).filter(
        Movie.movie_id == movie.movie_id
    ).first()

    if existing_movie:

        raise HTTPException(
            status_code=400,
            detail="Movie ID Already Exists"
        )

    new_movie = Movie(
        movie_id=movie.movie_id,
        movie_name=movie.movie_name,
        genre=movie.genre,
        rating=movie.rating,
        duration=movie.duration
    )

    db.add(new_movie)

    db.commit()

    return {
        "message": "Movie Added Successfully"
    }

# ============================================================
# 2. GET ALL MOVIES
# ============================================================

@app.get("/movies")
def get_all_movies(
    db: Session = Depends(get_db)
):

    return db.query(Movie).all()

# ============================================================
# 3. GET MOVIE BY ID
# ============================================================

@app.get("/movies/{movie_id}")
def get_movie_by_id(
    movie_id: int,
    db: Session = Depends(get_db)
):

    movie = db.query(Movie).filter(
        Movie.movie_id == movie_id
    ).first()

    if not movie:

        raise HTTPException(
            status_code=404,
            detail="Movie Not Found"
        )

    return movie

# ============================================================
# 4. UPDATE MOVIE
# ============================================================

@app.put("/movies/{movie_id}")
def update_movie(
    movie_id: int,
    updated_movie: MovieSchema,
    db: Session = Depends(get_db)
):

    movie = db.query(Movie).filter(
        Movie.movie_id == movie_id
    ).first()

    if not movie:

        raise HTTPException(
            status_code=404,
            detail="Movie Not Found"
        )

    movie.movie_name = updated_movie.movie_name
    movie.genre = updated_movie.genre
    movie.rating = updated_movie.rating
    movie.duration = updated_movie.duration

    db.commit()

    return {
        "message": "Movie Updated Successfully"
    }

# ============================================================
# 5. DELETE MOVIE
# ============================================================

@app.delete("/movies/{movie_id}")
def delete_movie(
    movie_id: int,
    db: Session = Depends(get_db)
):

    movie = db.query(Movie).filter(
        Movie.movie_id == movie_id
    ).first()

    if not movie:

        raise HTTPException(
            status_code=404,
            detail="Movie Not Found"
        )

    db.delete(movie)

    db.commit()

    return {
        "message": "Movie Deleted Successfully"
    }

# ============================================================
# ADD THEATRE
# ============================================================

@app.post("/theatres")
def add_theatre(
    theatre: TheatreSchema,
    db: Session = Depends(get_db)
):

    new_theatre = Theatre(
        theatre_id=theatre.theatre_id,
        theatre_name=theatre.theatre_name,
        location=theatre.location
    )

    db.add(new_theatre)

    db.commit()

    return {
        "message": "Theatre Added Successfully"
    }

# ============================================================
# ADD SHOW
# ============================================================

@app.post("/shows")
def add_show(
    show: ShowSchema,
    db: Session = Depends(get_db)
):

    movie = db.query(Movie).filter(
        Movie.movie_id == show.movie_id
    ).first()

    if not movie:

        raise HTTPException(
            status_code=404,
            detail="Movie Not Found"
        )

    theatre = db.query(Theatre).filter(
        Theatre.theatre_id == show.theatre_id
    ).first()

    if not theatre:

        raise HTTPException(
            status_code=404,
            detail="Theatre Not Found"
        )

    new_show = Show(

        movie_id=show.movie_id,
        theatre_id=show.theatre_id,

        screen_name=show.screen_name,

        show_name=show.show_name,

        timing=show.timing,

        show_date=show.show_date,

        # SILVER

        silver_seats=show.silver_seats,
        silver_price=show.silver_price,
        booked_silver=0,
        cancelled_silver=0,
        remaining_silver=show.silver_seats,

        # GOLD

        gold_seats=show.gold_seats,
        gold_price=show.gold_price,
        booked_gold=0,
        cancelled_gold=0,
        remaining_gold=show.gold_seats,

        # RECLINER

        recliner_seats=show.recliner_seats,
        recliner_price=show.recliner_price,
        booked_recliner=0,
        cancelled_recliner=0,
        remaining_recliner=show.recliner_seats
    )

    db.add(new_show)

    db.commit()

    return {
        "message": "Show Added Successfully"
    }

# ============================================================
# 6. BOOK MOVIE TICKET
# ============================================================

@app.post("/book-ticket")
def book_ticket(
    booking: BookingSchema,
    db: Session = Depends(get_db)
):

    show = db.query(Show).filter(
        Show.show_id == booking.show_id
    ).first()

    if not show:

        raise HTTPException(
            status_code=404,
            detail="Show Not Found"
        )

    total_price = 0

    if booking.seat_type.lower() == "gold":

        if show.remaining_gold < booking.seats:

            raise HTTPException(
                status_code=400,
                detail="Gold Seats Not Available"
            )

        show.booked_gold += booking.seats
        show.remaining_gold -= booking.seats

        total_price = booking.seats * show.gold_price

    elif booking.seat_type.lower() == "silver":

        if show.remaining_silver < booking.seats:

            raise HTTPException(
                status_code=400,
                detail="Silver Seats Not Available"
            )

        show.booked_silver += booking.seats
        show.remaining_silver -= booking.seats

        total_price = booking.seats * show.silver_price

    elif booking.seat_type.lower() == "recliner":

        if show.remaining_recliner < booking.seats:

            raise HTTPException(
                status_code=400,
                detail="Recliner Seats Not Available"
            )

        show.booked_recliner += booking.seats
        show.remaining_recliner -= booking.seats

        total_price = booking.seats * show.recliner_price

    else:

        raise HTTPException(
            status_code=400,
            detail="Invalid Seat Type"
        )

    new_booking = Booking(

        customer_name=booking.customer_name,

        show_id=booking.show_id,

        seat_type=booking.seat_type,

        seats_booked=booking.seats,

        total_price=total_price
    )

    db.add(new_booking)

    db.commit()

    return {

        "message": "Ticket Booked Successfully",

        "total_price": total_price
    }

# ============================================================
# 7. CANCEL TICKET
# ============================================================

@app.put("/cancel-booking/{booking_id}")
def cancel_booking(
    booking_id: int,
    db: Session = Depends(get_db)
):

    booking = db.query(Booking).filter(
        Booking.booking_id == booking_id
    ).first()

    if not booking:

        raise HTTPException(
            status_code=404,
            detail="Booking Not Found"
        )

    if booking.booking_status == "CANCELLED":

        return {
            "message": "Already Cancelled"
        }

    show = db.query(Show).filter(
        Show.show_id == booking.show_id
    ).first()

    if booking.seat_type.lower() == "gold":

        show.booked_gold -= booking.seats_booked
        show.cancelled_gold += booking.seats_booked
        show.remaining_gold += booking.seats_booked

    elif booking.seat_type.lower() == "silver":

        show.booked_silver -= booking.seats_booked
        show.cancelled_silver += booking.seats_booked
        show.remaining_silver += booking.seats_booked

    elif booking.seat_type.lower() == "recliner":

        show.booked_recliner -= booking.seats_booked
        show.cancelled_recliner += booking.seats_booked
        show.remaining_recliner += booking.seats_booked

    booking.booking_status = "CANCELLED"

    db.commit()

    return {
        "message": "Booking Cancelled Successfully"
    }

# ============================================================
# 8. GET AVAILABLE SHOWS
# ============================================================

@app.get("/available-shows")
def get_available_shows(
    db: Session = Depends(get_db)
):

    return db.query(Show).all()

# ============================================================
# 9. GET ALL BOOKINGS
# ============================================================

@app.get("/bookings")
def get_all_bookings(
    db: Session = Depends(get_db)
):

    return db.query(Booking).all()

# ============================================================
# 10. SEARCH MOVIE BY NAME
# ============================================================

@app.get("/search-movie/{movie_name}")
def search_movie(
    movie_name: str,
    db: Session = Depends(get_db)
):

    movies = db.query(Movie).filter(
        Movie.movie_name.ilike(f"%{movie_name}%")
    ).all()

    if not movies:

        raise HTTPException(
            status_code=404,
            detail="Movie Not Found"
        )

    return movies

# ============================================================
# 11. TOP RATED MOVIES
# ============================================================

@app.get("/top-rated-movies")
def top_rated_movies(
    db: Session = Depends(get_db)
):

    return db.query(Movie).order_by(
        Movie.rating.desc()
    ).all()

# ============================================================
# 12. REMAINING SEATS
# ============================================================

@app.get("/remaining-seats/{show_id}")
def remaining_seats(
    show_id: int,
    db: Session = Depends(get_db)
):

    show = db.query(Show).filter(
        Show.show_id == show_id
    ).first()

    if not show:

        raise HTTPException(
            status_code=404,
            detail="Show Not Found"
        )

    return {

        "Gold Remaining": show.remaining_gold,

        "Silver Remaining": show.remaining_silver,

        "Recliner Remaining": show.remaining_recliner
    }

# ============================================================
# 13. BOOKING HISTORY
# ============================================================

@app.get("/booking-history/{customer_name}")
def booking_history(
    customer_name: str,
    db: Session = Depends(get_db)
):

    history = db.query(Booking).filter(
        Booking.customer_name == customer_name
    ).all()

    if not history:

        raise HTTPException(
            status_code=404,
            detail="No Booking History Found"
        )

    return history

# ============================================================
# 14. TOTAL REVENUE
# ============================================================

@app.get("/total-revenue")
def total_revenue(
    db: Session = Depends(get_db)
):

    bookings = db.query(Booking).filter(
        Booking.booking_status == "BOOKED"
    ).all()

    revenue = 0

    for booking in bookings:

        revenue += booking.total_price

    return {

        "Total Revenue": revenue
    }

# ============================================================
# DELETE SHOW
# ============================================================

@app.delete("/shows/{show_id}")
def delete_show(
    show_id: int,
    db: Session = Depends(get_db)
):

    show = db.query(Show).filter(
        Show.show_id == show_id
    ).first()

    if not show:

        raise HTTPException(
            status_code=404,
            detail="Show Not Found"
        )

    db.delete(show)

    db.commit()

    return {
        "message": "Show Deleted Successfully"
    }