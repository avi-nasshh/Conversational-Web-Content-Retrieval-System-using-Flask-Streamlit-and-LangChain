
import streamlit as st
import requests

st.title("LLM-based RAG Search")

# Input for user query
query = st.text_input("Enter your query:")

if st.button("Search"):
    # Make a POST request to the Flask API
    print("accessing ", "<Flask app string>", " with query ", query)
    flask_api_url = "http://localhost:5001/query_endpoint"  # URL of your Flask backend
    payload = {"query": query}
    
    # call the flask app and get response

    # implement the flask call here
    try: 
        st.write("Starting the API call...")

        response = requests.post(flask_api_url,json=payload)
        st.write("API call completed.")
        if response.status_code == 200:
            # Display the generated answer
            answer = response.json().get('answer', "No answer received.")
            st.write("Answer:", answer)
        else:
            st.write("In else section")
            st.error(f"Error: {response.status_code}")
            st.write(response.text)  # Display the response content for debugging
    except requests.exceptions.RequestException as e:
        st.error(f"Request failed: {e}")
