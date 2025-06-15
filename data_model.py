
from flask_sqlalchemy import SQLAlchemy, Column, Integer, String, Float

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100))
    def __repr__(self):
        return f"id: {self.id} name:{self.name}"

    def __str__(self):
        if not self.date_of_death:
            return f"name:{self.name}"

class Movie(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    director = Column(String(100), nullable=False)
    release_year = Column(Integer)
    rating = Column(Float)
    def __repr__(self):
        return (f"id: {self.id} name:{self.name} director:{self.director} "
                f"release_year:{self.release_year} rating:{self.rating}")

    def __str__(self):
        return (f"name:{self.name} director:{self.director} "
                f"release_year:{self.release_year} rating:{self.rating}")
