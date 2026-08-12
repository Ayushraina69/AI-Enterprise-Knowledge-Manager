import os
from dotenv import load_dotenv
from agents import Agent, Runner, OpenAIChatCompletionsModel
from openai import AsyncOpenAI

load_dotenv()

api_key = os.getenv("OPENROUTER_API_KEY")

if not api_key:
    raise ValueError("OPENROUTER_API_KEY not found in .env")

client = AsyncOpenAI(
    api_key=api_key,
    base_url="https://openrouter.ai/api/v1"
)

model = OpenAIChatCompletionsModel(
    model="openrouter/free",
    openai_client=client
)

agent = Agent(
    name="Connection Test Agent",
    instructions="Reply with a short message confirming that you are working."
    ,
    model=model
)

result = Runner.run_sync(
    agent,
    "Are you working?"
)

print(result.final_output)