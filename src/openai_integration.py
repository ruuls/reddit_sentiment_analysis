
import openai
import pandas as pd

class OpenAIIntegration:
    def __init__(self, api_key):
        openai.api_key = api_key

    def generate_message(self, df):
        base_prompt = (
            "There is a clinical trial happening at Virginia Tech, Moss Arts Center. "
            "Generate a personalized message to invite the participant who has commented the following on Reddit to the clinical trial.\n"
            'Comment: "{comment}"\n\n'
            "This was the comment by the participant. "
        )
        
        positive_scores = ['Positive']
        neutral_scores = ['Neutral']
        negative_scores = ['Negative']

        personalized_messages = []

        for idx, row in df.iterrows():
            comment = row["Comment_Body"]
            score = str(row["Sentiment"])

            if score == 'Positive':
                prompt = (
                    base_prompt.format(comment=comment) +
                    "The participant seems very enthusiastic and positive about the topic. "
                    "Generate a highly encouraging and motivating message that emphasizes the positive impact they can have by joining the clinical trial."
                )
            elif score == 'Neutral':
                prompt = (
                    base_prompt.format(comment=comment) +
                    "The participant appears neutral and is likely considering their options. "
                    "Generate an informative and balanced message that provides details to help them make an informed decision about participating in the clinical trial."
                )
            elif score == 'Negative':
                prompt = (
                    base_prompt.format(comment=comment) +
                    "The participant has expressed concerns or a negative sentiment. "
                    "Generate a reassuring message that addresses their concerns directly, highlights the incentives, and emphasizes the safety and benefits of participating in the clinical trial."
                )
            else:
                prompt = None

            if prompt:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt}]
                )

                try:
                    if len(response.choices) > 0:
                        first_choice = response.choices[0]
                        personalized_message = first_choice.message['content']
                        personalized_messages.append((idx, personalized_message))
                    else:
                        personalized_messages.append((idx, "No message generated"))
                except (AttributeError, IndexError) as e:
                    print(f"Error extracting personalized message: {e}")
                    personalized_messages.append((idx, "Error generating message"))

        personalized_df = pd.DataFrame(personalized_messages, columns=["Index", "Personalized_Message"])
        df = df.merge(personalized_df, left_index=True, right_on="Index")
        return df
