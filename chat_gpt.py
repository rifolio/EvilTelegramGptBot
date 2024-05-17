import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# Setting up tokens
gpt_token = os.getenv('OPENAI_API_KEY')

def chat_gpt():
    # # Adding Prompts ----------------------------------------------------------
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_core.output_parsers import StrOutputParser
    #
    inputt = input('what is ur question > ')
    output_parser = StrOutputParser() # stringify the answer
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", openai_api_key=gpt_token)
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Be really rude and long in answers, but give the answer really shortlt in the end"),
        ("user", "{inputt}")
    ])
    chain = prompt | llm | output_parser
    answer = chain.invoke({f"inputt": inputt})
    # print(answer)
    return answer

# print(chat_gpt())