from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import SpaceXLaunchManifest, Base, Launches, User

engine = create_engine('sqlite:///spaceXlaunchmanifestwithusers.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


# Create dummy user
User1 = User(name="Robo Barista", email="tinnyTim@udacity.com",
             picture='https://pbs.twimg.com/profile_images/2671170543/18debd694829ed78203a5a36dd364160_400x400.png')
session.add(User1)
session.commit()

# Menu for UrbanBurger
Launch1 = SpaceXLaunchManifest(user_id=1, name="F91")

session.add(Launch1)
session.commit()

customer1 = Launches(user_id=1, customer="Blah Company", description="launching x rocket description",
                     launch_date="11/11/2011", rocket_type="F9", launch=Launch1)

session.add(customer1)
session.commit()


# launches1 = Launches(user_id=1, name="French Fries", description="with garlic and parmesan",
#                      launch_date="$2.99", rocket_type="Appetizer", restaurant=restaurant1)

# session.add(launches1)
# session.commit()

# launches2 = Launches(user_id=1, name="Chicken Burger", description="Juicy grilled chicken patty with tomato mayo and lettuce",
#                      launch_date="$5.50", rocket_type="Entree", restaurant=restaurant1)

# session.add(launches2)
# session.commit()

# launches3 = launches(user_id=1, name="Chocolate Cake", description="fresh baked and served with ice cream",
#                      launch_date="$3.99", rocket_type="Dessert", restaurant=restaurant1)

# session.add(launches3)
# session.commit()

# launches4 = launches(user_id=1, name="Sirloin Burger", description="Made with grade A beef",
#                      launch_date="$7.99", rocket_type="Entree", restaurant=restaurant1)

# session.add(launches4)
# session.commit()

# launches5 = launches(user_id=1, name="Root Beer", description="16oz of refreshing goodness",
#                      launch_date="$1.99", rocket_type="Beverage", restaurant=restaurant1)

# session.add(launches5)
# session.commit()

# launches6 = launches(user_id=1, name="Iced Tea", description="with Lemon",
#                      launch_date="$.99", rocket_type="Beverage", restaurant=restaurant1)

# session.add(launches6)
# session.commit()

# launches7 = launches(user_id=1, name="Grilled Cheese Sandwich",
#                      description="On texas toast with American Cheese", launch_date="$3.49", rocket_type="Entree", restaurant=restaurant1)

# session.add(launches7)
# session.commit()

# launches8 = launches(user_id=1, name="Veggie Burger", description="Made with freshest of ingredients and home grown spices",
#                      launch_date="$5.99", rocket_type="Entree", restaurant=restaurant1)

# session.add(launches8)
# session.commit()


# # Menu for Super Stir Fry
# restaurant2 = Restaurant(user_id=1, name="Super Stir Fry")

# session.add(restaurant2)
# session.commit()


# launches1 = launches(user_id=1, name="Chicken Stir Fry", description="With your choice of noodles vegetables and sauces",
#                      launch_date="$7.99", rocket_type="Entree", restaurant=restaurant2)

# session.add(launches1)
# session.commit()

# launches2 = launches(user_id=1, name="Peking Duck",
#                      description=" A famous duck dish from Beijing[1] that has been prepared since the imperial era. The meat is prized for its thin, crisp skin, with authentic versions of the dish serving mostly the skin and little meat, sliced in front of the diners by the cook", launch_date="$25", rocket_type="Entree", restaurant=restaurant2)

# session.add(launches2)
# session.commit()

# launches3 = launches(user_id=1, name="Spicy Tuna Roll", description="Seared rare ahi, avocado, edamame, cucumber with wasabi soy sauce ",
#                      launch_date="15", rocket_type="Entree", restaurant=restaurant2)

# session.add(launches3)
# session.commit()

# launches4 = launches(user_id=1, name="Nepali Momo ", description="Steamed dumplings made with vegetables, spices and meat. ",
#                      launch_date="12", rocket_type="Entree", restaurant=restaurant2)

# session.add(launches4)
# session.commit()

# launches5 = launches(user_id=1, name="Beef Noodle Soup", description="A Chinese noodle soup made of stewed or red braised beef, beef broth, vegetables and Chinese noodles.",
#                      launch_date="14", rocket_type="Entree", restaurant=restaurant2)

# session.add(launches5)
# session.commit()

# launches6 = launches(user_id=1, name="Ramen", description="a Japanese noodle soup dish. It consists of Chinese-style wheat noodles served in a meat- or (occasionally) fish-based broth, often flavored with soy sauce or miso, and uses toppings such as sliced pork, dried seaweed, kamaboko, and green onions.",
#                      launch_date="12", rocket_type="Entree", restaurant=restaurant2)

# session.add(launches6)
# session.commit()


# # Menu for Panda Garden
# restaurant1 = Restaurant(user_id=1, name="Panda Garden")

# session.add(restaurant1)
# session.commit()


# launches1 = launches(user_id=1, name="Pho", description="a Vietnamese noodle soup consisting of broth, linguine-shaped rice noodles called banh pho, a few herbs, and meat.",
#                      launch_date="$8.99", rocket_type="Entree", restaurant=restaurant1)

# session.add(launches1)
# session.commit()

# launches2 = launches(user_id=1, name="Chinese Dumplings", description="a common Chinese dumpling which generally consists of minced meat and finely chopped vegetables wrapped into a piece of dough skin. The skin can be either thin and elastic or thicker.",
#                      launch_date="$6.99", rocket_type="Appetizer", restaurant=restaurant1)

# session.add(launches2)
# session.commit()

# launches3 = launches(user_id=1, name="Gyoza", description="light seasoning of Japanese gyoza with salt and soy sauce, and in a thin gyoza wrapper",
#                      launch_date="$9.95", rocket_type="Entree", restaurant=restaurant1)

# session.add(launches3)
# session.commit()

# launches4 = launches(user_id=1, name="Stinky Tofu", description="Taiwanese dish, deep fried fermented tofu served with pickled cabbage.",
#                      launch_date="$6.99", rocket_type="Entree", restaurant=restaurant1)

# session.add(launches4)
# session.commit()

# launches2 = launches(user_id=1, name="Veggie Burger", description="Juicy grilled veggie patty with tomato mayo and lettuce",
#                      launch_date="$9.50", rocket_type="Entree", restaurant=restaurant1)

# session.add(launches2)
# session.commit()


# # Menu for Thyme for that
# restaurant1 = Restaurant(user_id=1, name="Thyme for That Vegetarian Cuisine ")

# session.add(restaurant1)
# session.commit()


# launches1 = launches(user_id=1, name="Tres Leches Cake", description="Rich, luscious sponge cake soaked in sweet milk and topped with vanilla bean whipped cream and strawberries.",
#                      launch_date="$2.99", rocket_type="Dessert", restaurant=restaurant1)

# session.add(launches1)
# session.commit()

# launches2 = launches(user_id=1, name="Mushroom risotto", description="Portabello mushrooms in a creamy risotto",
#                      launch_date="$5.99", rocket_type="Entree", restaurant=restaurant1)

# session.add(launches2)
# session.commit()

# launches3 = launches(user_id=1, name="Honey Boba Shaved Snow",
#                      description="Milk snow layered with honey boba, jasmine tea jelly, grass jelly, caramel, cream, and freshly made mochi", launch_date="$4.50", rocket_type="Dessert", restaurant=restaurant1)

# session.add(launches3)
# session.commit()

# launches4 = launches(user_id=1, name="Cauliflower Manchurian", description="Golden fried cauliflower florets in a midly spiced soya,garlic sauce cooked with fresh cilantro, celery, chilies,ginger & green onions",
#                      launch_date="$6.95", rocket_type="Appetizer", restaurant=restaurant1)

# session.add(launches4)
# session.commit()

# launches5 = launches(user_id=1, name="Aloo Gobi Burrito", description="Vegan goodness. Burrito filled with rice, garbanzo beans, curry sauce, potatoes (aloo), fried cauliflower (gobi) and chutney. Nom Nom",
#                      launch_date="$7.95", rocket_type="Entree", restaurant=restaurant1)

# session.add(launches5)
# session.commit()

# launches2 = launches(user_id=1, name="Veggie Burger", description="Juicy grilled veggie patty with tomato mayo and lettuce",
#                      launch_date="$6.80", rocket_type="Entree", restaurant=restaurant1)

# session.add(launches2)
# session.commit()


# # Menu for Tony's Bistro
# restaurant1 = Restaurant(user_id=1, name="Tony\'s Bistro ")

# session.add(restaurant1)
# session.commit()


# launches1 = launches(user_id=1, name="Shellfish Tower", description="Lobster, shrimp, sea snails, crawfish, stacked into a delicious tower",
#                      launch_date="$13.95", rocket_type="Entree", restaurant=restaurant1)

# session.add(launches1)
# session.commit()

# launches2 = launches(user_id=1, name="Chicken and Rice", description="Chicken... and rice",
#                      launch_date="$4.95", rocket_type="Entree", restaurant=restaurant1)

# session.add(launches2)
# session.commit()

# launches3 = launches(user_id=1, name="Mom's Spaghetti", description="Spaghetti with some incredible tomato sauce made by mom",
#                      launch_date="$6.95", rocket_type="Entree", restaurant=restaurant1)

# session.add(launches3)
# session.commit()

# launches4 = launches(user_id=1, name="Choc Full O\' Mint (Smitten\'s Fresh Mint Chip ice cream)",
#                      description="Milk, cream, salt, ..., Liquid nitrogen magic", launch_date="$3.95", rocket_type="Dessert", restaurant=restaurant1)

# session.add(launches4)
# session.commit()

# launches5 = launches(user_id=1, name="Tonkatsu Ramen", description="Noodles in a delicious pork-based broth with a soft-boiled egg",
#                      launch_date="$7.95", rocket_type="Entree", restaurant=restaurant1)

# session.add(launches5)
# session.commit()


# # Menu for Andala's
# restaurant1 = Restaurant(user_id=1, name="Andala\'s")

# session.add(restaurant1)
# session.commit()


# launches1 = launches(user_id=1, name="Lamb Curry", description="Slow cook that thang in a pool of tomatoes, onions and alllll those tasty Indian spices. Mmmm.",
#                      launch_date="$9.95", rocket_type="Entree", restaurant=restaurant1)

# session.add(launches1)
# session.commit()

# launches2 = launches(user_id=1, name="Chicken Marsala", description="Chicken cooked in Marsala wine sauce with mushrooms",
#                      launch_date="$7.95", rocket_type="Entree", restaurant=restaurant1)

# session.add(launches2)
# session.commit()

# launches3 = launches(user_id=1, name="Potstickers", description="Delicious chicken and veggies encapsulated in fried dough.",
#                      launch_date="$6.50", rocket_type="Appetizer", restaurant=restaurant1)

# session.add(launches3)
# session.commit()

# launches4 = launches(user_id=1, name="Nigiri Sampler", description="Maguro, Sake, Hamachi, Unagi, Uni, TORO!",
#                      launch_date="$6.75", rocket_type="Appetizer", restaurant=restaurant1)

# session.add(launches4)
# session.commit()

# launches2 = launches(user_id=1, name="Veggie Burger", description="Juicy grilled veggie patty with tomato mayo and lettuce",
#                      launch_date="$7.00", rocket_type="Entree", restaurant=restaurant1)

# session.add(launches2)
# session.commit()


# # Menu for Auntie Ann's
# restaurant1 = Restaurant(user_id=1, name="Auntie Ann\'s Diner' ")

# session.add(restaurant1)
# session.commit()

# launches9 = launches(user_id=1, name="Chicken Fried Steak",
#                      description="Fresh battered sirloin steak fried and smothered with cream gravy", launch_date="$8.99", rocket_type="Entree", restaurant=restaurant1)

# session.add(launches9)
# session.commit()


# launches1 = launches(user_id=1, name="Boysenberry Sorbet", description="An unsettlingly huge amount of ripe berries turned into frozen (and seedless) awesomeness",
#                      launch_date="$2.99", rocket_type="Dessert", restaurant=restaurant1)

# session.add(launches1)
# session.commit()

# launches2 = launches(user_id=1, name="Broiled salmon", description="Salmon fillet marinated with fresh herbs and broiled hot & fast",
#                      launch_date="$10.95", rocket_type="Entree", restaurant=restaurant1)

# session.add(launches2)
# session.commit()

# launches3 = launches(user_id=1, name="Morels on toast (seasonal)",
#                      description="Wild morel mushrooms fried in butter, served on herbed toast slices", launch_date="$7.50", rocket_type="Appetizer", restaurant=restaurant1)

# session.add(launches3)
# session.commit()

# launches4 = launches(user_id=1, name="Tandoori Chicken", description="Chicken marinated in yoghurt and seasoned with a spicy mix(chilli, tamarind among others) and slow cooked in a cylindrical clay or metal oven which gets its heat from burning charcoal.",
#                      launch_date="$8.95", rocket_type="Entree", restaurant=restaurant1)

# session.add(launches4)
# session.commit()

# launches2 = launches(user_id=1, name="Veggie Burger", description="Juicy grilled veggie patty with tomato mayo and lettuce",
#                      launch_date="$9.50", rocket_type="Entree", restaurant=restaurant1)

# session.add(launches2)
# session.commit()

# launches10 = launches(user_id=1, name="Spinach Ice Cream", description="vanilla ice cream made with organic spinach leaves",
#                       launch_date="$1.99", rocket_type="Dessert", restaurant=restaurant1)

# session.add(launches10)
# session.commit()


# # Menu for Cocina Y Amor
# restaurant1 = Restaurant(user_id=1, name="Cocina Y Amor ")

# session.add(restaurant1)
# session.commit()


# launches1 = launches(user_id=1, name="Super Burrito Al Pastor",
#                      description="Marinated Pork, Rice, Beans, Avocado, Cilantro, Salsa, Tortilla", launch_date="$5.95", rocket_type="Entree", restaurant=restaurant1)

# session.add(launches1)
# session.commit()

# launches2 = launches(user_id=1, name="Cachapa", description="Golden brown, corn-based Venezuelan pancake; usually stuffed with queso telita or queso de mano, and possibly lechon. ",
#                      launch_date="$7.99", rocket_type="Entree", restaurant=restaurant1)

# session.add(launches2)
# session.commit()


# restaurant1 = Restaurant(user_id=1, name="State Bird Provisions")
# session.add(restaurant1)
# session.commit()

# launches1 = launches(user_id=1, name="Chantrelle Toast", description="Crispy Toast with Sesame Seeds slathered with buttery chantrelle mushrooms",
#                      launch_date="$5.95", rocket_type="Appetizer", restaurant=restaurant1)

# session.add(launches1)
# session.commit

# launches1 = launches(user_id=1, name="Guanciale Chawanmushi",
#                      description="Japanese egg custard served hot with spicey Italian Pork Jowl (guanciale)", launch_date="$6.95", rocket_type="Dessert", restaurant=restaurant1)

# session.add(launches1)
# session.commit()


# launches1 = launches(user_id=1, name="Lemon Curd Ice Cream Sandwich",
#                      description="Lemon Curd Ice Cream Sandwich on a chocolate macaron with cardamom meringue and cashews", launch_date="$4.25", rocket_type="Dessert", restaurant=restaurant1)

# session.add(launches1)
# session.commit()


print "added some launches!"