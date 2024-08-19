
import praw
import prawcore
import time
import pandas as pd

class RedditScraper:
    def __init__(self, client_id, client_secret, user_agent, subreddits, keywords):
        self.reddit = praw.Reddit(client_id=client_id,
                                  client_secret=client_secret,
                                  user_agent=user_agent)
        self.subreddits = subreddits
        self.keywords = keywords
        self.data = []

    def check_keywords(self, text):
        return any(keyword in text.lower() for keyword in self.keywords)

    def process_submission(self, submission, subreddit_name, category):
        if self.check_keywords(submission.title) or self.check_keywords(submission.selftext):
            post_author = submission.author.name if submission.author else "[deleted]"
            post_title = submission.title
            post_id = submission.id
            post_created_utc = submission.created_utc

            submission.comments.replace_more(limit=0)  # Avoid pagination issues

            for comment in submission.comments.list():
                try:
                    comment_created_utc = comment.created_utc
                    
                    self.data.append({
                        "Subreddit": subreddit_name,
                        "Category": category,
                        "Post_ID": post_id,
                        "Post_Author": post_author,
                        "Post_Title": post_title,
                        "Post_Created_UTC": post_created_utc,
                        "Comment_Created_UTC": comment_created_utc,
                    })
                except AttributeError:
                    print(f"Error processing comment in submission: {submission.id}")

    def scrape(self):
        for subreddit_name in self.subreddits:
            try:
                subreddit = self.reddit.subreddit(subreddit_name)
                
                for category, method in [('hot', subreddit.hot),
                                         ('top', subreddit.top),
                                         ('controversial', subreddit.controversial),
                                         ('new', subreddit.new)]:
                    try:
                        for submission in method(limit=5):
                            self.process_submission(submission, subreddit_name, category)
                    except AttributeError:
                        print(f"Error processing {category} submission in subreddit: {subreddit_name}")

            except prawcore.exceptions.Forbidden as e:
                print(f"Access forbidden for subreddit '{subreddit_name}': {e}")
            except Exception as e:
                print(f"Unexpected error for subreddit '{subreddit_name}': {e}")
            
            time.sleep(2)  # Sleep between subreddits to avoid rate limits

        return pd.DataFrame(self.data)
