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


# class Restaurant(Base):
#     __tablename__ = 'restaurant'

#     id = Column(Integer, primary_key=True)
#     name = Column(String(250), nullable=False)
#     user_id = Column(Integer, ForeignKey('user.id'))
#     user = relationship(User)

#     @property
#     def serialize(self):
#         """Return object data in easily serializeable format"""
#         return {
#             'name': self.name,
#             'id': self.id,
#         }

# class MenuItem(Base):
#     __tablename__ = 'menu_item'

#     name = Column(String(80), nullable=False)
#     id = Column(Integer, primary_key=True)
#     description = Column(String(250))
#     price = Column(String(8))
#     course = Column(String(250))
#     restaurant_id = Column(Integer, ForeignKey('restaurant.id'))
#     restaurant = relationship(Restaurant)
#     user_id = Column(Integer, ForeignKey('user.id'))
#     user = relationship(User)

class SpaceX(Base):
    __tablename__ = 'launch'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'id': self.id,
        }

class Rockets(Base):
    __tablename__ = 'rocket'

    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    description = Column(String(250))
    launch_date = Column(String(8))
    rocket_type = Column(String(250))
    rocket_id = Column(Integer, ForeignKey('launch.id'))
    launch = relationship(SpaceX)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'description': self.description,
            'id': self.id,
            'launch_date': self.launch_date,
            'rocket_type': self.rocket_type,
        }


engine = create_engine('sqlite:///spaceXlaunchmanifestwithusers.db')


Base.metadata.create_all(engine)