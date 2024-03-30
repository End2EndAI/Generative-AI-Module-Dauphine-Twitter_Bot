# Generative-AI-Module-Dauphine-Twitter_Bot

### Repository Overview
This project, part of the "Generative AI" course for the Master IASD Executive program at Dauphine-PSL University, demonstrates the use of generative AI in a tool that helps agents in customer service to answer customer's tweets faster.

This project can be reuse for any other use cases, that requires to use company data to generate a text from a user query (chatbot, email, calls, ...).

### Key Components
- `app.py`: The Flask app, containing the backend.
- `notebooks/`:
    - `embed_data.ipynb` : This notebook embeds tweet data into a chromadb vector database using the OpenAI API.
    - `evaluate_tool.ipynb` : This notebook sends data from `twitter_data_clean_eval.csv` through the Flask API to generate responses to customer tweets, comparing them to original tweets for analysis.

### Pre-requisites
Before running this project, ensure you have completed the environment setup as outlined in the [Setup Guide](https://github.com/End2EndAI/Generative-AI-Module-Dauphine/blob/main/resources/Guide_Setup_Environment.md) from the Generative AI module repository.

### Configuration and Setup
1. **OpenAI API Credentials**
   - Create a `config.ini` file in the project root with the following content, replacing `key` with your actual OpenAI API key:
     ```ini
     [OPENAI_API]
     OPENAI_KEY = key
     ```

2. **Data Preparation**
   - Clone the [Generative-AI-Module-Dauphine repository](https://github.com/End2EndAI/Generative-AI-Module-Dauphine).
   - Create a `data/` directory in the Twitter Bot project folder.
   - Copy all CSV files from the Generative-AI-Module-Dauphine repository into the `data/` directory.

3. **Embedding Tweet Data**
   - Navigate to the `notebooks/` directory.
   - Open and run `embed_data.ipynb` in a Jupyter environment. This notebook embeds tweet data into a chromadb vector database using the OpenAI API.

4. **Running the Flask Application**
   - Execute the Flask app to start the server:
     ```sh
     python app.py
     ```

5. **Evaluation and Interaction**
   - Use the `notebooks/evaluate_tool.ipynb` notebook for evaluating the system. This notebook sends data from `twitter_data_clean_eval.csv` through the Flask API to generate responses to customer tweets, comparing them to original tweets for analysis.

### Running the Project
After completing the setup and configuration steps, you can start experimenting with interface, and generate answers for customer's tweets.
This project offers a hands-on opportunity to showcase the practical applications and challenges of generative AI technologies.
