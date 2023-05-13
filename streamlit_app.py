import numpy as np
import pandas as pd
import streamlit as st
import altair as alt
import openai
openai.api_key = st.secrets["API_key"]
from streamlit.hashing import _get_code_with_cache
import hashlib

# Define a custom class to hold session state
class SessionState:
    def __init__(self, **kwargs):
        self.hash_funcs = {"md5": hashlib.md5}
        for key, val in kwargs.items():
            setattr(self, key, val)

    def __getitem__(self, key):
        return getattr(self, key)

    def __setitem__(self, key, value):
        setattr(self, key, value)

    def __contains__(self, key):
        return hasattr(self, key)

    def clear(self):
        for key in self.__dict__.keys():
            delattr(self, key)

    def sync(self):
        session_id = st.report_thread.get_report_ctx().session_id
        session = _get_session(session_id)
        if session is None:
            return
        session_state = session.get("session_state")
        if session_state is None:
            return
        if self in session_state:
            return
        session_state[self] = {}
        for key in self.__dict__.keys():
            if key not in ["hash_funcs"]:
                val = getattr(self, key)
                session_state[self][key] = self._hash(val)

    def _hash(self, val):
        if isinstance(val, bytes):
            return val
        hasher = self.hash_funcs.get("md5")
        return hasher(val.encode("utf-8")).hexdigest()

def _get_session(session_id):
    session_info = st._get_session_info(session_id)
    if session_info is None:
        return None
    return session_info.session

# Create a new instance of SessionState
session_state = SessionState(history=[])



def get_reply(input_string): 
    response = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=[
          {"role": "system", "content": "You are a helpful assistant."},
          {"role": "user", "content": "What is Silak?"},
          {"role": "assistant", "content": "Established in 1979, SILAK stands for Service, Integrity, Leadership, Advocacy, \
          and Kinship, and is the oldest departmental publication of West Visayas State University (WVSU). \
          It serves as the student publication of the university's flagship college, the College of Education (COE), \
          with the core value of commitment to development journalisms."},
          {"role": "user", "content": "What are important achievements of Silak?"},
          {"role": "assistant", "content": "In 1993, under the guidance of the late Prof. Gladys Cordero, SILAK’s \
          longest-serving adviser for almost 20 years, the publication won the Philippine Information Agency’s \
          Gawad Graciano Lopez-Jaena Hall of Fame Award for having been deemed the Best Departmental Paper in \
          the region for six consecutive years. The honor was once again restored in December 2021, \
          after maintaining the distinction for three consecutive years under the watch of current SILAK \
          Adviser Dr. Hazel P. Villa."},
          {"role": "user", "content" : "What are the innovations?"},
          {"role": "assistant", "content": "SILAK has also innovated through the years. In 2017, it was the first to introduce a broadcast arm in the university known as SILAK TV, where its first episode was aired during the 115th founding anniversary of WVSU. In the same year, the publication changed its name from SILAK Publications Inc. to SILAK Media, Inc. to reflect its three divisions: SILAK Print, SILAK TV, and SILAK Online."},
          {"role": "user", "content" : "What is the mission of Silak?"},
          {"role": "assistant", "content": "SILAK Media shall live by its mission of being committed to development journalism and the improvement of communities."},

          {"role": "user", "content": "What is the purpose?"},
          {"role": "assistant", "content": "Promote a student information media that is highly informative, socially involved, dynamic, truthful, impartial, and reliable. Develop the skills of the members of its editorial staff through training, seminars, workshops, conferences, and symposia that are in line with campus journalism, creative writing, and academic writing. Establish a strong sense of loyalty to the ideals upheld by WVSUas the bearer of goodwill in terms of student publication."},
          {"role": "user", "content": "What are the objectives?"},
          {"role": "assistant", "content": "- Publish students’ opinions on the issues that concern them. Conduct training, seminars, workshops, conferences, and symposia in order to expand its scope of service and community involvement. Promote the passion for writing among members of its editorial staff and students of the COE and of WVSU through responsible writing in the fields of journalism, creative writing, and academic writing. Promote the passion for Broadcast Journalism with its SILAK TV Division. Ensure quick and reliable information dissemination with its SILAK Online division."},
          {"role": "user", "content": input_string}
        ]
    )

    # Print the generated response
    answer = response['choices'][0]['message']['content']
    return answer

# Define the Streamlit app
def app():
    st.header("Welcome to WVSU Silak Publication Chatbot")
    st.subheader("Louie F. Cervantes M.Eng. \n(c) 2023 WVSU College of ICT")
    
    st.title("Silak Chatbot is chatGPT-powered AI")
    st.write("This experimental project demonstrates how AI can be imbued with specific knowledge on a set of topics. Like chatGPT, the bot can engage the user in a conversation. But prompt engineering has provided this app with specific information beyond the training of chatGPT.  This particular program is designed to be a helpful assistant to a potential applicant to be a writer or staff member of Silak Media.")

    st.write("This bot can answer questions about the history, mission, purpose, objectives, innovations, milestones awards and other information specifically about Silak Media.")
    
    st.write("The potential applications of this technology is fully-automated AI bots to respond to Q and A on such topics as admission requirements, academic policies or any knowledge domain.")
    
    # Create two columns, with the first column wider than the second
    left_column, right_column = st.beta_columns([2, 1])

    
    # Add content to the left column
    with left_column:
        # Create a multiline text field
        user_input = st.text_area('Input your question here:', height=10)

        # Display the text when the user submits the form
        if st.button('Submit'):
            session_state.history.append('user: ' + user_input)
            output = get_reply(user_input)
            history.append('chatBot: ' + output)
            session_state.history.append('chatBot: ' + output)
            session_state.sync()
            st.write(output)
            with right_column:
                for item in range(len(history)):
                    st.write(session_state.history)

# Run the app
if __name__ == "__main__":
    app()
