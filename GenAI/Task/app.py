import os
from datetime import datetime
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import database

# Load environment variables from local .env
base_dir = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(base_dir, '.env'))

# Verify API key is present
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

try:
    from google import genai
    # Initialize Google GenAI client
    if GEMINI_API_KEY:
        ai_client = genai.Client(api_key=GEMINI_API_KEY)
    else:
        ai_client = None
        print("WARNING: GEMINI_API_KEY is not set in environment.")
except ImportError:
    ai_client = None
    print("WARNING: google-genai package is not installed or import failed.")

def generate_content_with_fallback(prompt):
    """Utility to generate content using fallback models in case of rate limits/quota exhaustion."""
    if not ai_client:
        raise ValueError("Gemini client is not initialized.")
        
    models = [
        'gemini-3.5-flash',
        'gemini-2.5-flash',
        'gemini-2.0-flash-lite',
        'gemini-2.5-flash-lite',
        'gemini-flash-latest',
        'gemini-3-flash-preview'  
    ]
    last_err = None
    for model in models:
        try:
            print(f"Querying Gemini model: {model}")
            response = ai_client.models.generate_content(
                model=model,
                contents=prompt
            )
            return response
        except Exception as e:
            err_str = str(e)
            print(f"Error with model {model}: {err_str}")
            last_err = e
            # If rate limited or quota exhausted, try the next model
            if "429" in err_str or "RESOURCE_EXHAUSTED" in err_str:
                continue
            # If the API key itself is invalid, stop immediately
            if "API_KEY_INVALID" in err_str or "API key not valid" in err_str:
                raise
            # Otherwise try next model as a safety net
            continue
    raise last_err

# Initialize Flask with paths relative to the root task folder
template_dir = os.path.join(base_dir, 'client', 'templates')
static_dir = os.path.join(base_dir, 'client', 'static')

