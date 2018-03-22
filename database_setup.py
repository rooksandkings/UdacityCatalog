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

class SpaceXLaunchManifest(Base):
    __tablename__ = 'launch_manifest'

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

class Launches(Base):
    __tablename__ = 'launches'

    customer = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    description = Column(String(250))
    launch_date = Column(String(8))
    rocket_type = Column(String(250))
    launch_id = Column(Integer, ForeignKey('launch_manifest.id'))
    launch = relationship(SpaceXLaunchManifest)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'customer': self.customer,
            'description': self.description,
            'id': self.id,
            'launch_date': self.launch_date,
            'rocket_type': self.rocket_type,
        }


engine = create_engine('sqlite:///spaceXlaunchmanifestwithusers.db')


Base.metadata.create_all(engine)