import streamlit as st
from backend import workflow
from langchain_core.messages import HumanMessage
import uuid

###################################################UTILITY FUNCTIONS###########################################################
def generate_uuid():
    response=uuid.uuid4()
    return response

def chat_id(thread_id):
    if thread_id not in st.session_state['chat_thread']:
        st.session_state['chat_thread'].append(thread_id)


def reset_chat():
    new_thread=generate_uuid()
    st.session_state['thread_id']=new_thread
    chat_id(st.session_state['thread_id'])
    st.session_state['messages']=[]
    
def load_conversation(thread_id):
    state=workflow.get_state(config={'configurable':{'thread_id':thread_id}})
    return state.values.get('messages',[])


    

#####################################################SESSION SETUP##################################################

if 'thread_id' not in st.session_state:
    st.session_state['thread_id']=generate_uuid()




if 'messages' not in st.session_state:
    st.session_state['messages']=[]
    
if 'chat_thread' not in st.session_state:
    st.session_state['chat_thread']=[]
    

chat_id(st.session_state['thread_id'])


    
#####################################################SIDEBAR####################################################################

st.sidebar.title('Langgarph_Chatbot')
if st.sidebar.button('New Chat'):
    reset_chat()
st.sidebar.header('My conversations')


for thread_id in st.session_state['chat_thread'][::-1]:
    if st.sidebar.button(str(thread_id)):
        st.session_state['thread_id']=thread_id
        message=load_conversation(thread_id)
        
        temp_messages=[]
        
        for msg in message:
            if isinstance(msg,HumanMessage):
                role='user'
            else:
                role='assistant'
            
            temp_messages.append({'role':role,'content':msg.content})
        
        st.session_state['messages']=temp_messages


#############################################################MAIN UI#################################################################
user_input=st.chat_input('Type here')

for message in st.session_state['messages']:
    with st.chat_message(message['role']):
        st.text(message['content'])
    

if user_input:

    st.session_state['messages'].append({'role':'user','content':user_input})
    with st.chat_message('user'):
        st.text(user_input)
    
    config = {
        "configurable": {
            "thread_id": st.session_state['thread_id']
        }
    } 
    prompt={'messages':HumanMessage(content=user_input)}
    respone=workflow.invoke(prompt,config=config)
    ai_message=respone['messages'][-1].content
    
    st.session_state['messages'].append({'role':'assistant','content':ai_message})

    with st.chat_message('assistant'):
        st.text(ai_message)