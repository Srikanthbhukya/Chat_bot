from langgraph.graph import StateGraph,START,END
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from dotenv import load_dotenv
from typing import TypedDict,Annotated
from langgraph.checkpoint.memory import InMemorySaver
from langchain_core.messages import HumanMessage
from langgraph.graph.message import BaseMessage,add_messages

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
     

graph=StateGraph(Chat_mess)
graph.add_node('chat_bot',Chat_bot)

graph.add_edge(START,'chat_bot')
graph.add_edge('chat_bot',END)
checkpointer=InMemorySaver()

workflow=graph.compile(checkpointer=checkpointer)



