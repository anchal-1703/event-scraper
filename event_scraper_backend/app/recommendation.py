from langchain.chains import RetrievalQA
from langchain_community.vectorstores import Redis as RedisVectorStore
from langchain_google_vertexai import VertexAIEmbeddings, ChatVertexAI

import redis
import json
import os
from dotenv import load_dotenv
load_dotenv()

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")


# Vertex AI Embedding setup
embedding = VertexAIEmbeddings(
    project="event-recommender-460511",
    location="us-central1",
    model_name="gemini-2.5-flash-preview-05-20"
)

# Proper Redis connection
redis_conn = redis.Redis.from_url("redis://localhost:6379")

# Load data from Redis (persistent store)
def load_event_data():
    keys = redis_conn.keys("persistent:*")
    events = []
    for key in keys:
        data = redis_conn.get(key)
        if data:
            events += json.loads(data)
    return events

# Convert events to documents
def build_documents(events):
    from langchain.schema import Document
    docs = []
    for e in events:
        content = f"{e['title']} - {e['date']} at {e['venue']}. Visit: {e['url']}"
        docs.append(Document(page_content=content, metadata=e))
    return docs

# Build vector store from events
def build_retriever():
    events = load_event_data()
    docs = build_documents(events)
    vectorstore = RedisVectorStore.from_documents(
        docs,
        embedding=embedding,
        redis_url="redis://localhost:6379",
        index_name="events-index"
    )
    return vectorstore.as_retriever()

retriever = build_retriever()

# Use ChatVertexAI (Gemini) instead of ChatOpenAI
qa = RetrievalQA.from_chain_type(
    llm=ChatVertexAI(model="gemini-pro", temperature=0),
    retriever=retriever
)

# Run query
def recommend_event(user_query):
    return qa.run(user_query)



# from langchain.chains import RetrievalQA
# from langchain_community.chat_models import ChatOpenAI
# from langchain_community.vectorstores import Redis as RedisVectorStore
# from langchain_google_vertexai import VertexAIEmbeddings

# import redis
# import json
# from dotenv import load_dotenv
# load_dotenv()
# import os


# embedding = VertexAIEmbeddings(
#     project="en-lang-client-0684796858",
#     location="us-central1",
#     model_name="models/text-embedding-005",
# )
# # Init Redis
# # print("OpenAI API Key:", os.getenv("OPENAI_API_KEY"))

# redis_conn = redis.from_url("redis://localhost:6379")
# # embedding = VertexAIEmbeddings()

# # Load data from Redis (persistent store)
# def load_event_data():
#     keys = redis_conn.keys("persistent:*")
#     events = []
#     for key in keys:
#         data = redis_conn.get(key)
#         if data:
#             events += json.loads(data)
#     return events

# # # Convert events to documents
# def build_documents(events):
#     from langchain.schema import Document
#     docs = []
#     for e in events:
#         content = f"{e['title']} - {e['date']} at {e['venue']}. Visit: {e['url']}"
#         docs.append(Document(page_content=content, metadata=e))
#     return docs

# # Build vector store from events
# def build_retriever():
#     events = load_event_data()
#     docs = build_documents(events)
#     # print(f"Number of docs: {len(docs)}")
#     # print(f"Sample doc: {docs[0] if docs else 'No docs found'}")

#     vectorstore = RedisVectorStore.from_documents(docs, embedding=embedding, redis_url="redis://localhost:6379", index_name="events-index")
#     return vectorstore.as_retriever()
# # build_retriever()
# retriever = build_retriever()
# qa = RetrievalQA.from_chain_type(llm=ChatOpenAI(temperature=0), retriever=retriever)

# # Run query
# def recommend_event(user_query):
#     return qa.run(user_query)
# # 8043437751:AAG0wNUoQIrs0m8Z2K0J4MkI6ZEjVCIMPsY
# # AIzaSyAvlNq-3IOIM0X4ex5QhXpqVakt_QlA1VI
# # 859934971211
# # gen-lang-client-0684796858