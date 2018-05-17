from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Category, Base, CategoryItem, User
 
engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine
 
DBSession = sessionmaker(bind=engine)
session = DBSession()


# Create dummy user
User1 = User(name="Sayali Dhopeshwarkar", email="sayali.dhopeshwarkar@gmail.com",
             picture='')
session.add(User1)
session.commit()


category1 = Category(user_id=1, name = "Soccer")
session.add(category1)
session.commit()

catItem1 = CategoryItem(user_id=1, title = "Two Shinguards", description = "Two Shinguards", category = category1)
session.add(catItem1)
session.commit()

catItem2 = CategoryItem(user_id=1, title = "Shinguards", description = "Shinguards", category = category1)
session.add(catItem2)
session.commit()

catItem1 = CategoryItem(user_id=1, title = "Jersey", description = "Jersey", category = category1)
session.add(catItem1)
session.commit()

catItem2 = CategoryItem(user_id=1, title = "Soccer Cleats", description = "Soccer Cleats", category = category1)
session.add(catItem2)
session.commit()



category2 = Category(user_id=1, name = "Hockey")
session.add(category2)
session.commit()

catItem1 = CategoryItem(user_id=1, title = "Stick", description = "Stick", category = category2)
session.add(catItem1)
session.commit()

catItem2 = CategoryItem(user_id=1, title = "Ball", description = "Ball", category = category2)
session.add(catItem2)
session.commit()



category3 = Category(user_id=1, name = "Snowboarding")
session.add(category3)
session.commit()

catItem1 = CategoryItem(user_id=1, title = "Goggles", description = "Goggles", category = category3)
session.add(catItem1)
session.commit()

catItem2 = CategoryItem(user_id=1, title = "Snowboard", description = "Snowboard", category = category3)
session.add(catItem2)
session.commit()



category4 = Category(user_id=1, name = "Frisbee")
session.add(category4)
session.commit()

catItem1 = CategoryItem(user_id=1, title = "Frisbee", description = "Frisbee", category = category4)
session.add(catItem1)
session.commit()



category5 = Category(user_id=1, name = "Baseball")
session.add(category5)
session.commit()

catItem1 = CategoryItem(user_id=1, title = "Bat", description = "Bat", category = category5)
session.add(catItem1)
session.commit()

catItem2 = CategoryItem(user_id=1, title = "Baseball", description = "Base ball", category = category5)
session.add(catItem2)
session.commit()



category6 = Category(user_id=1, name = "Basketball")
session.add(category6)
session.commit()

catItem1 = CategoryItem(user_id=1, title = "Basket", description = "Basket", category = category6)
session.add(catItem1)
session.commit()

catItem2 = CategoryItem(user_id=1, title = "Ball", description = "Ball", category = category6)
session.add(catItem2)
session.commit()



category7 = Category(user_id=1, name = "Skating")
session.add(category7)
session.commit()

catItem1 = CategoryItem(user_id=1, title = "Skating board", description = "Skating board", category = category7)
session.add(catItem1)
session.commit()



print "added catalog items!"
