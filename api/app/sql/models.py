from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, backref

from .database import Base

##################
# Look-up Tables #
##################

class CatchAreaLUT(Base):
    __tablename__ = 'catch_area_lut'
    catch_area_id = Column(UUID, primary_key=True, server_default='uuid_generate_v4()')
    parent_catch_area_id = Column(UUID, ForeignKey('catch_area_lut.catch_area_id'))
    catch_area_code = Column(String)
    catch_area_description = Column(String, nullable=False)
    shape = Column(String)
    created_by = Column(String, nullable=False)
    created_datetime = Column(Date, nullable=False)
    modified_by = Column(String)
    modified_datetime = Column(Date)
    childen_catch_areas = relationship('CatchAreaLUT', backref=backref("parent", remote_side=[catch_area_id]))

class SpeciesLUT(Base):
    __tablename__ = 'species_lut'
    species_id = Column(UUID, primary_key=True, server_default='uuid_generate_v4()')
    species_name = Column(String)
    created_by = Column(String, nullable=False)
    created_datetime = Column(Date, nullable=False)
    modified_by = Column(String)
    modified_datetime = Column(Date)

class RegulationTypeLUT(Base):
    __tablename__ = 'regulation_type_lut'
    regulation_type_id = Column(UUID, primary_key=True, server_default='uuid_generate_v4()')
    regulation_type_code = Column(String, nullable=False)
    regulation_type_description = Column(String, nullable=False)
    created_by = Column(String, nullable=False)
    created_datetime = Column(Date, nullable=False)
    modified_by = Column(String)
    modified_datetime = Column(Date)

class RegulationAgeLUT(Base):
    __tablename__ = 'regulation_age_lut'
    regulation_age_id = Column(UUID, primary_key=True, server_default='uuid_generate_v4()')
    regulation_age_description = Column(String, nullable=False)
    created_by = Column(String, nullable=False)
    created_datetime = Column(Date, nullable=False)
    modified_by = Column(String)
    modified_datetime = Column(Date)

class RegulationAuhtorityLUT(Base):
    __tablename__ = 'regulation_authority_lut'
    regulation_authority_id = Column(UUID, primary_key=True, server_default='uuid_generate_v4()')
    regulation_authority_code = Column(String, nullable=False)
    regulation_authority_name = Column(String, nullable=False)  
    created_by = Column(String, nullable=False)
    created_datetime = Column(Date, nullable=False)
    modified_by = Column(String)
    modified_datetime = Column(Date)

class FisheryTypeLUT(Base):
    __tablename__ = 'fishery_type_lut'
    fishery_type_id = Column(UUID, primary_key=True, server_default='uuid_generate_v4()')
    fishery_type_code = Column(String, nullable=False)
    fishery_type_decription = Column(String, nullable=False)  
    created_by = Column(String, nullable=False)
    created_datetime = Column(Date, nullable=False)
    modified_by = Column(String)
    modified_datetime = Column(Date)

class FisheryRegulationTypeLUT(Base):
    __tablename__ = 'fishery_regulation_type_lut'
    fishery_regulation_type_id = Column(UUID, primary_key=True, server_default='uuid_generate_v4()')
    fishery_regulation_type_code = Column(String, nullable=False)
    fishery_regulation_type_description = Column(String, nullable=False)  
    created_by = Column(String, nullable=False)
    created_datetime = Column(Date, nullable=False)
    modified_by = Column(String)
    modified_datetime = Column(Date)

class GearTypeLUT(Base):
    __tablename__ = 'gear_type_lut'
    gear_type_id = Column(UUID, primary_key=True, server_default='uuid_generate_v4()')
    gear_type_code = Column(String, nullable=False)
    gear_type_description = Column(String, nullable=False)  
    created_by = Column(String, nullable=False)
    created_datetime = Column(Date, nullable=False)
    modified_by = Column(String)
    modified_datetime = Column(Date)

