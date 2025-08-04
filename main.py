import streamlit as st
from ol_api import *
from create_bubbles import *
import matplotlib.pyplot as plt
import numpy as np

def main():
    st.subheader(":red[BookBubbles]: Visualize the subjects you read.")
    st.text("""This app uses Open Library's API to search for a book with matching title and author. If there's a match, the subjects of the book are returned and stored. The app creates a bubble chart to visualize the stored subjects. The more books a subject appears in, the bigger the its bubble.""")
    st.markdown("""
    1. Type a book title and the author's name. Click 'Search'. (English works best)
    2. When there's a match, you get a printout. Subjects will be stored in memory.
    3. Click 'Visualize' to see the bubble chart of all matched books below.
    4. Click 'Clear' to delete stored subjects from session memory.""")

    book_name = st.text_input("Book title")
    author_name = st.text_input("Author")

    col1, col2, col3 = st.columns(3)
    with col1:
        search_button = st.button('Search', type="primary")
    with col2:
        visualize_button = st.button('Visualize', type="secondary")
    with col3:
        clear_button = st.button('Clear', type="secondary")

    # Create a session state if it doesn't exist
    if "categories" not in st.session_state:
        st.session_state.categories = []
    if "share" not in st.session_state:
        st.session_state.share = []
    if "color" not in st.session_state:
        st.session_state.color = []
    if "input" not in st.session_state:
        st.session_state.input = ""
    if "proxy" not in st.session_state:
        st.session_state.proxy = False

    def pass_subject():
        st.session_state.input = st.session_state.user_input
        st.session_state.proxy = True

    if st.session_state.proxy == True:
        if st.session_state.input not in st.session_state.categories and st.session_state.input != "":
            st.session_state.categories.append(st.session_state.input)
            st.session_state.share.append(1)
            st.session_state.input = ""
            #st.session_state.input = False
        elif st.session_state.input in st.session_state.categories and st.session_state.input != "" and st.session_state.input != False:
            index = st.session_state.categories.index(st.session_state.input)
            st.session_state.share[index] += 1
            st.session_state.input = ""
            #st.session_state.input = False

    if search_button and len(book_name) == 0 or search_button and len(author_name) == 0 or search_button and book_name.isspace() or search_button and author_name.isspace():
        st.write("Add a book title and author name. Example: _return of the king_ and _Tolkien_")
    if search_button and len(book_name) != 0 and len(author_name) != 0 and not book_name.isspace() and not author_name.isspace():
        formatted_names = format_names(book_name, author_name)
        single_book_info = return_single_book_info(formatted_names)
        if single_book_info is None:
            st.write("Couldn't find a book with these inputs.")
        else:
            all_subjects = fetch_book_category(single_book_info[3])
            found_categories = lookup_category(all_subjects)

            string = ""
            counter = 0

            for item in single_book_info:
                counter += 1
                if counter > 2:
                    break
                string += str(item)
                string += ", "
            string = string[:-2]
            st.write(string)

            if found_categories is not None and found_categories is not False:
                for item in found_categories:
                    if item not in st.session_state.categories:
                        st.session_state.categories.append(item)
                        st.session_state.share.append(1)
                    else:
                        index = st.session_state.categories.index(item)
                        st.session_state.share[index] += 1


            elif found_categories is False:
                st.session_state.input= st.text_input("No found subjects. Give a subject: ", key="user_input")
                st.button("Add subject", type="secondary", on_click=pass_subject)

    if visualize_button:
        if len(st.session_state.categories) < 1:
            st.write("Please search books.")
        else:
            #st.write(st.session_state.categories)
            #st.write(st.session_state.share)
            st.session_state.color = create_hex_color_list(st.session_state.share)
            #st.write(st.session_state.color)

            categories = {'category': st.session_state.categories,
            'share': st.session_state.share,
            'color': st.session_state.color
                          }

            if len(categories['category'])==1:
                create_one_bubble(categories["category"][0])
            else:
                create_bubble_chart(categories)

    if clear_button:
        for key in st.session_state.keys():
            del st.session_state[key]

if __name__ == "__main__":
    main()