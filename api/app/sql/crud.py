from sqlalchemy.orm import Session, selectinload, subqueryload, joinedload, contains_eager, aliased
from sqlalchemy import func, select
from uuid import UUID
from sqlalchemy.dialects import postgresql
from zoneinfo import ZoneInfo
from . import models, schemas
from fastapi import HTTPException


def get_bags(db: Session, bag_limit_id: str):
    return db.query(models.Fishery).all()
    #return db.query(models.BagLimit).filter(models.BagLimit.parent_bag_limit_id == None).filter(models.BagLimit.bag_limit_id == 'b1549260-ef72-4126-bd9d-f677015ea52a').all()


def get_catch_areas(db: Session):
        top = db.query(models.CatchAreaLUT)\
            .filter(models.CatchAreaLUT.parent_catch_area_id == None).all()
        return top


def lut(db: Session, requested_table: str):
    # allowed tables, only look up tables should be hitting this
    allowed_tables = {
        'catch_area' : models.CatchAreaLUT,
        'regulation_type': models.RegulationTypeLUT,
        'regulation_age': models.RegulationAgeLUT,
        'regulation_autority': models.RegulationAuthorityLUT,
        'bag_limit_type': models.BagLimitTypeLUT,
        'resident_status': models.BagLimitResidentStatusLUT,
        'gear_type': models.GearTypeLUT,
        'management_year': models.FisheryManagementYearLUT,
        'fishery_regulation_type': models.FisheryRegulationTypeLUT,
        'fishery_type': models.FisheryTypeLUT,
        'species': models.SpeciesLUT,
        'species_group_type': models.SpeciesGroupTypeLUT
    }
    # check if requested table is available, if not throw a  404
    if requested_table not in allowed_tables:
        raise HTTPException(status_code = 404, detail='Table not found')
    else:
        return db.query(allowed_tables[requested_table]).all()



def get_regs(db: Session):
    return db.query(models.Fishery, 
                    models.CatchAreaLUT.catch_area_id, \
                    models.CatchAreaLUT.catch_area_description,
                    models.FisheryTypeLUT.fishery_type_description) \
                    .join(models.CatchAreaLUT) \
                    .join(models.FisheryTypeLUT)\
                    .options(
                        selectinload(
                            models.Fishery.fishery_regulation
                            )\
                            .selectinload(models.FisheryRegulation.gear_type)
                            ) \
                    .all()
# def get_geo(db: Session, catch_area_id: UUID):
#     return db.query(models.CatchArea).filter(models.CatchArea.catch_area_id == catch_area_id).first()


# def get_geo_all(db: Session):
#     return db.query(models.CatchArea).all()

# def get_geo_all_areas(db: Session):
#     return db.query(models.CatchArea.description, models.CatchArea.catch_area_id).all()

# def create_geo(db: Session, geo: schemas.Geo):
#     geometry = geo['geom']['features'][0]['geometry']
#     crs = geo['geom']['crs']
#     psql_insert = str(geometry) + ', \"crs\": ' + str(crs)
#     db_geom = models.CatchAreaRaw(description=geo['description'], geom=func.ST_GeomFromGeoJSON(psql_insert))
#     db.add(db_geom)
#     db.commit()
#     db.refresh(db_geom)
#     return db_geom

# def get_rules(db: Session, catch_area_id: UUID):
#     return db.query(models.Rules.catch_area_id,\
#                     models.Rules.rules_id,\
#                     models.CatchAreaRaw.description,
#                     models.SpeciesLUT.common_name,
#                     models.RegulationTypeLUT.regulation_type_code,
#                     models.Rules.start_rule_datetime,
#                     models.Rules.end_rule_datetime)\
#                         .filter(models.Rules.catch_area_id == str(catch_area_id))\
#                         .join(models.SpeciesLUT)\
#                         .join(models.RegulationTypeLUT)\
#                         .join(models.CatchAreaRaw)\
#                         .all()

# def get_regulation_types(db: Session):
#     return db.query(models.RegulationTypeLUT.regulation_type_id,\
#                     models.RegulationTypeLUT.regulation_type_code,\
#                     models.RegulationTypeLUT.regulation_type_description).all()

# def get_species(db: Session):
#     return db.query(models.SpeciesLUT.species_id,\
#                     models.SpeciesLUT.common_name).all()

# def create_rule(db: Session, rule: schemas.CreateRule):
#     db_rule = models.Rules(catch_area_id = str(rule.catch_area_id), 
#                            regulation_type_id=str(rule.regulation_type_id),
#                            start_rule_datetime=rule.start_rule_datetime.astimezone(ZoneInfo('America/Los_Angeles')),
#                            end_rule_datetime=rule.end_rule_datetime.astimezone(ZoneInfo('America/Los_Angeles')),
#                            species_id = str(rule.species_id)
#                            )
#     db.add(db_rule)
#     db.commit()
#     db.refresh(db_rule)
#     return db_rule
