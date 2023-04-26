from pydantic import BaseModel
from pydantic_geojson import FeatureModel
from uuid import UUID
import datetime


class GeoBase(BaseModel):
    catch_area_id: UUID
    description: str
    geom: FeatureModel

class Geo(GeoBase):
    pass #wtf is going on here?
    class Config:
        orm_mode = True

class CatchArea(BaseModel):
    catch_area_id: UUID
    description: str

class RulesBase(BaseModel):
    rules_id: UUID | None = None
    catch_area_id: UUID

class Rules(RulesBase):
    description: str
    common_name: str
    regulation_type_code: str
    start_rule_datetime: datetime.datetime
    end_rule_datetime: datetime.datetime

    class Config:
        orm_mode = True

class RegulationType(BaseModel):
    regulation_type_id: UUID
    regulation_type_code: str
    regulation_type_description: str

    class Config:
        orm_mode = True

class Species(BaseModel):
    species_id: UUID
    common_name: str

class CreateRule(RulesBase):
    regulation_type_id: UUID
    start_rule_datetime: datetime.datetime
    end_rule_datetime: datetime.datetime
    species_id: UUID


# class CatchAreaAlt(BaseModel):
#     catch_area_id: UUID
#     description: str
#     rules: list[Rules] = []
#     class Config:
#         orm_mode = True


    
