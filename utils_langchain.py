import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import openai
import json
from langchain.memory import ConversationBufferMemory
from langchain.chains import LLMChain
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
import os
# Load environment variables from .env file
load_dotenv()

# Load API keys from environment variables
SERPER_API_KEY = os.getenv("SERPER_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def search_articles(query,max_articles=2):
    """
    Searches for articles related to the query using Serper API.
    Returns a list of dictionaries containing article URLs, headings, and text.
    """
    url = "https://google.serper.dev/search"
    headers = {
        'X-API-KEY': SERPER_API_KEY,  # Use the API key from environment variables
        'Content-Type': 'application/json'
    }
    payload = json.dumps({"q": query})  
    response = requests.post(url,headers=headers,data=payload)
    if response.status_code != 200:
        print(f"Error: Received status code {response.status_code}")
        print(f"Response content: {response.text}")
        return []
    data = response.json()
    articles = []
    
    # implement the search logic - retrieves articles
    for item in data.get("organic", [])[:max_articles]:
        article = {
            "url": item.get("link"),
            "title": item.get("title"),
            "snippet": item.get("snippet"),
        }
        articles.append(article)
    return articles


def fetch_article_content(url,max_content_length=200):
    """
    Fetches the article content, extracting headings and text.
    """
    # implementation of fetching headings and content from the articles
    response = requests.get(url)
    if response.status_code != 200:
        return ""
    
    soup = BeautifulSoup(response.text, 'html.parser')
    content = ""

    for element in soup.find_all(['h1', 'h2', 'h3', 'p']):
        text = element.get_text()
        if len(content)+ len(text)> max_content_length:
            content+=text[:max_content_length-len(content)]
            break
        content+= text+ " "
    return content.strip()



def concatenate_content(articles,max_total_length=50):
    """
    Concatenates the content of the provided articles into a single string.
    """
    full_text = ""
    # formatting + concatenation of the string is implemented here
    for article in articles:
        content = fetch_article_content(article['url'])
        if len(full_text) + len(content) > max_total_length:
            full_text += content[:max_total_length - len(full_text)]
            break
        full_text += content + "\n\n"
    
    return full_text.strip()


openai.api_key = os.getenv("OPENAI_API_KEY")

memory= ConversationBufferMemory(memory_key="chat_history",input_key="input")

template = """You are a helpful assistant.
Based on the following content, answer the query:

{input}


chat_history : {chat_history}
"""
prompt = PromptTemplate(
    input_variables=["input","chat_history"],
    template=template,
)

llm=OpenAI(model_name="gpt-3.5-turbo-16k")
chain = LLMChain(llm=llm, memory=memory,prompt=prompt,verbose=True)

def generate_answer(content, query):
    """
    Generates an answer from the concatenated content using GPT-4.
    The content and the user's query are used to generate a contextual answer.
    """
    # Create the prompt based on the content and the query
    try:
        inputs= f"Content: {content}\nQuery: {query}"
        answer = chain.run({"input":inputs})
        return answer
    except openai.error.RateLimitError:
        print("Error: You have exceeded your current quota. Please check your OpenAI API plan and billing details.")
        return "Error: Quota exceeded. Please check your plan and billing details."
    
    except openai.error.OpenAIError as e:
        # Handle other OpenAI API errors
        print(f"An error occurred: {e}")
        return f"Error: {e}"

    except Exception as e:
        # Handle any other exceptions
        print(f"An unexpected error occurred: {e}")
        return f"Error: {e}"
