import cohere
import requests

# API keys - replace with your actual API keys.
# Without valid keys, the code will not work.
COHERE_API_KEY = "your Cohere API key"
SERPAPI_KEY = "your SerpAPI API key"

# Cohere initialization
co = cohere.Client(COHERE_API_KEY)

# retrieval function (using SerpAPI)
def retrieve_information(query):
    url = "https://serpapi.com/search"
    params = {
        "q": query,
        "api_key": SERPAPI_KEY,
        "engine": "google"
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        results = response.json()
        # Extract the first 3 snippets from the search results
        snippets = [result.get("snippet", "") for result in results.get("organic_results", [])[:3]]
        return " ".join(snippets)
    else:
        return "No information found."

# Function for generation (using Cohere) 
def generate_response(query, context):
    prompt = f"Query: {query}\nContext: {context}\nAnswer:"
    response = co.generate(
        model="command",  # Use Cohere's command model
        prompt=prompt,
        max_tokens=500,  # Answer length limit 
        temperature=0.7  # Answer "creativity" level
    )
    return response.generations[0].text

# Principal RAG function
def rag_model(query):
    # Retrieval step
    context = retrieve_information(query)
    print(f"Context retrieved: {context}")
    # Generation step
    response = generate_response(query, context)
    return response

# Example of usage  
# Feel free to change the query as you like.
query = "Who is the 47th president of United States?"
answer = rag_model(query)
print(f"Answer: {answer}")
