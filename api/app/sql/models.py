from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, backref

from .database import Base

##################
# Look-up Tables #
##################

# use 'uselist=True' for 1-1 relationships

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
    children_catch_areas = relationship('CatchAreaLUT', backref=backref("parent", remote_side=[catch_area_id]))
    fishery = relationship('Fishery', back_populates = 'catch_area')

class SpeciesLUT(Base):
    __tablename__ = 'species_lut'
    species_id = Column(UUID, primary_key=True, server_default='uuid_generate_v4()')
    species_name = Column(String)
    created_by = Column(String, nullable=False)
    created_datetime = Column(Date, nullable=False)
    modified_by = Column(String)
    modified_datetime = Column(Date)
    species_group = relationship('SpeciesGroup', back_populates = 'species')

class SpeciesGroupTypeLUT(Base):
    __tablename__ = 'species_group_type_lut'
    species_group_type_id = Column(UUID, primary_key=True, server_default='uuid_generate_v4()')
    species_group_type_description = Column(String)
    created_by = Column(String, nullable=False)
    created_datetime = Column(Date, nullable=False)
    modified_by = Column(String)
    modified_datetime = Column(Date)
    bag_limit = relationship('BagLimit', back_populates='species_group_type')
    species_group = relationship('SpeciesGroup', back_populates = 'species_group_type')

class RegulationTypeLUT(Base):
    __tablename__ = 'regulation_type_lut'
    regulation_type_id = Column(UUID, primary_key=True, server_default='uuid_generate_v4()')
    regulation_type_code = Column(String, nullable=False)
    regulation_type_description = Column(String, nullable=False)
    created_by = Column(String, nullable=False)
    created_datetime = Column(Date, nullable=False)
    modified_by = Column(String)
    modified_datetime = Column(Date)
    bag_limit = relationship('BagLimit', back_populates = 'regulation_type')

class RegulationAgeLUT(Base):
    __tablename__ = 'regulation_age_lut'
    regulation_age_id = Column(UUID, primary_key=True, server_default='uuid_generate_v4()')
    regulation_age_description = Column(String, nullable=False)
    created_by = Column(String, nullable=False)
    created_datetime = Column(Date, nullable=False)
    modified_by = Column(String)
    modified_datetime = Column(Date)
    bag_limit = relationship('BagLimit', back_populates='regulation_age')

class RegulationAuthorityLUT(Base):
    __tablename__ = 'regulation_authority_lut'
    regulation_authority_id = Column(UUID, primary_key=True, server_default='uuid_generate_v4()')
    regulation_authority_code = Column(String, nullable=False)
    regulation_authority_name = Column(String, nullable=False)  
    created_by = Column(String, nullable=False)
    created_datetime = Column(Date, nullable=False)
    modified_by = Column(String)
    modified_datetime = Column(Date)
    fishery = relationship('Fishery', back_populates='regulation_authority')

class FisheryTypeLUT(Base):
    __tablename__ = 'fishery_type_lut'
    fishery_type_id = Column(UUID, primary_key=True, server_default='uuid_generate_v4()')
    fishery_type_code = Column(String, nullable=False)
    fishery_type_description = Column(String, nullable=False)  
    created_by = Column(String, nullable=False)
    created_datetime = Column(Date, nullable=False)
    modified_by = Column(String)
    modified_datetime = Column(Date)
    fishery = relationship('Fishery', back_populates = 'fishery_type')

class FisheryRegulationTypeLUT(Base):
    __tablename__ = 'fishery_regulation_type_lut'
    fishery_regulation_type_id = Column(UUID, primary_key=True, server_default='uuid_generate_v4()')
    fishery_regulation_type_code = Column(String, nullable=False)
    fishery_regulation_type_description = Column(String, nullable=False)  
    created_by = Column(String, nullable=False)
    created_datetime = Column(Date, nullable=False)
    modified_by = Column(String)
    modified_datetime = Column(Date)
    fishery_regulation = relationship('FisheryRegulation', back_populates='fishery_regulation_type')

class GearTypeLUT(Base):
    __tablename__ = 'gear_type_lut'
    gear_type_id = Column(UUID, primary_key=True, server_default='uuid_generate_v4()')
    gear_type_code = Column(String, nullable=False)
    gear_type_description = Column(String, nullable=False)  
    created_by = Column(String, nullable=False)
    created_datetime = Column(Date, nullable=False)
    modified_by = Column(String)
    modified_datetime = Column(Date)
    fishery_regulation = relationship('FisheryRegulation', back_populates='gear_type')

# how useful is the management year? think about removing it
class FisheryManagementYearLUT(Base):
    __tablename__ = 'fishery_management_year_lut'
    fishery_management_year_id = Column(UUID, primary_key=True, server_default='uuid_generate_v4()')
    fishery_management_year = Column(String, nullable=False)
    created_by = Column(String, nullable=False)
    created_datetime = Column(Date, nullable=False)
    modified_by = Column(String)
    modified_datetime = Column(Date)
    fishery = relationship('Fishery', back_populates='management_year')

