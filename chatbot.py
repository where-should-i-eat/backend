import openai

with open('API_KEY.txt', 'r') as file:
    API_KEY = file.read().rstrip()

openai.api_key = API_KEY

def init_chatbot(model="gpt-3.5-turbo"):
    response = input("What do you want to buy?\n")
    messages_history = [
        {"role": "system", "content": "You are a helpful shopping assistant. Your goal is to get tags to search Craigslist with for relevant items. When you are done with your task, say DONE."},
        {"role": "assistant", "content": "What do you want to buy?"}]
    chatbot(response, messages_history, model)

def chatbot(response, messages_history, model):
    messages_history += [{"role": "user", "content": response}]

    output = openai.ChatCompletion.create(
        model=model,
        messages=messages_history,
        max_tokens=100
    )
    output_text = output['choices'][0]['message']['content']
    messages_history += [{"role": "assistant", "content": output_text}]

    next_response = input(output_text + "\n")
    chatbot(next_response, messages_history, model)

init_chatbot()