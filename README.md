# Book Tracker

A simple personal reading tracker built with Streamlit and SQLite. Search for a book via the Open Library API, add it to your list, and track its status, rating, and notes as you read.

## Features

- **Search and auto-fill** — look up a book by title using the Open Library API, which pulls in the author and cover image automatically
- **Status tracking** — mark books as Want to Read, Reading, Read, or DNF
- **Star rating** — rate books out of 5 once you've finished them
- **Notes** — jot down thoughts on each book
- **Edit and delete** — update or remove any book from your list at any time

## Tech Stack

- **Python**
- **Streamlit** — web interface
- **SQLite** — local storage (`books.db`)
- **Open Library API** — book search and cover art (no API key required)

## Setup

1. Clone the repository:
   ```
   git clone <your-repo-url>
   cd book-tracker
   ```

2. Create and activate an environment, then install dependencies:
   ```
   micromamba create -n book-tracker python=3.12
   micromamba activate book-tracker
   pip install -r requirements.txt
   ```

3. Run the app:
   ```
   streamlit run app.py
   ```

4. Open the app in your browser at `http://localhost:8501`

## Project Structure

```
book-tracker/
├── app.py              # Main application: database logic and Streamlit UI
├── requirements.txt    # Python dependencies
├── books.db             # SQLite database (created automatically on first run)
└── README.md
```

## Status

Early-stage personal project — built as a learning exercise.
