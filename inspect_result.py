import os
import asyncio
from pydantic_ai import Agent
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

# Mock result
class Result(BaseModel):
    value: str

# Minimal agent
agent = Agent('google-gla:gemini-2.5-flash', output_type=Result)

async def main():
    if not os.getenv("GOOGLE_API_KEY"):
         # fallback for testing if key missing
         print("Missing API KEY")
         return

    try:
        # Simple prompt
        result = await agent.run("Say hello and return value='hello'")
        print(f"Type: {type(result)}")
        print(f"Dir: {dir(result)}")
        try:
            print(f"Data: {result.data}")
        except AttributeError:
            print("No .data attribute")
    except Exception as e:
        print(f"Run failed: {e}")

if __name__ == "__main__":
    asyncio.run(main())