app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
app.secret_key = 'movie_chatbot_secure_session_key'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    if not ai_client:
        return jsonify({
            'response': "Database chatbot is running in offline mode because the Gemini API key is missing or the google-genai library is not loaded. Please set GEMINI_API_KEY in the .env file.",
            'sql_query': None,
            'success': False
        })
        
    data = request.json or {}
    user_message = data.get('message', '').strip()
    
    if not user_message:
        return jsonify({'response': "Please enter a message.", 'success': False})
        
    # Get database schema structure for context
    schema_info = database.get_schema_info()
    current_time_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # ----------------------------------------------------
    # STEP 1: Translate User Query to read-only SQL
    # ----------------------------------------------------
    sql_generation_prompt = f"""
You are a database translation engine for a movie ticketing MySQL database.
Your job is to translate a user's natural language question into a SINGLE valid, read-only MySQL SELECT query.

### DATABASE SCHEMA:
{schema_info}

Current system date/time: {current_time_str}

### INSTRUCTIONS:
1. ONLY return the raw SQL query. Do NOT wrap it in markdown code block formatting (like ```sql ... ```). Do not include any explanation or extra text.
2. The query must be strictly read-only. Use only SELECT, SHOW, DESCRIBE, or EXPLAIN.
3. If the user's request requires modifying the database (e.g., booking a ticket, adding a user, updating a movie rating, deleting a showtime, cancelling a booking), do NOT perform the modification. Instead, write a SELECT query to check the details or respond with the exact word "UNSUPPORTED" if it's purely a modification command.
4. If the user's question is completely unrelated to the movies database, return the exact word "UNSUPPORTED".
5. Use proper JOIN statements (e.g., join showtimes with movies on showtimes.movie_id = movies.id).
6. Date values are in 'YYYY-MM-DD' format. Time values are in 'HH:MM' (24-hour format). If the user refers to "today", "tomorrow", or "next week", write queries relative to the current system date: {datetime.now().strftime('%Y-%m-%d')}.
7. Limit results to 20 maximum unless asked for more, to prevent overloading.

User Question: "{user_message}"
SQL Query:"""

    try:
        # Request Gemini to generate the SQL query with fallback model support
        sql_response = generate_content_with_fallback(sql_generation_prompt)
        
        generated_sql = sql_response.text.strip()
        
        # Clean any backticks or markdown if the LLM outputted them anyway
        if generated_sql.startswith("```"):
            lines = generated_sql.splitlines()
            if len(lines) > 2:
                # Remove first line (like ```sql) and last line (like ```)
                generated_sql = "\n".join(lines[1:-1]).strip()
        
        # Check if LLM determined this was unsupported/write action
        if "UNSUPPORTED" in generated_sql.upper():
            return handle_unsupported_or_write(user_message)
            
        print(f"Generated SQL: {generated_sql}")
        
        # ----------------------------------------------------
        # STEP 2: Execute query safely on MySQL database
        # ----------------------------------------------------
        try:
            db_results = database.execute_read_query(generated_sql)
            query_success = True
            error_message = None
        except PermissionError as pe:
            # Blocked by database.py safety check
            print(f"Safety Block: {pe}")
            return jsonify({
                'response': "For security reasons, I am only authorized to answer questions and look up records. I cannot make any modifications (such as booking, adding, updating, or deleting data) to the database.",
                'sql_query': generated_sql,
                'success': True
            })
        except Exception as e:
            # SQL execution error
            print(f"SQL Error: {e}")
            query_success = False
            db_results = []
            error_message = str(e)
            
        # ----------------------------------------------------
        # STEP 3: Formulate final response based on results
        # ----------------------------------------------------
        if query_success:
            answer_prompt = f"""
You are the AI Chatbot helper for a Movie Ticketing MySQL Database.
Answer the user's question using the SQL query and the raw database results provided below.

User Question: "{user_message}"
SQL Query Executed: {generated_sql}
Database Results (JSON): {db_results}

### INSTRUCTIONS:
1. Explain the results in a friendly, conversational, and natural way.
2. If the results list shows empty ([]) or no results, explain that politely (e.g. "I checked the schedule, but there are no showtimes for that movie today.").
3. Do not invent any records or details. Use only the data returned from the database.
4. Format prices in USD ($) or appropriate local currency (e.g. if the price value is 12.00, display it as $12.00).
5. If the user asked to perform an update or make a booking, remind them that you are a read-only assistant, but provide the details they queried (e.g. "I can't book this for you, but there are 5 seats left for Dune at 6:30 PM if you want to book it on our website!").
6. Keep your answers concise, clean, and beautifully structured. Use bullet points or tables where appropriate.
"""
        else:
            answer_prompt = f"""
You are the AI Chatbot helper for a Movie Ticketing MySQL Database.
The system attempted to query the database to answer the user's question, but a SQL database error occurred.

User Question: "{user_message}"
SQL Query Attempted: {generated_sql}
Database Error: {error_message}

### INSTRUCTIONS:
1. Explain politely that an error occurred while searching the database.
2. Mention what you were trying to find (based on the attempted SQL query) and explain why it might have failed.
3. Suggest how the user might rephrase their question.
4. Do NOT show raw code trackbacks, just a friendly message.
"""

        conversational_response = generate_content_with_fallback(answer_prompt)
        
        return jsonify({
            'response': conversational_response.text.strip(),
            'sql_query': generated_sql,
            'success': True
        })
        
    except Exception as general_err:
        print(f"General App Error: {general_err}")
        return jsonify({
            'response': f"An error occurred in processing your request: {general_err}",
            'sql_query': None,
            'success': False
        })

def handle_unsupported_or_write(user_message: str):
    """Fallback handler for requests that represent database write actions or out-of-scope topics."""
    prompt = f"""
You are the AI Chatbot helper for a Movie Ticketing MySQL Database.
The user is asking a question that either requires database modifications (like booking a ticket, modifying profiles, adding movies, deleting showtimes) or is completely unrelated to the movies ticketing database.

User Message: "{user_message}"

### INSTRUCTIONS:
1. Explain politely that you are a read-only database query assistant. You can retrieve and explain information from the database but you cannot perform updates, cancellations, bookings, or additions.
2. If they are trying to book a ticket, guide them to use the main web booking interface instead, while summarizing what information they can query from you (e.g. showtimes, movie details, theater locations, availability).
3. If the question is completely unrelated, bring them back on topic politely.
"""
    response = generate_content_with_fallback(prompt)
    return jsonify({
        'response': response.text.strip(),
        'sql_query': None,
        'success': True
    })

if __name__ == '__main__':
    # Get port from environment or default to 5000 as requested
    port = int(os.getenv("PORT", 5000))
    print(f"Starting Chatbot Server on http://127.0.0.1:{port}")
    app.run(host='127.0.0.1', port=port, debug=True)
