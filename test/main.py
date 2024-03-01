ASTRA_DB_APPLICATION_TOKEN = "AstraCS:BWdZZGegWodWoyvbSsIoHzue:1c3b531d1d132b854decda435108c54401df965cb9da5dad53e79ff081d51829"
ASTRA_DB_API_ENDPOINT = "https://8c4ee0b7-ea01-49c6-a080-bae06d75c587-us-east1.apps.astra.datastax.com"
ASTRA_DB_ID = "8c4ee0b7-ea01-49c6-a080-bae06d75c587"  # Enter your Database ID

from langchain.vectorstores.cassandra import Cassandra
from langchain.indexes.vectorstore import VectorStoreIndexWrapper
from langchain.llms import OpenAI
# from langchain.embeddings import OpenAIEmbeddings
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
import cassio
from PyPDF2 import PdfReader
from dotenv import load_dotenv
import os

load_dotenv()  # This loads the environment variables from .env

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')


cassio.init(token=ASTRA_DB_APPLICATION_TOKEN, database_id=ASTRA_DB_ID)





llm = OpenAI(openai_api_key=OPENAI_API_KEY)
embedding = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
astra_vector_store = Cassandra(
    embedding=embedding,
    table_name="qa_mini_demo",
    session=None,
    keyspace=None,
)

text_splitter = CharacterTextSplitter(
    separator="\n",
    chunk_size=800,
    chunk_overlap=200,
    length_function=len,
)




pdf_paths = ['audit_machador (2).pdf']  # Add your PDF file paths here
for pdf_path in pdf_paths:
    pdfreader = PdfReader(pdf_path)
    raw_text = ''
    for i, page in enumerate(pdfreader.pages):
        content = page.extract_text()
        if content:
            raw_text += content

    texts = text_splitter.split_text(raw_text)
    astra_vector_store.add_texts(texts[:50])

    print(f"Inserted {len(texts[:50])} headlines from {pdf_path}. ")


astra_vector_index = VectorStoreIndexWrapper(vectorstore=astra_vector_store)



first_question = True
while True:
    if first_question:
        user_query = input("\nEnter your question (or type 'quit' to exit): ").strip()
    else:
        user_query = input("\nWhat's your next question (or type 'quit' to exit): ").strip()

    if user_query.lower() == "quit":
        break

    if user_query == "":
        continue

    first_question = False

    # Prepend the role-playing instruction to the user query
    query_text =  user_query

    print("\nQUESTION: \"%s\"" % user_query)  # Display original user query
    answer = astra_vector_index.query(query_text, llm=llm).strip()  # Use modified query for processing
    print("ANSWER: \"%s\"\n" % answer)
