from fastapi import Depends, FastAPI, HTTPException, UploadFile, Form
from sqlalchemy.orm import Session
from uuid import UUID
from sql import crud, models, schemas
from sql.database import SessionLocal, engine
from fastapi.middleware.cors import CORSMiddleware
import json


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


origins = [

    "*",

]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def get_catch_areas(db: Session = Depends(get_db)):
    catch_areas = crud.get_catch_areas(db)
    return catch_areas

@app.get('/reg')
async def get_reg(db: Session = Depends(get_db)):
    regs = crud.get_regs(db)
    return regs

@app.get('/lut/{lut}')
async def lut(lut: str, db: Session = Depends(get_db)):
    lut = crud.lut(db, lut)
    return lut

# @app.get("/geo/{catch_area_id}")
# async def read_geojson_only_by_area(catch_area_id: UUID, db: Session = Depends(get_db)):
#     geo = crud.get_geo(db, catch_area_id)
#     return geo

# @app.post("/geo/")
# async def upload_geojson(file: UploadFile, description: str = Form(), db: Session = Depends(get_db)):
#     try:
#         contents = await file.read()
#         geoJSON = json.loads(contents)
#         insert = {
#             'description': description, 
#             'geom': geoJSON
#             }
#         geom = crud.create_geo(db, geo = insert)
#         return geom
#     except:
#         raise HTTPException(500, 'Bad Content')


# @app.get("/api/catchareas/", response_model=list[schemas.CatchArea])
# async def read_users(db: Session = Depends(get_db)):
#     geo = crud.get_geo_all_areas(db)
#     return geo

# @app.get("/api/rules/{catch_area_id}")
# async def read_rules(catch_area_id: UUID, db: Session = Depends(get_db)):
#     rules = crud.get_rules(db, catch_area_id)
#     return rules

# @app.get('/api/regulationtypes/', response_model=list[schemas.RegulationType])
# async def read_regtypes(db: Session = Depends(get_db)):
#     regulation_types = crud.get_regulation_types(db)
#     return regulation_types

# @app.get('/api/species/', response_model=list[schemas.Species])
# async def read_species(db: Session = Depends(get_db)):
#     species = crud.get_species(db)
#     return species

# @app.post("/api/rules/")
# async def create_rule(rule: schemas.CreateRule, db: Session = Depends(get_db)):
#     rules = crud.create_rule(db, rule)
#     return rules