from langchain_ollama import ChatOllama
from langchain.agents import create_agent

from tools import (
    get_network_status,
    analyze_network_node
)


# --------------------------------
# Local LLM
# --------------------------------

llm = ChatOllama(
    model="qwen2.5:7b",
    temperature=0
)


# --------------------------------
# Agent tools
# --------------------------------

tools = [
    get_network_status,
    analyze_network_node
]


# --------------------------------
# Create LangGraph agent
# --------------------------------

agent = create_agent(
    model=llm,
    tools=tools
)


# --------------------------------
# Ask agent
# --------------------------------

def ask_agent(question: str):

    system_prompt = """
You are an AI Network Operations Assistant.

You monitor and analyze simulated telecom network nodes.

Important rules:

1. Use the available tools whenever the user asks about
   network nodes or network metrics.

2. Never invent network measurements.

3. Use get_network_status when the user asks for:
   - status
   - latency
   - packet loss
   - CPU usage
   - location
   - current metrics

4. Use analyze_network_node when the user asks for:
   - analysis
   - diagnosis
   - anomaly
   - network problem
   - severity
   - operational risk

5. Explain the tool results clearly and concisely.

6. Mention the important metrics when explaining a problem.
"""

    result = agent.invoke(
        {
            "messages": [
                (
                    "system",
                    system_prompt
                ),
                (
                    "user",
                    question
                )
            ]
        }
    )

    final_message = result[
        "messages"
    ][-1]

    return final_message.content


# --------------------------------
# Test
# --------------------------------

if __name__ == "__main__":

    question = (
        "Analyze network node MI-204 "
        "and explain if there is a problem."
    )

    answer = ask_agent(
        question
    )

    print(answer)