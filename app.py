from flask import Flask, render_template, request, redirect, url_for, flash
from data_models import db, Author, Book
import os

app = Flask(__name__)

# DB config
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'data/library.sqlite')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "supersecretkey"


db.init_app(app)

# Home page
@app.route("/")
# Displays the home page with a searchable, sortable, paginated book list

def home():
    sort_by = request.args.get("sort", "title")
    query = request.args.get("q", "").strip()
    page = request.args.get("page", 1, type=int)
    per_page = 6

    books_query = Book.query

    if query:
        books_query = books_query.filter(Book.title.ilike(f"%{query}%"))

    if sort_by == "author":
        books_query = books_query.join(Author).order_by(Author.name)
    else:
        books_query = books_query.order_by(Book.title)

    pagination = books_query.paginate(page=page, per_page=per_page, error_out=False)
    books = pagination.items

    message = ""
    if query and not books:
        message = f"No books found matching '{query}'."

    return render_template("home.html", books=books, pagination=pagination, message=message)




# Shows a form to add a new author with name and optional birth/death dates.
@app.route("/add_author", methods=["GET", "POST"])
def add_author():
    message = ""
    if request.method == "POST":
        name = request.form.get("name")
        birth_date = request.form.get("birth_date")
        date_of_death = request.form.get("date_of_death")

        if name:
            new_author = Author(name=name, birth_date=birth_date, date_of_death=date_of_death)
            db.session.add(new_author)
            db.session.commit()
            message = f"Author '{name}' added successfully!"
        else:
            message = "Name is required."

    return render_template("add_author.html", message=message)

# Shows a form to add a new book with title, ISBN, year, and author selection.
@app.route("/add_book", methods=["GET", "POST"])
def add_book():
    message = ""
    authors = Author.query.order_by(Author.name).all()

    if request.method == "POST":
        isbn = request.form.get("isbn")
        title = request.form.get("title")
        publication_year = request.form.get("publication_year")
        author_id = request.form.get("author_id")

        if isbn and title and author_id:
            new_book = Book(
                isbn=isbn,
                title=title,
                publication_year=int(publication_year) if publication_year else None,
                author_id=int(author_id)
            )
            db.session.add(new_book)
            db.session.commit()
            message = f"Book '{title}' added successfully!"
        else:
            message = "ISBN, title, and author are required."

    return render_template("add_book.html", authors=authors, message=message)

@app.route("/book/<int:book_id>/delete", methods=["POST"])
# Deletes a specific book after confirmation
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)

    # Buch löschen
    db.session.delete(book)
    db.session.commit()

    flash(f"Book '{book.title}' deleted.")
    return redirect(url_for("home"))

@app.route("/book/<int:book_id>")
# Displays detailed information about a specific book
def book_detail(book_id):
    book = Book.query.get_or_404(book_id)
    return render_template("book_detail.html", book=book)



if __name__ == "__main__":
    app.run(debug=True)




# Create all the DB with all the tables and relations Thanks Alchemy :-)
"""
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
"""
