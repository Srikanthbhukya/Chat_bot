from langgraph.graph import StateGraph,START,END
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from dotenv import load_dotenv
from typing import TypedDict,Annotated
from langgraph.checkpoint.sqlite import SqliteSaver
from langchain_core.messages import HumanMessage
from langgraph.graph.message import BaseMessage,add_messages
import sqlite3
load_dotenv()

llm=HuggingFaceEndpoint(
     repo_id="Qwen/Qwen3-8B",
        task="text-generation",
       # max_new_tokens=512,
        temperature=0.7,
       # huggingfacehub_api_token=token,
)
model=ChatHuggingFace(llm=llm)


class Chat_mess(TypedDict):
    messages:Annotated[list[BaseMessage],add_messages]
   
def Chat_bot(state:Chat_mess):
    user=state['messages']
    response=model.invoke(user)
    return{
        'messages':[response]
    }
  

conn = sqlite3.connect(database='chatbot.db', check_same_thread=False)
# Checkpointer
checkpointer = SqliteSaver(conn=conn)
   

graph=StateGraph(Chat_mess)
graph.add_node('chat_bot',Chat_bot)

graph.add_edge(START,'chat_bot')
graph.add_edge('chat_bot',END)


workflow=graph.compile(checkpointer=checkpointer)

def retrive_threads():
    all_threads=set()
    for threads in checkpointer.list(None):
        all_threads.add(threads.config['configurable']['thread_id'])
    
    
    return  list(all_threads)


