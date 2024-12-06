import json
import mysql.connector
from flask import Flask, jsonify, request
from flask_cors import CORS
import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()


API_KEY = os.getenv('API_KEY')


app = Flask(__name__)

CORS(app)


genai.configure(api_key=API_KEY)

generation_config = {
    "temperature": 0.8,
    "top_p": 0.9,
    "top_k": 80,
    "max_output_tokens": 1500,
    "response_mime_type": "application/json",  
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)


def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST'),  
            database=os.getenv('DB_NAME'),  
            user=os.getenv('DB_USER'),  
            password=os.getenv('DB_PASSWORD')  )
        return connection
    except mysql.connector.Error as e:
        print(f"Error connecting to the database: {e}")
        return None

 
@app.route('/', methods=['POST'])
def get_quiz():
    
    data = request.json

    input_data = data.get('input')
    question_distribution = data.get('questionDistribution')
    difficulty = data.get('selectedDifficulty')

    prompt = f"""
    You are an assistant for a learning platform. Your job is to analyze the provided text or topic and generate questions based on the topic. Please generate the questions (in language text is provided). If it says for example "0 multiplechoice questions" using the following structure:

    {question_distribution.get('multipleChoice')} multiple-choice questions (A B C D). Format each question like this:
    "multipleChoice": [
    {{
        "question": "What is the capital of France?",
        "options": {{ "A": "Berlin", "B": "Madrid", "C": "Paris", "D": "Rome" }},
        "correct": "C"
    }}
    ],
    {question_distribution.get('trueFalse')} true or false questions. Format each question like this:
    "trueFalse": [
    {{
        "question": "The sky is blue.",
        "correct": "true"
    }}
    ],
    {question_distribution.get('openQuestions')} open questions. Format each question like this:
    "openQuestions": [
    {{
        "question": "Explain the theory of relativity.",
        "suggestedAnswer": "The theory of relativity is ..."
    }}
    ],
    {question_distribution.get('fillTheGaps')} fill-the-gaps questions. Format each like this:
    "fillTheGaps": [
    {{
        "text": "The quick ___ fox jumps over the ___ dog.",
        "options": {{
            "gap1": {{ "A": "brown", "B": "black", "C": "white" }},
            "gap2": {{ "A": "lazy", "B": "fast", "C": "sleepy" }}
        }},
        "correct": ["A", "A"]
    }}
    ]
    Please ensure the response is in **valid JSON** format and does not contain any extra explanations or characters. There are 3 levels of quiz difficulty: easy (treat as normal) - simple questions but creative; normal (treat as hard) - more intermediate, specific but creative questions that require effort; hard (treat as very hard) - very specific creative non-generic questions, challenging, very intermediate. User has chosen: {difficulty}. Here is the topic: "{input_data}"
    """

    chat_session = model.start_chat()
    response = chat_session.send_message(prompt)

    quiz_json = response.text
    try:
        quiz_data = json.loads(quiz_json)
    except json.JSONDecodeError as e:
        # Raise an error if failed
        print(f"JSON decoding error: {e}")
        return jsonify({"error": "Failed to decode JSON response"}), 500

    # Save data to database
    connection = get_db_connection()
    if connection is None:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor()
        cursor.execute(
            """
            INSERT INTO quizzes (input_data, question_distribution, difficulty, quiz_response)
            VALUES (%s, %s, %s, %s)
            """,
            (input_data, json.dumps(question_distribution), difficulty, json.dumps(quiz_data))
        )
        connection.commit()
    except mysql.connector.Error as e:
        print(f"Error inserting data into database: {e}")
        connection.rollback()
        return jsonify({"error": "Failed to save quiz data"}), 500
    finally:
        cursor.close()
        connection.close()

    # Return the quiz data to the client
    return jsonify(quiz_data)


# Run the Flask app!
if __name__ == '__main__':
    app.run(debug=True)
