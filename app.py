import sqlite3
import requests
import streamlit as st

DB_PATH = "books.db"

def get_connection():
    return sqlite3.connect(DB_PATH)


def create_books_table():
    conn = get_connection()
    with conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT,
                cover_url TEXT,
                status TEXT NOT NULL,
                rating INTEGER,
                notes TEXT
            )
        """)
    conn.close()

def search_book(query):
    """Look up a book by title via the Open Library API."""
    resp = requests.get(
        "https://openlibrary.org/search.json",
        params={"q": query, "limit": 1},
    )
    resp.raise_for_status()
    docs = resp.json().get("docs", [])
    if not docs:
        return None

    #docs is the list of book results from the API
    doc = docs[0]
    cover_id = doc.get("cover_i")
    return {
        "title": doc.get("title", query),
        "author": ", ".join(doc.get("author_name", [])) or "Unknown",
        "cover_url": f"https://covers.openlibrary.org/b/id/{cover_id}-M.jpg" if cover_id else None,
    }
def add_book(title, author, cover_url, status, rating=None, notes=""):
    conn = get_connection()
    with conn:
        conn.execute(
            "INSERT INTO books (title, author, cover_url, status, rating, notes) VALUES (?, ?, ?, ?, ?, ?)",
            (title, author, cover_url, status, rating, notes),
        )
    conn.close()


def get_all_books():
    conn = get_connection()
    with conn:
        rows = conn.execute(
            "SELECT id, title, author, cover_url, status, rating, notes FROM books ORDER BY id DESC"
        ).fetchall()
    conn.close()
    return rows


def update_book(book_id, status, rating, notes):
    conn = get_connection()
    with conn:
        conn.execute(
            "UPDATE books SET status = ?, rating = ?, notes = ? WHERE id = ?",
            (status, rating, notes, book_id),
        )
    conn.close()


def delete_book(book_id):
    conn = get_connection()
    with conn:
        conn.execute("DELETE FROM books WHERE id = ?", (book_id,))
    conn.close()


STATUS_OPTIONS = ["Want to Read", "Reading", "Read", "DNF"]

create_books_table()

st.title("Book Tracker")

st.header("Add a Book")
search_query = st.text_input("Book title")

if "found_book" not in st.session_state:
    st.session_state.found_book = None

if st.button("Search"):
    st.session_state.found_book = search_book(search_query) if search_query else None

found = st.session_state.found_book
if found:
    col1, col2 = st.columns([1, 3])
    with col1:
        if found["cover_url"]:
            st.image(found["cover_url"], width=100)
    with col2:
        st.write(f"**{found['title']}** by {found['author']}")

    status = st.selectbox("Status", STATUS_OPTIONS)
    if st.button("Add to list"):
        add_book(found["title"], found["author"], found["cover_url"], status)
        st.session_state.found_book = None
        st.success("Book added.")
        st.rerun()
elif search_query:
    st.info("No results. Try a different search.")

st.header("My Books")
books = get_all_books()

if not books:
    st.write("No books yet — search above to add your first one.")

for book_id, title, author, cover_url, status, rating, notes in books:
    with st.expander(f"{title} — {author} ({status})"):
        if cover_url:
            st.image(cover_url, width=100)

        new_status = st.selectbox(
            "Status", STATUS_OPTIONS, index=STATUS_OPTIONS.index(status), key=f"status_{book_id}"
        )
        new_rating = st.slider("Rating", 0, 5, rating or 0, key=f"rating_{book_id}")
        new_notes = st.text_area("Notes", notes or "", key=f"notes_{book_id}")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("Save", key=f"save_{book_id}"):
                update_book(book_id, new_status, new_rating, new_notes)
                st.success("Saved.")
                st.rerun()
        with col2:
            if st.button("Delete", key=f"delete_{book_id}"):
                delete_book(book_id)
                st.rerun()
