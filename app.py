import streamlit as st
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from transformers import pipeline
import nltk
import os
import webbrowser

  
   # Function to load HTML content
def load_html(file_name):
    with open(os.path.join("templates", file_name), "r") as f:
        return f.read()


# Set the NLTK data directory
nltk.data.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'nltk_data')))

# Download necessary NLTK data
nltk.download('punkt', download_dir=os.path.abspath(os.path.join(os.path.dirname(__file__), 'nltk_data')))
nltk.download('stopwords', download_dir=os.path.abspath(os.path.join(os.path.dirname(__file__), 'nltk_data')))

# Load a pre-trained Hugging Face model
chatbot = pipeline("text-generation", model="distilgpt2")

# Define healthcare-specific response logic (or use a model to generate responses)
def healthcare_chatbot(user_input):
    # Simple rule-based keywords to respond
    if "symptom" in user_input:
        return "Please consult a doctor for accurate advice."
    elif "appointment" in user_input:
        return "Would you like to schedule an appointment with the doctor?"
    elif "medication" in user_input:
        return "It's important to take prescribed medicines regularly. If you have concerns, consult your doctor."
    else:
        # For other inputs, use the Hugging Face model to generate a response
        try:
            response = chatbot(user_input, max_length=500, num_return_sequences=1)
            return response[0]['generated_text']
        except Exception as e:
            return "Sorry, I couldn't process your request. Please try again."

# Streamlit web app interface
def main():
    st.title("Healthcare Assistant Chatbot")
    st.markdown("""
        <style>
        .main {
            background-color: #f0f2f6;
        }
        </style>
        """, unsafe_allow_html=True)

    st.header("Welcome to the Healthcare Assistant Chatbot")
    st.subheader("How can I assist you today?")

    user_input = st.text_input("Enter your query here:")

    if st.button("Submit"):
        if user_input:
            st.write("**User:**", user_input)
            with st.spinner("Processing your query, please wait..."):
                response = healthcare_chatbot(user_input)
            st.write(f"**Healthcare Assistant:** {response}")
            print(response)

 

    # Sidebar navigation
    page = st.sidebar.selectbox("Select a page:", ["appointment.html", "reminder.html"])

    if page == "appointment.html":
        html_content = load_html("appointment.html")
        st.components.v1.html(html_content, height=400)
    
   

    elif page == "reminder.html":
        html_content = load_html("reminder.html")
        st.components.v1.html(html_content, height=400)
    


if __name__ == "__main__":
    main()