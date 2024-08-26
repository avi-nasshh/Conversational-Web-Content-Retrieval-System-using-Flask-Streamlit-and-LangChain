
from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv
from utils_langchain import search_articles, concatenate_content, generate_answer
from flask_cors import CORS
import logging

# Set up basic logging
logging.basicConfig(level=logging.DEBUG)

# Load environment variables from .env file
load_dotenv()
app = Flask(__name__)
CORS(app)

@app.route('/query_endpoint', methods=['POST'])
def handle_query():
    """
    Handles the POST request to '/query'. Extracts the query from the request,
    processes it through the search, concatenate, and generate functions,
    and returns the generated answer.
    """
    try:
        user_query = request.json.get("query")
        if not user_query:
                logging.error("No query provided by the user.")
                return jsonify({"error": "No query provided"}), 400

        
        # get the data/query from streamlit app
        logging.info(f"Received query: {user_query}")
        
        # Step 1: Search and scrape articles based on the query
        logging.info("Step 1: Searching articles")
        articles = search_articles(user_query)
        if not articles:
            logging.error("No articles found for the given query.")
            return jsonify({"error": "No articles found"}), 500
        
        # Step 2: Concatenate content from the scraped articles
        logging.info("Step 2: Concatenating content")
        full_text = concatenate_content(articles)

        logging.info("Step 3: Generating answer")
        answer = generate_answer(full_text, user_query)
        if not answer:
            logging.error("Failed to generate an answer from the provided content.")
            return jsonify({"error": "Failed to generate answer"}), 500
        # return the jsonified text back to streamlit
        return jsonify({"answer": answer})
    
    except Exception as e:
        logging.exception("An error occurred while processing the query.")
        return jsonify({"error": "Internal Server Error", "details": str(e)}), 500

if __name__ == '__main__':
    app.run(host='localhost', port=5001)
