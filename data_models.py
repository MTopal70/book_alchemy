from flask_sqlalchemy import SQLAlchemy
"""
This module defines the core database models for the Book Alchemy Library using SQLAlchemy. 
It includes two main entities:  and , with a one-to-many relationship between them.
"""
db = SQLAlchemy()

# Author model
class Author(db.Model):
    """
    Author Model with one --> many relationship between books.
    """
    __tablename__ = "authors"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    birth_date = db.Column(db.String(20))
    date_of_death = db.Column(db.String(20))

    # Relationship to Book
    books = db.relationship("Book", backref="author", lazy=True)

    def __repr__(self):
        return f"<Author {self.name}>"

    def __str__(self):
        return f"{self.name} ({self.birth_date} – {self.date_of_death or 'present'})"

# Book model
class Book(db.Model):
    """
    A single book
    relation to author via author_id
    """
    __tablename__ = "books"

    id = db.Column(db.Integer, primary_key=True)
    isbn = db.Column(db.String(20), unique=True, nullable=False)
    title = db.Column(db.String(200), nullable=False)
    publication_year = db.Column(db.Integer)
    author_id = db.Column(db.Integer, db.ForeignKey("authors.id"), nullable=False)

    def __repr__(self):
        return f"<Book {self.title}>"

    def __str__(self):
        return f"{self.title} ({self.publication_year})"

