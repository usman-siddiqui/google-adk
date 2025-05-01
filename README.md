This project implements an automated AI sales agent built using the Google ADK framework. The agent interacts with potential leads collected via form submissions, gathers additional information through a multi-turn conversation, and updates a CSV file with structured data. The system also tracks the lead status, marking them as "secured" or "no_response".

Setup Instructions

1. Create Virtual Environment
    
    ```python3 -m venv venv ```
    ```source venv/bin/activate  ``` # I am using linux OS


2. Install Dependencies
   ``` pip install -r requirements.txt ```


3. Set Environment Variables
    Create a .env file in the root directory and add:

    OPENAI_API_KEY=your_openai_api_key
    Replace your_openai_api_key with your actual OpenAI API key.

4. Create Required Directories and Files
    Ensure that the csv leads.csv file placed under csv file 
    
    if leads.csv file does not exists create it under csv folder and ensure that the headers (lead_id,name,age,country,interest,status) must be there

5. Design Decisions
    Modular Agent with Google ADK
    Agent Definition: Built using google.adk.agents.Agent for modular and scalable conversation design.

6. Tool Usage
    data_tool: Invokes save_data to update the lead's demographic and interest information in csv/leads.csv.

    status_tool: Invokes set_status to update the lead’s current engagement status (secured or no_response).

7. Prompt Design
    The system prompt guides the LLM to:

    Ask three specific questions.

    Automatically call status_tool if the user declines to proceed.

    Call data_tool after each response.

    Set the status to "secured" only if all three questions are answered.

    The prompt enforces implicit tool execution, meaning the LLM will call tools without asking user confirmation.

8. Data Handling
    CSV is chosen as a lightweight, inspectable format for managing lead data.

    JSON inputs to tools ensure structured, extendable interfacing.

9. Assumptions
    Each lead is identified by a unique lead_id.

    Fields such as age and lead_id are stored as integers.

    Users either complete the whole flow or are marked as unresponsive


10. To run the project use the mentioned command under app folder: ``` adk web ```. 

    1. The user will initiate the conversation

11.  Tests cases summary:

    1. user_no_response
        Scenario: User declines to provide information.

        Step 1:

        User Input: "hi"

        Agent Reply: Initiates conversation with greeting and asks for consent.

        Tool Use: None

        Step 2:

        User Input: "no"

        Agent Reply: Ends conversation politely.

        Tool Use: Calls set_status with {"lead_id":12,"status":"no_response"}

    2. user_yes_response
        Scenario: User agrees and successfully provides all requested info.

        Step 1:

        User Input: "hi"

        Agent Reply: Greets and asks for consent.

        Tool Use: None

        Step 2:

        User Input: "yes"

        Agent Reply: Begins data collection (asks for age).

        Tool Use: None

        Step 3:

        User Input: "28"

        Agent Reply: Acknowledges and asks for country.

        Tool Use: Calls save_data with {"lead_id":12,"name":"alice","age":28}

        Step 4:

        User Input: "pak"

        Agent Reply: Acknowledges and asks for product interest.

        Tool Use: Calls save_data with {"lead_id":12,"name":"alice","age":28,"country":"pak"}

        Step 5:

        User Input: "mobile"

        Agent Reply: Thanks the user and confirms all data collected.

        Tool Use:

        Calls save_data with {"lead_id":12,"name":"alice","age":28,"country":"pak","product":"mobile"}

        Calls set_status with {"status":"secured","lead_id":12}

        | Test Name          | Outcome        | Tool Calls                                               |
|--------------------|----------------|-----------------------------------------------------------|
| `user_no_response` | Conversation ended early | `set_status` with `"no_response"`                   |
| `user_yes_response`| Full flow completed       | 3x `save_data`, 1x `set_status` with `"secured"`     |


Test can be run with the following command under app folder: ``` adk eval agent agent/sales_app.evalset.json ```



