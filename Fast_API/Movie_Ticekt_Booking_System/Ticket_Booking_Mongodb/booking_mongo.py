# ============================================================
# 🎬 MOVIE TICKET BOOKING SYSTEM
# FastAPI + MongoDB
# ============================================================

# INSTALL:
# pip install fastapi uvicorn pymongo

# RUN:
# uvicorn main:app --reload

# ============================================================

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pymongo import MongoClient
from bson.objectid import ObjectId

# ============================================================
# MONGODB CONNECTION
# ============================================================

MONGO_URL = "mongodb+srv://shashikumarv860_db_user:shashi2113@shashi.p3tis2s.mongodb.net/movie_booking_db?retryWrites=true&w=majority"

db = MongoClient(MONGO_URL)["movie_bookings_db"]

movies_collection = db["movies"]
theatres_collection = db["theatres"]
shows_collection = db["shows"]
bookings_collection = db["bookings"]

# ============================================================
# FASTAPI APP
# ============================================================

app = FastAPI(
    title="Movie Ticket Booking System MongoDB",
    version="1.0"
)

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

    show_id: int

    movie_id: int

    theatre_id: int

    screen_name: str

    show_name: str

    timing: str

    show_date: str

    # GOLD

    gold_seats: int
    gold_price: int

    # SILVER

    silver_seats: int
    silver_price: int

    # RECLINER

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
        "message": "Movie Ticket Booking System MongoDB"
    }

# ============================================================
# 1. ADD MOVIE
# ============================================================

@app.post("/movies")
def add_movie(movie: MovieSchema):

    existing_movie = movies_collection.find_one(
        {"movie_id": movie.movie_id}
    )

    if existing_movie:

        raise HTTPException(
            status_code=400,
            detail="Movie ID Already Exists"
        )

    movies_collection.insert_one({

        "movie_id": movie.movie_id,

        "movie_name": movie.movie_name,

        "genre": movie.genre,

        "rating": movie.rating,

        "duration": movie.duration
    })

    return {
        "message": "Movie Added Successfully"
    }

# ============================================================
# 2. GET ALL MOVIES
# ============================================================

@app.get("/movies")
def get_all_movies():

    movies = list(
        movies_collection.find({}, {"_id": 0})
    )

    return movies

# ============================================================
# 3. GET MOVIE BY ID
# ============================================================

@app.get("/movies/{movie_id}")
def get_movie_by_id(movie_id: int):

    movie = movies_collection.find_one(
        {"movie_id": movie_id},
        {"_id": 0}
    )

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
    movie: MovieSchema
):

    existing_movie = movies_collection.find_one(
        {"movie_id": movie_id}
    )

    if not existing_movie:

        raise HTTPException(
            status_code=404,
            detail="Movie Not Found"
        )

    movies_collection.update_one(

        {"movie_id": movie_id},

        {
            "$set": {

                "movie_name": movie.movie_name,

                "genre": movie.genre,

                "rating": movie.rating,

                "duration": movie.duration
            }
        }
    )

    return {
        "message": "Movie Updated Successfully"
    }

# ============================================================
# 5. DELETE MOVIE
# ============================================================

@app.delete("/movies/{movie_id}")
def delete_movie(movie_id: int):

    movie = movies_collection.find_one(
        {"movie_id": movie_id}
    )

    if not movie:

        raise HTTPException(
            status_code=404,
            detail="Movie Not Found"
        )

    movies_collection.delete_one(
        {"movie_id": movie_id}
    )

    return {
        "message": "Movie Deleted Successfully"
    }

# ============================================================
# 6. ADD THEATRE
# ============================================================

@app.post("/theatres")
def add_theatre(theatre: TheatreSchema):

    theatres_collection.insert_one({

        "theatre_id": theatre.theatre_id,

        "theatre_name": theatre.theatre_name,

        "location": theatre.location
    })

    return {
        "message": "Theatre Added Successfully"
    }

# ============================================================
# 7. ADD SHOW
# ============================================================

