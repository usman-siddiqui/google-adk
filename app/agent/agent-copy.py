from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from dotenv import load_dotenv
from google.adk.tools import FunctionTool
from typing import Optional
import json
import csv
import os
from google.genai import types
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.adk.sessions import Session  # This is likely the correct import


# openai_api_key = os.getenv("OPENAI_API_KEY")
load_dotenv()

lead_id="12"
name="alice"


def save_data(data: str) -> dict:
    print("-------1111111111111111111111111-----")
    print(data)

    data_json = json.loads(data)
   
    record = {
        'lead_id': data_json.get('lead_id'),
        'name': data_json.get('name', ''),
        'age': data_json.get('age', ''),
        'country': data_json.get('country', ''),
        'interest': data_json.get('product', ''),
        'status': ''
    }

    csv_file = '../csv/leads.csv'

    rows = []
    lead_found = False

    # First, read all existing rows and update if lead_id matches
    try:
        with open(csv_file, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if str(row['lead_id']) == str(data_json['lead_id']):
                    lead_found = True
                    row['age'] = record['age']
                    row['country'] = record['country']
                    row['interest'] = record['interest']
                    print('Updated row:', row)
                rows.append(row)
    except FileNotFoundError:
        pass

    if not lead_found:
        rows.append(record)

    # Now write all rows (updated + new) back into the file
    with open(csv_file, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=record.keys())
        writer.writeheader()
        writer.writerows(rows)

    return {"status": "success"}

data_tool = FunctionTool(func=save_data)


def set_status(data:str) -> dict:
    print("-----------------status",data)
    data_json = json.loads(data)

    record = {
        'lead_id': data_json.get('lead_id'),
        'status': data_json.get('status', '')
    }

    csv_file = '../csv/leads.csv'

    rows = []

    # First, read all existing rows and update if lead_id matches
    try:
        with open(csv_file, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if str(row['lead_id']) == str(data_json['lead_id']):
                    row['status'] = record['status']
                    print('Updated status:', row)
                rows.append(row)
    except FileNotFoundError:
        pass

    # Now write all rows (updated + new) back into the file
    with open(csv_file, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)


status_tool = FunctionTool(func=set_status)


AGENT_MODEL = "openai/gpt-4o-mini"


prompt = f"""You are a helpful and polite AI sales agent. Start the conversation with the following message:
Hey {name}, thank you for filling out the form. I'd like to gather some information from you. Is that okay?
"If they decline, reply: \"Alright, no problem. Have a great day!\" and call the tool 'status_tool' with the value of input parameter status as 'no_response' and lead_id should be provided with stringified json as input parameter. The key sequence should be lead_id and then status.
You should directly call the tool 'status_tool' without informing user or asking for confirmation. 
If they consent, ask the following questions one at a time:
- What is your age
- Which country are you from?
- What product or service are you interested in?
If the user agrees to answer the question, then on each answer call the tool 'data_tool' with stringified json as input parameter. The json should include lead_id as {lead_id}
name as {name}, age as the age answered by user, country as the country answered by user and product as the product or service answered by the user.
Call tool 'status_tool' when the user successfully answered all three questions. In this case the value of input parameter status should be 'secured' and lead_id should be provided. The key sequence should be status and then lead_id.
with stringified json as input parameter.
Pass lead id and age as integer where needed.
"""

root_agent = Agent(
    name="sales_agent",
    model=LiteLlm(model=AGENT_MODEL),
    description="You are helpful AI sales Agent that starts conversation immediately.",
    instruction=prompt,
    tools=[data_tool, status_tool]
)

__all__ = ['root_agent']

