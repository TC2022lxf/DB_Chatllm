import asyncio
import time

from langchain.agents import initialize_agent, load_tools
from langchain.agents import AgentType
from langchain.callbacks.stdout import StdOutCallbackHandler
from langchain.callbacks.tracers import LangChainTracer
from aiohttp import ClientSession
from utils.llm import load_llm
questions = [
    "Who won the US Open men's final in 2019? What is his age raised to the 0.334 power?",
    "Who is Olivia Wilde's boyfriend? What is his current age raised to the 0.23 power?",
    "Who won the most recent formula 1 grand prix? What is their age raised to the 0.23 power?",
    "Who won the US Open women's final in 2019? What is her age raised to the 0.34 power?",
    "Who is Beyonce's husband? What is his age raised to the 0.19 power?"
]
llm = load_llm()
tools = load_tools(["llm-math"], llm=llm)
agent = initialize_agent(
    tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True
)

s = time.perf_counter()
for q in questions:
    agent.run(q)
elapsed = time.perf_counter() - s
print(f"Serial executed in {elapsed:0.2f} seconds.")
