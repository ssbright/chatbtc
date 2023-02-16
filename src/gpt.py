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
    message = response.choices[0].text.strip()
    print("This is the message", message)
    return message

