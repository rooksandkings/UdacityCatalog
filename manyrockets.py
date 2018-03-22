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

# Create sample Mission
mission1 = SpaceXLaunchManifest(user_id=1, name="Iridium Next")

session.add(mission1)
session.commit()

# Create sample Launches
launch1 = Launches(user_id=1, customer="Iridium Communications", description="Iridium (Flight 1)",
                     launch_date="1/14/2017", rocket_type="Falcon 9 v1.1", launch=mission1)

session.add(launch1)
session.commit()

launch2 = Launches(user_id=1, customer="Iridium Communications", description="Iridium (Flight 2)",
                     launch_date="6/25/2017", rocket_type="Falcon 9 v1.1", launch=mission1)

session.add(launch2)
session.commit()

launch3 = Launches(user_id=1, customer="Iridium Communications", description="Iridium (Flight 3)",
                     launch_date="10/9/2017", rocket_type="Falcon 9 v1.1", launch=mission1)

session.add(launch3)
session.commit()

launch4 = Launches(user_id=1, customer="Iridium Communications", description="Iridium (Flight 4)",
                     launch_date="12/22/2017", rocket_type="Falcon 9 v1.1", launch=mission1)

session.add(launch4)
session.commit()

print "Launches Added!"
