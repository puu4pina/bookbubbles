import json
import requests
import streamlit as st
search_base_url = "https://openlibrary.org/search.json?q="
category_base_url = "https://openlibrary.org/works/"

# Formats input strings to be used in request
def format_names(title,author):
    search_terms = []
    book_name = title
    book_name = book_name.lower()
    book_name = book_name.replace(" ", "+")
    author_name = author
    author_name = author_name.lower()
    author_name = author_name.replace(" ", "+")
    search_terms.append(book_name)
    search_terms.append(author_name)
    return search_terms

# Fetch book subjects with work_id
def fetch_book_category(work_id):

    search_url = f"{category_base_url}{work_id}.json"
    answer = requests.get(search_url)

    if answer.status_code == 200:
        work_dict = answer.json()
        category_data = work_dict.get('subjects')
        #print(category_data)
        return category_data

    else:
        print("Failed to find data with this Work ID")

# Compare found subjects to most common ones in list and return the ones that match
def lookup_category(category_list):
    topics = ["Artificial Intelligence", "Machine Learning", "Arts", "Architecture", "Art History", "Dance", "Design", "Fashion", "Film", "Graphic Design", "Music", "Music Theory", "Women", "Painting", "Photography", "Animals", "Fantasy", "Adventure", "Dystopian", "Mythology", "Satire", "Historical Fiction", "Horror", "Humor", "Magic", "Mystery", " Detective", "Plays", "Poetry", "Romance", "Science Fiction", "Short Stories", "Thriller", "Science", "Mathematics", "Biology", "Chemistry", "Physics", "Programming", "Business", "Finance", "Management", "Politics", "Political", "Entrepreneurship", "Economics", "Business Success", "Picture Books", "History", "Ancient Civilization", "Archaeology", "Anthropology", "World War II", "Social Life", "Health", "Wellness", "Cooking", "Cookbooks", "Mental Health", "Exercise", "Nutrition", "Self-help", "Biography", "Autobiographies", "Philosophy", "History", "Politics", "Government", "World War II", "Kings", "Queens", "Composers", "Artists", "Social Sciences", "Anthropology", "Religion", "Political Science", "Psychology", "Places", "Geography", "Psychology", "Algebra", "Chemistry", "English Language", "Physics", "Computer Science"]
    found_topics = []
    for category in category_list:
        for topic in topics:
            if topic in category:
                if topic not in found_topics:
                    found_topics.append(topic)

    #weight = 1/len(found_topics)
    if len(found_topics) > 0:
        return found_topics
    else:
        st.write("No found subjects.")
        return False

# Fetch info from all matches
def fetch_books_info(names_list):
    search_url = f"{search_base_url}{names_list[0]}&author={names_list[1]}"
    answer = requests.get(search_url)

    if answer.status_code == 200:
        books_dict = answer.json()
        all_books_data = books_dict.get('docs')
        return all_books_data

    else:
        print("Failed to find data with this book name")

# Return the info from a single book
def return_single_book_info(names_list):

    all_books = fetch_books_info(names_list)

    for book in all_books:
        try:
            authors_name = book.get('author_name')[0]
            fixed_authors_name = authors_name.lower()
            fixed_authors_name = fixed_authors_name.replace(" ", "+")
            books_name = book.get('title')
            fixed_books_name = books_name.lower()
            fixed_books_name = fixed_books_name.replace(" ", "+")
            work_id = book.get('key')
            work_id = work_id[7:]
            published = book.get('first_publish_year')
            categories = fetch_book_category(work_id)

            if names_list[0] in fixed_books_name and names_list[1] in fixed_authors_name and categories is not None and len(categories) > 0:

                book_data = []
                book_data.append(books_name)
                book_data.append(authors_name)
                book_data.append(published)
                book_data.append(work_id)
                all_books = []
                return book_data


        except TypeError:
            pass

