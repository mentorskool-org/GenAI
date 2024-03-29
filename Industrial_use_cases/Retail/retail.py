from langchain_google_genai import GoogleGenerativeAI
from langchain.utilities.sql_database import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain
from langchain.prompts import SemanticSimilarityExampleSelector
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from langchain.prompts import FewShotPromptTemplate
from langchain.chains.sql_database.prompt import PROMPT_SUFFIX, _postgres_prompt
from langchain.prompts.prompt import PromptTemplate
from sqlalchemy import URL

import os
from dotenv import load_dotenv
from few_shot_example import few_shots


# llm = GoogleGenerativeAI(
#     model="gemini-pro", temperature=0.1, google_api_key=os.environ["GOOGLE_API_KEY"]
# )

# result = llm.invoke("What is Taj Mahal?")
# print(result)


def get_few_shot_chain():
    # Create connection string
    connectionURL = URL.create(
        "postgresql+psycopg2",
        host=os.environ.get("HOST"),
        database="atliq_tshirts",
        username=os.environ.get("USER"),
        port=5432,
        password=os.environ.get("PASSWORD"),
    )

    db = SQLDatabase.from_uri(connectionURL, sample_rows_in_table_info=3)

    llm = GoogleGenerativeAI(
        model="gemini-pro", temperature=0.1, google_api_key=os.environ["GOOGLE_API_KEY"]
    )

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    to_vectorize = [" ".join(example.values()) for example in few_shots]
    vectorstore = Chroma.from_texts(to_vectorize, embeddings, metadatas=few_shots)
    example_selector = SemanticSimilarityExampleSelector(
        vectorstore=vectorstore,
        k=2,
    )

    example_prompt = PromptTemplate(
        input_variables=["Question", "SQLQuery", "SQLResult", "Answer"],
        template="\nQuestion: {Question}\nSQLQuery: {SQLQuery}\nSQLResult: {SQLResult}\nAnswer: {Answer}",
    )

    few_shot_prompt = FewShotPromptTemplate(
        example_selector=example_selector,
        example_prompt=example_prompt,
        prefix=_postgres_prompt,
        suffix=PROMPT_SUFFIX,
        input_variables=["input", "table_info", "top_k"], #These variables are used in the prefix and suffix
    )

    chain = SQLDatabaseChain.from_llm(llm, db, verbose=True, prompt=few_shot_prompt)
    return chain


if __name__ == "__main__":
    chain = get_few_shot_chain()
    print(chain.run("How many t-shirts of Nike are available in the store?"))