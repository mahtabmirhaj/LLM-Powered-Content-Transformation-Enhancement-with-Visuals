from ericai import EricAI, AsyncEricAI
from ericai.constants import ERICSSON_GENAI_BASE
from ericai.cert_trust import get_combined_ca_bundle_path

from langchain_openai import ChatOpenAI
import os

# paste your access token here (get it with `ericai --ericsson-access-token`)
# the access token is valid for a limited time, you might need to regenerate it
access_token = os.getenv("ERICAI_ACCESS_TOKEN")

# The EricAI client mimics the OpenAI client (in fact, it's a subclass of openai.OpenAI)
client = EricAI()
async_client = AsyncEricAI()  # this is the asynchronous implementation of EricAI (using Python's async package)

print
print("ERICSSON_GENAI_BASE: " + ERICSSON_GENAI_BASE)
print

# First we instantiate the OpenAI interface for langchain, but use Ericsson's EricAI API URL and token
ericai = ChatOpenAI(
    model="deepseek-ai/DeepSeek-R1-Distill-Qwen-32B",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    api_key=access_token,  # if you prefer to pass api key in directly instaed of using env vars
    base_url=ERICSSON_GENAI_BASE,
)

# Now we plug the EricAI client into our langchain-openai interface
ericai.client = client.chat.completions
ericai.async_client = async_client.chat.completions

print(ericai.invoke("What model are you?"))

