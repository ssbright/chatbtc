import openai
from dotenv import load_dotenv
import os 

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")



def generate_text(prompt):
    response = openai.Completion.create(
        engine="davinci",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.7,
    )
    if len(response.choices[0].text) > 4096:
        # Truncate the response to the maximum length
        response_text = response.choices[0].text[:4093] + "..."
    else:
        response_text = response.choices[0].text
    #print("This is the message", response_text)
    return response_text

