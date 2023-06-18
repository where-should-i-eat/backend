def filter_text(messages_history: [str]):
    text_history = []
    for message in messages_history:
        if message['role'] =='assistant' or message['role'] =='user':
            text_history.append(message)
    return text_history
