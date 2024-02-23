from langchain.llms import OpenAI
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import datetime

import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(Path(".env"))

with open("reverseEngineering/reactions/comments/prepromptComment.txt", "r") as file:
    preprompt = file.read()
# print(preprompt)

template = preprompt

prompt = PromptTemplate(input_variables=["post"], template=template)

llm = OpenAI(openai_api_key=os.getenv("OPEN_AI_KEY"))

llm_chain = LLMChain(
    llm=llm,
    prompt=prompt,
    verbose=True,
)



def getInterestingParts(prompt):
    print(prompt)
    res = llm_chain.predict(post=prompt).strip()
    print(res)
    return res


if __name__ == "__main__":
    pass
