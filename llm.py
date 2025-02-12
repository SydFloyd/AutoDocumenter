# from datetime import datetime as dt
# import json
# from pprint import pprint
# from random import randint
import os
from openai import OpenAI

class LLM:
    def __init__(self, 
                 model='gpt-4o', 
                 max_tokens=1000, 
                 temperature=0.3, 
                 system_message=None, 
                 injected_messages=None,
                 save_messages=False):
        self.model = model
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.system_message = system_message
        self.injected_messages = injected_messages
        self.save_messages = save_messages

        self.message_history = []

        self.client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    def compile_messages(self, prompt):
        messages = []
        if self.system_message:
            messages.append({"role": "system", "content": self.system_message})
        if self.injected_messages:
            messages.extend(self.injected_messages)
        if self.save_messages:
            messages.extend(self.message_history)
        messages.append({"role": "user", "content": prompt})
        return messages
    
    def prompt(self, prompt):
        messages = self.compile_messages(prompt)

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            top_p=0.95,
            frequency_penalty=0,
            presence_penalty=0,
            stop=None,
        )

        answer = response.choices[0].message
        if self.save_messages:
            self.message_history.append({"role": "user", "content": prompt})
            self.message_history.append(answer)
        return answer.content