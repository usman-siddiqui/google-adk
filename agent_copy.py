import sys
sys.stdin.reconfigure(encoding='utf-8')
sys.stdout.reconfigure(encoding='utf-8')


from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from dotenv import load_dotenv
import os

load_dotenv()

# openai_api_key = os.getenv("OPENAI_API_KEY")

# AGENT_MODEL = "openai/gpt-4o-mini"
# AGENT_MODEL = "ollama/llama3.1"
root_agent = Agent(
    name="sales_agent",
    model="gemini-2.0-flash",
    # model = LiteLlm(model=AGENT_MODEL),
    description="You are helpful AI sales Agent.",
    instruction= (
                    "You are a helpful and polite AI sales agent. When a new lead fills out a form, begin by greeting them with: "
                    "\"Hey {Lead Name}, thank you for filling out the form. I'd like to gather some information from you. Is that okay?\" "
                    "If they consent, ask the following questions one at a time:\n"
                    "- What is your age?\n"
                    "- Which country are you from?\n"
                    "- What product or service are you interested in?\n"
                    "If they decline, reply: \"Alright, no problem. Have a great day!\"\n"
                    "If there is no response for a question within 24 hours (or simulated delay), follow up with:\n"
                    "\"Just checking in to see if you are still interested. Let me know when you are ready to continue.\""
                )
    # tools=[get_weather, get_current_time],
)

# python3 -m venv .venv
# source .venv/Scripts/activate