# how useful is the management year? think about removing it
class FisheryManagementYearLUT(Base):
    __tablename__ = 'fishery_management_year_lut'
    fishery_management_year_id = Column(UUID, primary_key=True, server_default='uuid_generate_v4()')
    fishery_management_year = Column(String, nullable=False)
    created_by = Column(String, nullable=False)
    created_datetime = Column(Date, nullable=False)
    modified_by = Column(String)
    modified_datetime = Column(Date)

##################
# Working tables #
##################

class Fishery(Base):
    __tablename__ = 'fishery'
    fishery_id = Column(UUID, primary_key=True, server_default='uuid_generate_v4()')
    fishery_type_id = Column(UUID, ForeignKey('fishery_type_lut.fishery_type_id'), nullable=False)
    fishery_management_year_id = Column(UUID, ForeignKey('fishery_type_lut.fishery_type_id'), nullable=False)
    catch_area_id = Column(UUID, ForeignKey('catch_area_lut.catch_area_id'), nullable=False)
    fishery_description = Column(String, nullable=False)
    regulation_authority_id = Column(UUID, ForeignKey('regulation_authority_lut.regulation_authority_id'))
    created_by = Column(String, nullable=False)
    created_datetime = Column(Date, nullable=False)
    modified_by = Column(String)
    modified_datetime = Column(Date)
    fishery_regulation = relationship('FisheryRegulation', back_populates='fishery')
    # relationships

class FisheryRegulation(Base):
    __tablename__ = 'fishery_regulation'
    fishery_regulation_id = Column(UUID, primary_key=True, server_default='uuid_generate_v4()')
    fishery_id = Column(UUID, ForeignKey('fishery.fishery_id'))
    fishery_regulation_type_id = Column(UUID, ForeignKey('fishery_regulation_type_lut.fishery_regulation_type_id'))
    start_datetime = Column(Date)
    end_datetime = Column(Date)
    gear_type_id = Column(UUID, ForeignKey('gear_type_lut.gear_type_id'))
    created_by = Column(String, nullable=False)
    created_datetime = Column(Date, nullable=False)
    modified_by = Column(String)
    modified_datetime = Column(Date)
    fishery = relationship('Fishery', back_populates='fishery_regulation')


# class Rules(Base):
#     __tablename__ = "rules"
#     rules_id = Column(UUID, primary_key=True, server_default='uuid_generate_v4()')
#     catch_area_id = Column(UUID, ForeignKey('catch_area.catch_area_id'))
#     start_rule_datetime = Column(Date)
#     end_rule_datetime = Column(Date)
#     species_id = Column(UUID, ForeignKey('species_lut.species_id'))
#     regulation_type_id = Column(UUID, ForeignKey('regulation_type_lut.regulation_type_id'))
#     catch_area = relationship("CatchAreaRaw", back_populates="rules", uselist=False)
#     regulation = relationship("RegulationTypeLUT", back_populates="rules", uselist=False)
#     species = relationship("SpeciesLUT", back_populates="rules", uselist=False)


# class CatchAreaRaw(Base):
#     __tablename__ = "catch_area"
#     catch_area_id = Column(UUID, primary_key=True, server_default='uuid_generate_v4()')
#     description = Column(String)
#     geom = Column(String)
#     rules = relationship("Rules", back_populates="catch_area")

# class CatchArea(Base):
#     __tablename__ = "catch_area_geojson"
#     catch_area_id = Column(String, primary_key=True)
#     description = Column(String)
#     geom = Column(String)


# class RegulationTypeLUT(Base):
#     __tablename__ = 'regulation_type_lut'
#     regulation_type_id = Column(UUID, primary_key=True, server_default='uuid_generate_v4()')
#     regulation_type_code = Column(String)
#     regulation_type_description = Column(String)

#     rules = relationship('Rules', back_populates='regulation')

# class SpeciesLUT(Base):
#     __tablename__ = 'species_lut'
#     species_id = Column(UUID, primary_key=True, server_default='uuid_generate_v4()')
#     common_name = Column(String)
#     rules = relationship('Rules', back_populates = 'species')