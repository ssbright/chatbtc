import openai
from dotenv import load_dotenv
import os 

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")



def generate_text(prompt):
    response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
            {"role": "user", "content": prompt},
        ]
    )
    if len(response['choices'][0]['message']['content']) > 4096:
        # Truncate the response to the maximum length
        response_text = response_text = response['choices'][0]['message']['content'][:4093] + "..."
    else:
        response_text = response['choices'][0]['message']['content']
    #print("This is the message", response_text)
    return response_text

