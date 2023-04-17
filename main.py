# -*- coding: utf-8 -*-

# -- Sheet --

import openai
import os

os.environ["OPENAI_API_KEY"] = "..."
openai_api_key = "..."
openai.api_key = openai_api_key
serpapi_api_key = "..."
os.environ["SERPAPI_API_KEY"] = serpapi_api_key
tools = load_tools(["serpapi", "llm-math"], llm=llm)

from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.agents import AgentType
from langchain.llms import OpenAI

llm = OpenAI(openai_api_key=openai_api_key, temperature=0.5)
tools = load_tools(["serpapi"], llm=llm)

agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

# Step 1: Problem/Topic Selection
problem_or_topic = "What major obsticals of the problem- " + input("Please provide a problem or topic for DreamGPT to explore: ")

# Run the agent to gather initial thoughts on the problem or topic
initial_thoughts = []

for _ in range(2):
    thought = agent.run(problem_or_topic)
    initial_thoughts.append(thought)

search_result1 = ' '.join(initial_thoughts)
print(search_result1)


from langchain.llms import OpenAI

# Construct a prompt for GPT-3
prompt = (
    f"Please provide a concise summary of the following text:\n\n"
    f"{search_result1}\n\n"
    "Summary:"
)

# Call GPT-3 with the constructed prompt
response = llm(prompt)

# Save the response as search_summary
search_summary = response.strip()

# Print the search_summary
print(search_summary)

from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.llms import OpenAI


llm = OpenAI(temperature=0)

agent = initialize_agent(tools, llm, agent="zero-shot-react-description", verbose=True)


import random
import pinecone
from langchain.memory import ConversationBufferMemory
from collections import UserDict

class CustomConversationBufferMemory(ConversationBufferMemory, UserDict):
    pass

def randomize_temperature(base_temperature, min_offset=0.1, max_offset=0.3):
    offset = random.uniform(min_offset, max_offset)
    return base_temperature + offset

def summarize(text):
    # Replace this with your preferred summarization method
    return text[:100] + '...'

# Initialize the custom memory object
memory = CustomConversationBufferMemory(memory_key="chat_history")

# Initialize the agents with the memory object and randomized temperature
agent_id = initialize_agent(tools, OpenAI(temperature=randomize_temperature(1.0)), agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION, verbose=True, memory=memory)
agent_superego = initialize_agent(tools, OpenAI(temperature=randomize_temperature(1.0)), agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION, verbose=True, memory=memory)
agent_ego = initialize_agent(tools, OpenAI(temperature=randomize_temperature(1.0)), agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION, verbose=True, memory=memory)

# Run the debate between the agents
debate_rounds = 2  # You can change this to the desired number of debate rounds
debate_history = []

for i in range(debate_rounds):
    
    id_input = f"Id: As an agent focusing on self-interest and creativity, taking {search_summary} as reference, my innovative solution to {problem_or_topic} is:"
    debate_history.append(agent_id.run(id_input))

    superego_input = f"Superego: Based on {summarize(id_input)}, considering the risks and potential benefit to others and the environment, my solution for {problem_or_topic} is:"
    debate_history.append(agent_superego.run(superego_input))

    ego_input = f"Ego: Considering {summarize(id_input)} and {summarize(superego_input)}, the most practical yet innovative solution to {problem_or_topic} should be:"
    debate_history.append(agent_ego.run(ego_input))

# Print the debate history
for message in debate_history:
    print(message)


# Print the debate history and save it to a local file
with open("debate_history.txt", "w") as file:
    for message in debate_history:
        print(message)
        file.write(message + "\n")


from langchain.llms import OpenAI

# Initialize the summarizer
summarizer = OpenAI(temperature=0.3)

# Combine the debate history into a single text
debate_text = ' '.join(debate_history)

# Construct a prompt for GPT-3 to summarize the debate
prompt = (
    f"Please summarize the following conversation between three AI agents (Id, Superego, and Ego) discussing {problem_or_topic}:\n\n"
    f"{debate_text}\n\n"
    "Summary:"
)

# Call GPT-3 with the constructed prompt
summary = summarizer(prompt)

# Print the summary
print(summary)

with open("conversation.txt", "w") as f:
    for message in debate_history:
        f.write(message + "\n")

with open("conversation.txt", "r") as f:
    content = f.read()
    print(content)

import random

def rearrange_word_chunks(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()
    
    sentences = [line.strip() for line in lines if line.strip()]
    word_chunks = [word for sentence in sentences for word in sentence.split()]
    random.shuffle(word_chunks)
    
    rearranged_file_path = 'rearranged_word_chunks.txt'
    with open(rearranged_file_path, 'w') as f:
        for word_chunk in word_chunks:
            f.write(word_chunk + ' ')
    
    return rearranged_file_path

rearranged_file_path = rearrange_word_chunks('conversation.txt')
from langchain.llms import OpenAI

problem_or_topic = "your problem or topic here"  # Replace this with your problem or topic
llm = OpenAI(temperature=0.5)  # You can adjust the temperature value depending on the desired randomness

# Read rearranged word chunks from the file
with open(rearranged_file_path, 'r') as f:
    rearranged_word_chunks = f.read()

# Construct a prompt for GPT-3
prompt = (
    f"Given the following rearranged word chunks from a conversation about {problem_or_topic}, "
    "identify potential solutions or insights:\n\n"
    f"{rearranged_word_chunks}\n\n"
    "Potential solutions or insights:"
)

# Call GPT-3 with the constructed prompt
response = llm(prompt)

# Print the response
print(response)



