import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(
    base_url=os.environ["AZURE_OPENAI_ENDPOINT"].rstrip("/") + "/openai/v1/",
    api_key=os.environ["AZURE_OPENAI_API_KEY"],
)
r = client.responses.create(
    model=os.environ["AZURE_OPENAI_DEPLOYMENT"],
    input="Write a 3-message trade chat about a CS2 skin.",
    reasoning={"effort": "minimal"},
    max_output_tokens=300,
)
print(r.output_text)
print(r.usage)