import replicate
import streamlit as st
import os

REPLICATE_API_TOKEN = st.secrets['RAT']
os.environ['REPLICATE_API_TOKEN'] = REPLICATE_API_TOKEN

st.set_page_config(page_title="😂🤣...Rishi ChatBot?")

if "messages" not in st.session_state.keys():
    st.session_state.messages = [{'role': 'assistant', 'content': 'How may I assist you today?'}]

for message in st.session_state.messages:
    with st.chat_message(message['role']):
        st.write(message['content'])

def clear_chat_history():
    st.session_state.messages = [{'role':'assistant', 'content': 'How may I assist you today?'}]
    
st.sidebar.button('Clear Chat History', on_click = clear_chat_history)

def generate_response(prompt_input):
    string_dialouge = "You are a helpful, respectful and honest assistant. Always answer as helpfully as possible, while being safe. Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content. Please ensure that your responses are socially unbiased and positive in nature.\n\nIf a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. If you don't know the answer to a question, please don't share false information."
    for dict_message in st.session_state.messages:
        if dict_message['role']=='user':
            string_dialouge+= "User: "+ dict_message['content'] + '\n\n'
        else:
            string_dialouge += "Assistant: " + dict_message['content'] + '\n\n'
    
    input = {
        "top_p": 1,
        "prompt": f"{string_dialouge} {prompt_input} Assistant: ",
        "temperature": 0.75,
        "system_prompt": "You are a helpful, respectful and honest assistant. Always answer as helpfully as possible, while being safe. Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content. Please ensure that your responses are socially unbiased and positive in nature.\n\nIf a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. If you don't know the answer to a question, please don't share false information.",
        "max_new_tokens": 800,
        "repetition_penalty": 1
      )
    output = replicate.run("meta/llama-2-7b-chat", input = input)
    return ''.join(output)

if prompt:= st.chat_input():
    st.session_state.messages.append({'role':'user', 'content': prompt})
    with st.chat_message('user'):
        st.write(prompt)
        
if st.session_state.messages[-1]['role'] != 'assistant':
    with st.chat_message('assistant'):
        with st.spinner("Thinking..."):
            response = generate_response(prompt)
            placeholder = st.empty()
            full_response = ''
            for item in response:
                full_response += item
                placeholder.markdown(full_response)
            placeholder.markdown(full_response)
    message = {"role": 'assistant', 'content': full_response}
    st.session_state.messages.append(message)
