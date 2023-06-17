import openai
import dotenv
import os

dotenv.load_dotenv()
openai.api_key = os.environ.get("API_KEY")

output = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Who won the world series in 2020?"},
        {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
        {"role": "user", "content": "Where was it played?"}, 
        {"role": "assistant", "content": "The 2020 World Series was played at Globe Life Field in Arlington, Texas, USA."},
        {"role": "user", "content": "What is an unknown rule of baseball that many people don't know?"}
    ]
)

output_text = output['choices'][0]['message']['content']
print(output_text)