from app import app, create_tables

if __name__ == '__main__':
    create_tables()
    print("Starting Movie Ticket Booking Server on http://127.0.0.1:5000 ...")
    app.run(debug=True, port=5000)
