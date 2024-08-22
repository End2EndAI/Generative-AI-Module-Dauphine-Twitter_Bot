import configparser
from flask import Flask, request, jsonify, render_template
from openai import OpenAI
import chromadb
import chromadb.utils.embedding_functions as embedding_functions

# Load configurations
def load_config(section, key):
    """
    Load a specific configuration value from config.ini.

    :param section: The section in the config file.
    :param key: The key within the section.
    :return: The value of the specified key.
    """
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config.get(section, key)

# Initialize OpenAI API client
openai_api_key = load_config('OPENAI_API', 'OPENAI_KEY')
client_openai = OpenAI(api_key=openai_api_key)

# Flask application initialization
app = Flask(__name__)

# ChromaDB client setup
def setup_chromadb():
    """
    Setup and return a ChromaDB collection instance.

    :return: A ChromaDB collection instance.
    """
    openai_ef = embedding_functions.OpenAIEmbeddingFunction(
                    api_key=openai_api_key,
                    model_name="text-embedding-3-small"
                )
    client = chromadb.PersistentClient(path="chromadb")
    collection = client.get_or_create_collection(
        name="tweet_amazon_collection",
        embedding_function=openai_ef,
        metadata={"hnsw:space": "cosine"}
    )
    return collection

collection = setup_chromadb()

# Prompt generation for replies
def create_prompt(input_text, similar_customer_tweet, similar_company_tweet):
    """
    Creates a prompt for the GPT model based on input and similar tweets.

    :param input_text: The original tweet text.
    :param similar_customer_tweet: Similar customer tweet text.
    :param similar_company_tweet: Company's response to the similar customer tweet.
    :return: A formatted string to be used as a prompt for the GPT model.
    """
    return f"""\
    ## CONTEXT ##
    You are an AI assistant for a company called Amazon. You are in a team of agents in customer service that answers customers messages on Twitter.

    ################

    ## OBJECTIVES ##
    I want you to reply to a customer's tweet, inspiring from similar conversation between customers and agents. Use this step-by-step process:

    1. CUSTOMER_TWEET: Analyze the provided customer's message on Twitter you have to reply.
    2. SIMILAR_TWEETS: Analyze the provided similar customer's tweet and the reply from our agent.  
    3. REPLY: Reply [CUSTOMER_TWEET] using relevant information in [SIMILAR_TWEETS] in the same style and format. If there is a link in [SIMILAR_TWEETS], use it in the response.

    ################

    ## RESPONSE ##
    Write the tweet [REPLY] directly. Do not write the whole analysis.

    ################

    ## DATA ##

    <CUSTOMER_TWEET>
    {input_text}
    </CUSTOMER_TWEET>

    <SIMILAR_TWEETS>
    [Customer]:
    {similar_customer_tweet}

    [Agent]:
    {similar_company_tweet}
    </SIMILAR_TWEETS>

    [REPLY]:\
    """

# Retrieve similar tweets
def get_similar_tweet(input_text, n=1):
    """
    Retrieve similar tweets from the ChromaDB collection.

    :param input_text: The input tweet text.
    :param n: Number of similar tweets to retrieve.
    :return: A tuple containing lists of customer tweets and company responses.
    """
    retrieved = collection.query(query_texts=[input_text], n_results=n)
    customer_tweets = retrieved['documents'][0]
    metadatas = retrieved['metadatas'][0]
    company_tweets = [x['company_tweet'] for x in metadatas]
    return customer_tweets, company_tweets

# Generate answer based on similar tweets
def generate_answer(input_text):
    """
    Generate a response to the input tweet using a similar conversation.

    :param input_text: The input tweet text.
    :return: A tuple containing the AI-generated answer and similar tweets.
    """
    customer_tweets, company_tweets = get_similar_tweet(input_text, n=1)
    similar_customer_tweet = customer_tweets[0]
    similar_company_tweet = company_tweets[0]
    prompt = create_prompt(input_text, similar_customer_tweet, similar_company_tweet)
    messages = [{"role": "user", "content": prompt}]
    response = client_openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        temperature=0.7  # Adjust as needed
    )
    return response.choices[0].message.content, similar_customer_tweet, similar_company_tweet

@app.route('/')
def home():
    """Serve the homepage."""
    return render_template("index.html")

@app.route('/generate', methods=['POST'])
def generate():
    """Endpoint to generate a tweet reply."""
    data = request.json
    input_text = data.get('input_text', '')
    if not input_text:
        return jsonify({"error": "input_text is required"}), 400
    answer, similar_customer_tweet, similar_company_tweet = generate_answer(input_text)
    return jsonify({"response": answer, "similar_customer_tweet": similar_customer_tweet, "similar_company_tweet": similar_company_tweet})

if __name__ == '__main__':
    app.run(debug=False)  # Set debug=False for production