@app.post("/shows")
def add_show(show: ShowSchema):

    movie = movies_collection.find_one(
        {"movie_id": show.movie_id}
    )

    if not movie:

        raise HTTPException(
            status_code=404,
            detail="Movie Not Found"
        )

    theatre = theatres_collection.find_one(
        {"theatre_id": show.theatre_id}
    )

    if not theatre:

        raise HTTPException(
            status_code=404,
            detail="Theatre Not Found"
        )

    shows_collection.insert_one({

        "show_id": show.show_id,

        "movie_id": show.movie_id,

        "theatre_id": show.theatre_id,

        "screen_name": show.screen_name,

        "show_name": show.show_name,

        "timing": show.timing,

        "show_date": show.show_date,

        # GOLD

        "gold_seats": show.gold_seats,

        "gold_price": show.gold_price,

        "booked_gold": 0,

        "cancelled_gold": 0,

        "remaining_gold": show.gold_seats,

        # SILVER

        "silver_seats": show.silver_seats,

        "silver_price": show.silver_price,

        "booked_silver": 0,

        "cancelled_silver": 0,

        "remaining_silver": show.silver_seats,

        # RECLINER

        "recliner_seats": show.recliner_seats,

        "recliner_price": show.recliner_price,

        "booked_recliner": 0,

        "cancelled_recliner": 0,

        "remaining_recliner": show.recliner_seats
    })

    return {
        "message": "Show Added Successfully"
    }

# ============================================================
# 8. BOOK MOVIE TICKET
# ============================================================

@app.post("/book-ticket")
def book_ticket(booking: BookingSchema):

    show = shows_collection.find_one(
        {"show_id": booking.show_id}
    )

    if not show:

        raise HTTPException(
            status_code=404,
            detail="Show Not Found"
        )

    total_price = 0

    # GOLD

    if booking.seat_type.lower() == "gold":

        if show["remaining_gold"] < booking.seats:

            raise HTTPException(
                status_code=400,
                detail="Gold Seats Not Available"
            )

        total_price = booking.seats * show["gold_price"]

        shows_collection.update_one(

            {"show_id": booking.show_id},

            {
                "$inc": {

                    "booked_gold": booking.seats,

                    "remaining_gold": -booking.seats
                }
            }
        )

    # SILVER

    elif booking.seat_type.lower() == "silver":

        if show["remaining_silver"] < booking.seats:

            raise HTTPException(
                status_code=400,
                detail="Silver Seats Not Available"
            )

        total_price = booking.seats * show["silver_price"]

        shows_collection.update_one(

            {"show_id": booking.show_id},

            {
                "$inc": {

                    "booked_silver": booking.seats,

                    "remaining_silver": -booking.seats
                }
            }
        )

    # RECLINER

    elif booking.seat_type.lower() == "recliner":

        if show["remaining_recliner"] < booking.seats:

            raise HTTPException(
                status_code=400,
                detail="Recliner Seats Not Available"
            )

        total_price = booking.seats * show["recliner_price"]

        shows_collection.update_one(

            {"show_id": booking.show_id},

            {
                "$inc": {

                    "booked_recliner": booking.seats,

                    "remaining_recliner": -booking.seats
                }
            }
        )

    else:

        raise HTTPException(
            status_code=400,
            detail="Invalid Seat Type"
        )

    booking_id = bookings_collection.count_documents({}) + 1

    bookings_collection.insert_one({

        "booking_id": booking_id,

        "customer_name": booking.customer_name,

        "show_id": booking.show_id,

        "seat_type": booking.seat_type,

        "seats_booked": booking.seats,

        "total_price": total_price,

        "booking_status": "BOOKED"
    })

    return {

        "message": "Ticket Booked Successfully",

        "booking_id": booking_id,

        "total_price": total_price
    }

# ============================================================
# 9. CANCEL TICKET
# ============================================================

