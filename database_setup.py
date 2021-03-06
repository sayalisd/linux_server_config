import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
Base = declarative_base()

class User(Base):
	__tablename__ = 'user'

	id = Column(Integer, primary_key=True)
	name = Column(String(250), nullable=False)
	email = Column(String(250), nullable=False)
	picture = Column(String(250))

class Category(Base):
	__tablename__ = 'category'

	id = Column(Integer, primary_key=True)
	name = Column(String, nullable=False)
	user_id = Column(Integer, ForeignKey('user.id'))
	user = relationship(User)

	@property
	def serialize(self):
		return{
		'name' : self.name,
		'id':self.id
		}

class CategoryItem(Base):
	__tablename__ = 'category_items'

	id = Column(Integer, primary_key=True)
	title = Column(String, nullable=False)
	description = Column(String(500))
	category_id = Column(Integer,ForeignKey('category.id'))
	category = relationship(Category)
	user_id = Column(Integer, ForeignKey('user.id'))
	user = relationship(User)

	@property
	def serialize(self):
		return{
		'title' : self.title,
		'description': self.description,
		'id':self.id,
		'category_id':self.category_id
		}

engine = create_engine('sqlite:///catalog.db')
Base.metadata.create_all(engine)