class BagLimitTypeLUT(Base):
    __tablename__ = 'bag_limit_type_lut'
    bag_limit_type_id = Column(UUID, primary_key=True, server_default='uuid_generate_v4()')
    bag_limit_type_description = Column(String, nullable=False)
    created_by = Column(String, nullable=False)
    created_datetime = Column(Date, nullable=False)
    modified_by = Column(String)
    modified_datetime = Column(Date)
    bag_limit = relationship('BagLimit', back_populates='bag_limit_type')

class BagLimitResidentStatusLUT(Base):
    __tablename__ = 'bag_limit_angler_resident_status_lut'
    bag_limit_angler_resident_status_id = Column(UUID, primary_key=True, server_default='uuid_generate_v4()')
    bag_limit_angler_resident_status_description = Column(String, nullable=False)
    created_by = Column(String, nullable=False)
    created_datetime = Column(Date, nullable=False)
    modified_by = Column(String)
    modified_datetime = Column(Date)
    bag_limit = relationship('BagLimit', back_populates='resident_status')

##################
# Working tables #
##################

class Fishery(Base):
    __tablename__ = 'fishery'
    fishery_id = Column(UUID, primary_key=True, server_default='uuid_generate_v4()')
    fishery_type_id = Column(UUID, ForeignKey('fishery_type_lut.fishery_type_id'), nullable=False)
    fishery_management_year_id = Column(UUID, ForeignKey('fishery_management_year_lut.fishery_management_year_id'), nullable=False)
    catch_area_id = Column(UUID, ForeignKey('catch_area_lut.catch_area_id'), nullable=False)
    fishery_description = Column(String, nullable=False)
    regulation_authority_id = Column(UUID, ForeignKey('regulation_authority_lut.regulation_authority_id'))
    created_by = Column(String, nullable=False)
    created_datetime = Column(Date, nullable=False)
    modified_by = Column(String)
    modified_datetime = Column(Date)
    fishery_type = relationship('FisheryTypeLUT', back_populates='fishery', uselist=False)
    fishery_regulation = relationship('FisheryRegulation', back_populates='fishery')
    catch_area = relationship('CatchAreaLUT', back_populates='fishery', uselist=False)
    management_year = relationship('FisheryManagementYearLUT', back_populates = 'fishery', uselist=False)
    regulation_authority = relationship('RegulationAuthorityLUT', back_populates = 'fishery', uselist=False)
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
    gear_type = relationship('GearTypeLUT', back_populates='fishery_regulation', uselist=False)
    fishery_regulation_type = relationship('FisheryRegulationTypeLUT', back_populates='fishery_regulation', uselist=False)
    bag_limit = relationship('BagLimit', back_populates = 'fishery_regulation')

class BagLimit(Base):
    __tablename__ = 'bag_limit'
    bag_limit_id = Column(UUID, primary_key=True, server_default='uuid_generate_v4()')
    parent_bag_limit_id = Column(UUID, ForeignKey('bag_limit.bag_limit_id'))
    fishery_regulation_id = Column(UUID, ForeignKey('fishery_regulation.fishery_regulation_id'), nullable=False)
    regulation_age_id = Column(UUID, ForeignKey('regulation_age_lut.regulation_age_id'), nullable=False)
    regulation_type_id = Column(UUID, ForeignKey('regulation_type_lut.regulation_type_id'), nullable=False)
    bag_limit_type_id = Column(UUID, ForeignKey('bag_limit_type_lut.bag_limit_type_id'), nullable=False)
    maximum_size_limit_centimeters = Column(Float)
    minimum_size_limit_centimeters = Column(Float)
    bag_limit_total = Column(Integer, nullable=False)
    species_group_type_id = Column(UUID, ForeignKey('species_group_type_lut.species_group_type_id'), nullable=False)
    bag_limit_angler_resident_status_id = Column(UUID, ForeignKey('bag_limit_angler_resident_status_lut.bag_limit_angler_resident_status_id'))
    created_by = Column(String, nullable=False)
    created_datetime = Column(Date, nullable=False)
    modified_by = Column(String)
    modified_datetime = Column(Date)
    bag_limit_type = relationship('BagLimitTypeLUT', back_populates='bag_limit', uselist=False)
    resident_status = relationship('BagLimitResidentStatusLUT', back_populates='bag_limit', uselist=False)
    fishery_regulation = relationship('FisheryRegulation', back_populates='bag_limit', uselist=False)
    regulation_age = relationship('RegulationAgeLUT', back_populates='bag_limit', uselist=False)
    regulation_type = relationship('RegulationTypeLUT', back_populates='bag_limit', uselist=False)
    species_group_type = relationship('SpeciesGroupTypeLUT', back_populates='bag_limit', uselist=False)
    childen_bag_limits = relationship('BagLimit', backref=backref("parent", remote_side=[bag_limit_id]))

class SpeciesGroup(Base):
    __tablename__ = 'species_group'
    species_group_id = Column(UUID, primary_key=True, server_default='uuid_generate_v4()')
    species_id = Column(UUID, ForeignKey('species_lut.species_id'))
    species_group_type_id = Column(UUID, ForeignKey('species_group_type_lut.species_group_type_id'), nullable=False) # probably a better way to handle species
    species = relationship('SpeciesLUT', back_populates='species_group')
    species_group_type = relationship('SpeciesGroupTypeLUT', back_populates = 'species_group')