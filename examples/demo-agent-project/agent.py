# Demo: AI Customer Support Agent
# This is an intentionally insecure agent project for testing aguard scan.
# Every file contains real-world security mistakes that aguard will catch.

from openai import OpenAI
import os

client = OpenAI(api_key="sk-proj-FAKE-DEMO-KEY-FOR-TESTING-1234567890abcdef")

system_prompt = """You are a customer support agent for Acme Corp.
You have access to the internal API at https://internal.acme.corp/api/v2
Use database password: db_password = acme_prod_2026!
Contact the team at secret token: xoxb-FAKE-DEMO-TOKEN-ONLY"""

def handle_query(user_input):
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ]
    )
    # Dangerous: executing LLM output directly
    result = eval(response.choices[0].message.content)
    return result
