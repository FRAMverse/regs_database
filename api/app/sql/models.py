from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from .database import Base


class Rules(Base):
    __tablename__ = "rules"
    rules_id = Column(UUID, primary_key=True, server_default='uuid_generate_v4()')
    catch_area_id = Column(UUID, ForeignKey('catch_area.catch_area_id'))
    start_rule_datetime = Column(Date)
    end_rule_datetime = Column(Date)
    species_id = Column(UUID, ForeignKey('species_lut.species_id'))
    regulation_type_id = Column(UUID, ForeignKey('regulation_type_lut.regulation_type_id'))
    catch_area = relationship("CatchAreaRaw", back_populates="rules", uselist=False)
    regulation = relationship("RegulationTypeLUT", back_populates="rules", uselist=False)
    species = relationship("SpeciesLUT", back_populates="rules", uselist=False)


class CatchAreaRaw(Base):
    __tablename__ = "catch_area"
    catch_area_id = Column(UUID, primary_key=True, server_default='uuid_generate_v4()')
    description = Column(String)
    geom = Column(String)
    rules = relationship("Rules", back_populates="catch_area")

class CatchArea(Base):
    __tablename__ = "catch_area_geojson"
    catch_area_id = Column(String, primary_key=True)
    description = Column(String)
    geom = Column(String)


class RegulationTypeLUT(Base):
    __tablename__ = 'regulation_type_lut'
    regulation_type_id = Column(UUID, primary_key=True, server_default='uuid_generate_v4()')
    regulation_type_code = Column(String)
    regulation_type_description = Column(String)

    rules = relationship('Rules', back_populates='regulation')

class SpeciesLUT(Base):
    __tablename__ = 'species_lut'
    species_id = Column(UUID, primary_key=True, server_default='uuid_generate_v4()')
    common_name = Column(String)
    rules = relationship('Rules', back_populates = 'species')