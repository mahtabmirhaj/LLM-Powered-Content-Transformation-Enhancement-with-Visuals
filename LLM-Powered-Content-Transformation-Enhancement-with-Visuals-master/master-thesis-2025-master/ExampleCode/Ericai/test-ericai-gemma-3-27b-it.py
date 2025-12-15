import os
from ericai import EricAI, AsyncEricAI
from ericai.constants import ERICSSON_GENAI_BASE
from ericai.cert_trust import get_combined_ca_bundle_path

#from langchain_openai import ChatOpenAI

# paste your access token here (get it with `ericai --ericsson-access-token`)
# the access token is valid for a limited time, you might need to regenerate it
access_token = os.getenv("ERICAI_ACCESS_TOKEN")

# The EricAI client mimics the OpenAI client (in fact, it's a subclass of openai.OpenAI)
client = EricAI()

print()
print("ERICSSON_GENAI_BASE: " + ERICSSON_GENAI_BASE)
print()

user_prompt= "What model are you?"

#Prepare the chat prompt
chat_prompt = [
    {
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": user_prompt
            }
        ]
    }
]

# Include speech result if speech is enabled
messages = chat_prompt

response = client.chat.completions.create(
    model="Google/Gemma-3-27B-it",
    messages=messages,
    # stream=False
)

print("--- response ---")
print(response)
print()
print("--- response.choices[0].message.content ---")
print(response.choices[0].message.content)
