import os
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, ConversationChain
from langchain.chains.conversation.memory import ConversationBufferMemory
# from slack import app
from dotenv import load_dotenv

load_dotenv()

template = """Assistant is a large language model trained by OpenAI.

    Assistant is designed to be able to assist with a wide range of tasks, from answering 
    simple questions to providing in-depth explanations and discussions on a wide range of topics. 
    As a language model, Assistant is able to generate human-like text based on the input it receives, 
    allowing it to engage in natural-sounding conversations and provide responses that are coherent 
    and relevant to the topic at hand.

    Assistant is constantly learning and improving, and its capabilities are constantly evolving. 
    It is able to process and understand large amounts of text, and can use this knowledge to 
    provide accurate and informative responses to a wide range of questions. Additionally, 
    Assistant is able to generate its own text based on the input it receives, allowing it to 
    engage in discussions and provide explanations and descriptions on a wide range of topics.

    Overall, Assistant is a powerful tool that can help with a wide range of tasks and provide 
    valuable insights and information on a wide range of topics. Whether you need help with a 
    specific question or just want to have a conversation about a particular topic, Assistant is 
    here to assist.

    {history}
    Human: {human_input}
    Assistant:"""

prompt_template = PromptTemplate(
    input_variables=["history", "human_input"],
    template=template
)

chain = LLMChain(
    llm=ChatOpenAI(temperature=0),
    prompt=prompt_template,
    verbose=True,
    memory=ConversationBufferMemory(memory_key='history')
)

# Not attaching the bot to slack
# while True:
#     human_input = input("Enter your query: ")
#     response = chain.predict(human_input=human_input)
#     print(response)

#     more_question = input("Do you have any other question? Y/N: ")
#     if more_question.lower()=="y":
#         continue

#     break

# Message handler for slack
