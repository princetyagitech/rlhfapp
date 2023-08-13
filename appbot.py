import streamlit as st
from streamlit_chat import message
from streamlit_extras.colored_header import colored_header
from streamlit_extras.add_vertical_space import add_vertical_space
import requests

st.set_page_config(page_title="An LLM-powered Streamlit Summarization app")



# Sidebar contents
with st.sidebar:
    st.title('🤗💬 RLHF Trained LLMs Chat App')
    add_vertical_space(4)
    algorithm = st.selectbox('Select the algorithm ',('ppo', 'ilql'))
    add_vertical_space(20)
    st.markdown('''
    ## About
    This app is an LLM-powered (only for Summarization task) chatbot built using:
    - [Streamlit](https://streamlit.io/)
    - [RLHF](LLMs trained using RLHF)
    - [T5 Base Model on PPO and ILQL algorithms]LLM model
    
    💡 Note: No API key required!
    ''')
    
    st.write('Thanks to [Data Professor](https://youtube.com/dataprofessor) for inspiration to design of this chat app')

# Generate empty lists for generated and past.
## generated stores AI generated responses
if 'generated' not in st.session_state:
    st.session_state['generated'] = ["I'm RLHF trained LLM Chat, I can summarize paragraph for you.Choose from PPO and ILQL algorithm to get started.🤗"]
## past stores User's questions
if 'past' not in st.session_state:
    st.session_state['past'] = ['Hi!']

# Layout of input/response containers
input_container = st.container()
colored_header(label='', description='', color_name='blue-30')
response_container = st.container()

# User input
## Function for taking user provided prompt as input
def get_text():
    input_text = st.text_input("You: ", "", key="input")
    return input_text
## Applying the user input box
with input_container:
    user_input = get_text()

# Response output
## Function for taking user prompt as input followed by producing AI generated responses
def generate_response(prompt,algorithm):
    '''model="princetyagi/iqlt5base"
    prefix = "summarize: "
    tokenizer = AutoTokenizer.from_pretrained(model)
    inputs = tokenizer(prefix+prompt, return_tensors="pt").input_ids
    model = AutoModelForSeq2SeqLM.from_pretrained(model)
    outputs = model.generate(inputs, max_new_tokens=100, do_sample=False)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)'''
    if algorithm=="ppo":

        API_URL = "https://api-inference.huggingface.co/models/princetyagi/iqlt5base"
        headers = {"Authorization": "Bearer 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"}

        def query(payload):
            response = requests.post(API_URL, headers=headers, json=payload)
            return response.json()
            
        output = query({
            "inputs": prompt,"parameters": {"temperature":0},
        })
        print(output)
        return output[0]['generated_text']
    
    elif algorithm=="ilql":
        API_URL = "https://api-inference.huggingface.co/models/princetyagi/iqlt5base"
        headers = {"Authorization": "Bearer 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"}

        def query(payload):
            response = requests.post(API_URL, headers=headers, json=payload)
            return response.json()
            
        output = query({
            "inputs": prompt,
        })
        return output[0]['generated_text']

## Conditional display of AI generated responses as a function of user provided prompts
with response_container:
    if user_input and algorithm:
        response = generate_response(user_input,algorithm)
        st.session_state.past.append(user_input)
        st.session_state.generated.append(response)
        
    if st.session_state['generated']:
        for i in range(len(st.session_state['generated'])):
            message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
            message(st.session_state["generated"][i], key=str(i))
