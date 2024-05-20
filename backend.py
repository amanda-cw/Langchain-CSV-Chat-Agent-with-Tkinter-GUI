import sqlite3
import pandas as pd
from sqlalchemy import create_engine
from langchain_experimental.agents import create_csv_agent
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_community.chat_models import ChatOpenAI
from langchain_openai import OpenAI, ChatOpenAI
from langchain.agents import AgentExecutor
from langchain.agents.agent_types import AgentType
from langchain_community.output_parsers.rail_parser import GuardrailsOutputParser

from langchain.pydantic_v1 import BaseModel, Field


import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Global csv connection variable
csv_agent = None


def load_csv_agent(csv_file_path):
    global csv_agent
    try:

        csv_agent = create_csv_agent(
            ChatOpenAI(
                temperature=0, model="gpt-3.5-turbo-0613", openai_api_key=OPENAI_API_KEY
            ),
            csv_file_path,
            verbose=True,
            agent_type=AgentType.OPENAI_FUNCTIONS,
            handle_parsing_errors=True,
        )

        return True, f"Database created and loaded successfully from {csv_file_path}"
    except Exception as e:
        return False, str(e)


def process_prompt(prompt):
    global csv_agent
    if csv_agent is None:
        return "No CSV agent connection is available."

    result = csv_agent.invoke(prompt)
    return result["output"]
