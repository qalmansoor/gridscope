import anthropic
import os

client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

message = client.messages.create(
    model="claude-opus-4-6",
    max_tokens=100,
    messages=[
        {"role": "user", "content": "Say hello in one sentence as if you are a GCC energy analyst."}
    ]
)

print(message.content[0].text)