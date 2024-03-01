from flask_restful import Resource, Api, request
from config.db import db
from flask import jsonify
import hashlib
import traceback
from datetime import datetime
from application.utils.aes_encryption import encrypt_aes, decrypt_aes
from Crypto.Random import get_random_bytes
from cloudinary import uploader
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
import cassio
from langchain.llms import OpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores.cassandra import Cassandra
from langchain.indexes.vectorstore import VectorStoreIndexWrapper
from bson import ObjectId

Bot = db["bot"]
ASTRA_DB_APPLICATION_TOKEN = "AstraCS:BWdZZGegWodWoyvbSsIoHzue:1c3b531d1d132b854decda435108c54401df965cb9da5dad53e79ff081d51829"
ASTRA_DB_API_ENDPOINT = "https://8c4ee0b7-ea01-49c6-a080-bae06d75c587-us-east1.apps.astra.datastax.com"
OPENAI_API_KEY = "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"
ASTRA_DB_ID = "8c4ee0b7-ea01-49c6-a080-bae06d75c587"  # Enter your Database ID


cassio.init(token=ASTRA_DB_APPLICATION_TOKEN, database_id=ASTRA_DB_ID)





llm = OpenAI(openai_api_key=OPENAI_API_KEY)
embedding = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
astra_vector_store = Cassandra(
    embedding=embedding,
    table_name="qa_mini_demo",
    session=None,
    keyspace=None,
)





aes_key = b'\xb3\xb8(\x8a\xbe0\xa8\x8d\xbe+[\xca{@\xb1\x1d'  # Generate a random AES key for encryption
print(f"AES Key: {aes_key}")
class AddChat(Resource):
    def post(self):
        try:
            data = request.get_json()
            bot_id = data.get("bot_id")
            question = data.get("question")


            if not bot_id:
                return jsonify({"message": "Bot ID is required", "status": 400})
            if not question:
                return jsonify({"message": "Question is required", "status": 400})
            
            bot = Bot.find_one({"_id": ObjectId(bot_id)})
            if not bot:
                return jsonify({"message": "Bot not found", "status": 404})
            
            text = bot.get("text_splits", "")
            astra_vector_store.add_texts(text)
            print(f"Inserted {len(text)} headlines. ")
            role_playing = decrypt_aes(bot["encrypted_bot_prompt"], bot["iv"], aes_key)  # Decrypt prompt


            astra_vector_index = VectorStoreIndexWrapper(vectorstore=astra_vector_store)


            query_text = str(role_playing) + question

            print("\nQUESTION: \"%s\"" % question)  # Display original user query
            answer = astra_vector_index.query(query_text, llm=llm).strip()  # Use modified query for processing
            print("ANSWER: \"%s\"\n" % answer)
            
            chat_data = {
                "question": question,
                "answer": answer,
                "timestamp": datetime.now()
            }

            bot["chat_history"].append(chat_data)
            Bot.update_one({"_id": ObjectId(bot_id)}, {"$set": bot})


            return jsonify({"message": "Chat added successfully", "status": 200, "answer": answer, "previous_chat": bot.get("chat_history", [])})


        except Exception as e:
            print(traceback.format_exc())
            return jsonify({"message": "Something went wrong", "status": 500})

