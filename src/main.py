
from src.config import load_config
from src.reddit_scraper import RedditScraper
from src.sentiment_analysis import SentimentAnalyzer
from src.openai_integration import OpenAIIntegration

def main():
    # Load configuration
    openai_api_key = load_config()

    # Initialize Reddit scraper
    subreddits = ["science", "clinicaltrials", "clinicalresearch", "Medical", "PaidStudies", 
                  "askdocs", "cancerresearch", "alzheimers", "MedicalNegligence", "TreatmentComplaints", "SideEffects", "MedicalGore"]
    keywords = ["clinical trial", "research study", "volunteer", "trial", "clinical research","clinical trial risks", "trial failure"]

    scraper = RedditScraper(client_id='your_client_id',
                            client_secret='your_client_secret',
                            user_agent='your_user_agent',
                            subreddits=subreddits,
                            keywords=keywords)
    
    df = scraper.scrape()

    if not df.empty:
        # Perform sentiment analysis
        sentiment_analyzer = SentimentAnalyzer()
        df = sentiment_analyzer.analyze_sentiment(df)

        # Generate personalized messages using OpenAI
        openai_integration = OpenAIIntegration(api_key=openai_api_key)
        df = openai_integration.generate_message(df)

        # Save the updated DataFrame to a CSV file
        df.to_csv("../data/reddit_data_with_personalized_messages.csv", index=False)
        print("Personalized messages generated and saved.")
    else:
        print("No data extracted from subreddits.")

if __name__ == "__main__":
    main()