@app.put("/cancel-booking/{booking_id}")
def cancel_booking(booking_id: int):

    booking = bookings_collection.find_one(
        {"booking_id": booking_id}
    )

    if not booking:

        raise HTTPException(
            status_code=404,
            detail="Booking Not Found"
        )

    if booking["booking_status"] == "CANCELLED":

        return {
            "message": "Already Cancelled"
        }

    show = shows_collection.find_one(
        {"show_id": booking["show_id"]}
    )

    # GOLD

    if booking["seat_type"].lower() == "gold":

        shows_collection.update_one(

            {"show_id": booking["show_id"]},

            {
                "$inc": {

                    "booked_gold": -booking["seats_booked"],

                    "cancelled_gold": booking["seats_booked"],

                    "remaining_gold": booking["seats_booked"]
                }
            }
        )

    # SILVER

    elif booking["seat_type"].lower() == "silver":

        shows_collection.update_one(

            {"show_id": booking["show_id"]},

            {
                "$inc": {

                    "booked_silver": -booking["seats_booked"],

                    "cancelled_silver": booking["seats_booked"],

                    "remaining_silver": booking["seats_booked"]
                }
            }
        )

    # RECLINER

    elif booking["seat_type"].lower() == "recliner":

        shows_collection.update_one(

            {"show_id": booking["show_id"]},

            {
                "$inc": {

                    "booked_recliner": -booking["seats_booked"],

                    "cancelled_recliner": booking["seats_booked"],

                    "remaining_recliner": booking["seats_booked"]
                }
            }
        )

    bookings_collection.update_one(

        {"booking_id": booking_id},

        {
            "$set": {
                "booking_status": "CANCELLED"
            }
        }
    )

    return {
        "message": "Booking Cancelled Successfully"
    }

# ============================================================
# 10. GET AVAILABLE SHOWS
# ============================================================

@app.get("/available-shows")
def available_shows():

    shows = list(
        shows_collection.find({}, {"_id": 0})
    )

    return shows

# ============================================================
# 11. GET ALL BOOKINGS
# ============================================================

@app.get("/bookings")
def get_all_bookings():

    bookings = list(
        bookings_collection.find({}, {"_id": 0})
    )

    return bookings

# ============================================================
# 12. SEARCH MOVIE BY NAME
# ============================================================

@app.get("/search-movie/{movie_name}")
def search_movie(movie_name: str):

    movies = list(

        movies_collection.find(

            {
                "movie_name": {
                    "$regex": movie_name,
                    "$options": "i"
                }
            },

            {"_id": 0}
        )
    )

    if not movies:

        raise HTTPException(
            status_code=404,
            detail="Movie Not Found"
        )

    return movies

# ============================================================
# 13. TOP RATED MOVIES
# ============================================================

@app.get("/top-rated-movies")
def top_rated_movies():

    movies = list(

        movies_collection.find(
            {},
            {"_id": 0}
        ).sort("rating", -1)
    )

    return movies

# ============================================================
# 14. REMAINING SEATS
# ============================================================

@app.get("/remaining-seats/{show_id}")
def remaining_seats(show_id: int):

    show = shows_collection.find_one(
        {"show_id": show_id}
    )

    if not show:

        raise HTTPException(
            status_code=404,
            detail="Show Not Found"
        )

    return {

        "Gold Remaining": show["remaining_gold"],

        "Silver Remaining": show["remaining_silver"],

        "Recliner Remaining": show["remaining_recliner"]
    }

# ============================================================
# 15. BOOKING HISTORY
# ============================================================

@app.get("/booking-history/{customer_name}")
def booking_history(customer_name: str):

    history = list(

        bookings_collection.find(

            {"customer_name": customer_name},

            {"_id": 0}
        )
    )

    if not history:

        raise HTTPException(
            status_code=404,
            detail="No Booking History Found"
        )

    return history

# ============================================================
# 16. TOTAL REVENUE
# ============================================================

@app.get("/total-revenue")
def total_revenue():

    bookings = list(

        bookings_collection.find(

            {"booking_status": "BOOKED"},

            {"_id": 0}
        )
    )

    revenue = 0

    for booking in bookings:

        revenue += booking["total_price"]

    return {

        "Total Revenue": revenue
    }

# ============================================================
# 17. DELETE SHOW
# ============================================================

@app.delete("/shows/{show_id}")
def delete_show(show_id: int):

    show = shows_collection.find_one(
        {"show_id": show_id}
    )

    if not show:

        raise HTTPException(
            status_code=404,
            detail="Show Not Found"
        )

    shows_collection.delete_one(
        {"show_id": show_id}
    )

    return {
        "message": "Show Deleted Successfully"
    }