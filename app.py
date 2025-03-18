import streamlit as st
from query import llm  # Import LangChain LLM

st.title("Deepseek Chatbot (LangChain)")

# Initialize session state
if "response" not in st.session_state:
    st.session_state.response = ""
if "messages" not in st.session_state:
    st.session_state.messages = []

# Function to process user input
def generate_response():
    user_input = st.session_state.user_input
    
    if user_input.strip():
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        with st.spinner("Generating response..."):  # Show spinner while querying
            response = llm.predict(user_input)  # Query API with LangChain
            
        # Clean the response (remove unwanted HTML tags)
        cleaned_response = response.replace("<think>", "").replace("</think>", "").strip()
        
        # Store response
        st.session_state.response = cleaned_response
        st.session_state.messages.append({"role": "assistant", "content": cleaned_response})
        
        # Clear the input
        st.session_state.user_input = ""

# Create a form to catch both button clicks and Enter key presses
with st.form(key="input_form", clear_on_submit=False):
    # Make it a text area instead of a single-line input
    st.text_area("Enter your prompt:", key="user_input", height=100)
    
    # Add a submit button inside the form
    submit_button = st.form_submit_button("Generate Response", on_click=generate_response)

# Display chat history
st.write("### Conversation:")
for message in st.session_state.messages:
    role = message["role"]
    content = message["content"]
    
    if role == "user":
        st.markdown(f"**You:** {content}")
    else:
        st.markdown(f"**Bot:** {content}")