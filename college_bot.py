import strealit as st
import pandas as pd
import google.generativeai as genai
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

st.set_page_config(page_title = "SVECW College Chatbot", layout = "centered")

## storing the history
if "messages" not in st.session_state :
        st.session_state.messages = []

csv_url = "svecw_details.csv"

## If Exception in reading the file 
try :
  df = pd.read_csv(scv_url)
except Exception as e :
  st.error(f"Failed to load the CSV file. Error : {e}")
  st.stop

## Filling null with empty spaces
df = df.fillna("")
## Converting to lower case
df["Question"] = df["Question"].str.lower()
df["Answer"] = df["Answer"].str.lower()

## TF-IDF vectorizer
vectorizer = TfidfVectorizer()
question_vectors = vectorizer.fit_transform(df["Question"])

API_key = "AIzaSyA1G168bJfFFdzBKv8Z4vmyWLP9mAtOZIg"

genai.configure(api_key = API_key)
model = genai.GenerativeModel('gemini-1.5-flash')


## Finding the closest question using cosine similarity
def find_closest_question(user_query, vectorizer, question_vectors, df) : 
  query_vector = vectorizer.transform([user_query.lower()])
  similarities = cosine_similarity(query_vector, question_vectors).flatten()
  best_match_index = similarities.argmax()
  best_match_score = similarities[best_match_index]

if bext_match_score > 0.3 :
  return df.iloc[best_match_index]['Answer']
else :
  return None


st.title("SVECW College Chatbot")
st.write("Welcome to the SVECW Chatbot! Ask me anything about the college.")

for message in st.session_state.messages :
    with st.chat_message(message["role"]) :
        st.markdown(message["content"])

if prompt := st.chat_input("Type your question here...") :
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user") :
        st.markdown(prompt)

    closest_answer = find_closest_question(prompt, vectorizer, question_vectors, df)
    if closest_answer:
        st.session_state.messages.append({"role": "assistant", "content": closest_answer})
        with st.chat_message("assistant"):
            st.markdown(closest_answer)
    else:
        try:
            response = model.generate_content(
                f"You are a helpful and knowledgeable chatbot for SVCEW College. Provide a detailed and specific answer to the following question: {prompt}"
            )
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            with st.chat_message("assistant"):
                st.markdown(response.text)
        except Exception as e:
            st.error(f"Sorry, I couldn't generate a response. Error: {e}")
