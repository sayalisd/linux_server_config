from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Category, Base, CategoryItem
 
engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine
 
DBSession = sessionmaker(bind=engine)
session = DBSession()



category1 = Category(name = "Soccer")
session.add(category1)
session.commit()

catItem1 = CategoryItem(title = "Two Shinguards", description = "Two Shinguards", category = category1)
session.add(catItem1)
session.commit()

catItem2 = CategoryItem(title = "Shinguards", description = "Shinguards", category = category1)
session.add(catItem2)
session.commit()

catItem1 = CategoryItem(title = "Jersey", description = "Jersey", category = category1)
session.add(catItem1)
session.commit()

catItem2 = CategoryItem(title = "Soccer Cleats", description = "Soccer Cleats", category = category1)
session.add(catItem2)
session.commit()



category2 = Category(name = "Hockey")
session.add(category2)
session.commit()

catItem1 = CategoryItem(title = "Stick", description = "Stick", category = category2)
session.add(catItem1)
session.commit()

catItem2 = CategoryItem(title = "Ball", description = "Ball", category = category2)
session.add(catItem2)
session.commit()



category3 = Category(name = "Snowboarding")
session.add(category3)
session.commit()

catItem1 = CategoryItem(title = "Goggles", description = "Goggles", category = category3)
session.add(catItem1)
session.commit()

catItem2 = CategoryItem(title = "Snowboard", description = "Snowboard", category = category3)
session.add(catItem2)
session.commit()



category4 = Category(name = "Frisbee")
session.add(category4)
session.commit()

catItem1 = CategoryItem(title = "Frisbee", description = "Frisbee", category = category4)
session.add(catItem1)
session.commit()



category5 = Category(name = "Baseball")
session.add(category5)
session.commit()

catItem1 = CategoryItem(title = "Bat", description = "Bat", category = category5)
session.add(catItem1)
session.commit()

catItem2 = CategoryItem(title = "Ball", description = "Ball", category = category5)
session.add(catItem2)
session.commit()



category6 = Category(name = "Basketball")
session.add(category6)
session.commit()

catItem1 = CategoryItem(title = "Basket", description = "Basket", category = category6)
session.add(catItem1)
session.commit()

catItem2 = CategoryItem(title = "Ball", description = "Ball", category = category6)
session.add(catItem2)
session.commit()



category7 = Category(name = "Skating")
session.add(category7)
session.commit()

catItem1 = CategoryItem(title = "Skating board", description = "Skating board", category = category7)
session.add(catItem1)
session.commit()



print "added catalog items!"
