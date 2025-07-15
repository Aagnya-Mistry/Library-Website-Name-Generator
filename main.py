import streamlit as st
import langchain_helper

st.title("Library Website Name Generator")

genre = st.sidebar.selectbox("Select a genre", ["Fiction", "Non-Fiction", "Science Fiction", "Fantasy", "Mystery", "Romance", "Horror", "Historical", "Biography", "Self-Help"])

def generate_website_name_and_list(genre):
    return langchain_helper.generate_website_name_and_list(genre)

if genre:
    response = generate_website_name_and_list(genre)
    st.header(response["website_name"].strip())
    book_list = response['list_of_books'].strip().split('\n')
    st.write("Here are some book recommendations for the genre:", genre)
    for book in book_list:
        st.write(f"- {book.strip()}")
