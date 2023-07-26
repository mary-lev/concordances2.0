from typing import List, Dict
import pandas as pd
from fastapi import FastAPI, Depends, HTTPException, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import crud, models, schemas
from database import SessionLocal, engine
from utils import get_date
from create_tei import create_TEI


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

origins = [
    "http://localhost:3000",  # React app address
    "http://localhost:8000",  # FastAPI server address
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/authors/", response_model=schemas.AuthorBase, tags=["authors"])
def create_author(author: schemas.AuthorBase, db: Session = Depends(get_db)):
    return crud.create_author(db=db, author=author)

@app.get("/authors/", response_model=List[schemas.AuthorInDBBase], tags=["authors"])
def read_authors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    authors = crud.get_authors(db, skip=skip, limit=limit)
    return authors

@app.post("/upload_publications/", tags=["publications"])
async def upload_publication_from_csv(file: UploadFile = File(...), db: Session = Depends(get_db)):
    df = pd.read_csv(file.file)
    df = df.fillna('')
    for _, row in df.iterrows():
        publication_data = {
            'id': row['biblio.id'],
            'title': row['biblio.title'],
            'author_id': int(row['biblio.author']) if pd.notna(row['biblio.author']) and row['biblio.author'] != '' else None,
            'city': row['biblio.city'],
            'editor': '',
            'publisher': row['biblio.editor'],
            'year': str(int(row['biblio.year'])) if pd.notna(row['biblio.year']) and row['biblio.year'] != '' else '',
            'part': row['biblio.part'],
            'short': row['biblio.short'],
        }
        publication = schemas.PublicationBase(**publication_data)
        crud.create_publication(db=db, publication=publication)
    return {"message": "Publications created"}

@app.get("/publication/{publication_id}", response_model=schemas.PublicationInDBBase, tags=["publications"])
def read_publication(publication_id: int, db: Session = Depends(get_db)):
    db_publication = crud.get_publication(db, publication_id=publication_id)
    if db_publication is None:
        raise HTTPException(status_code=404, detail="Publication not found")
    return db_publication

@app.get("/publications/", response_model=List[schemas.PublicationInDBBase], tags=["publications"])
async def read_publications(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    publications = crud.get_publications(db, skip=skip, limit=limit)
    return publications

@app.get("/publications/count/{author_id}", response_model=int, tags=["publications"])
async def count_publications(author_id: int, db: Session = Depends(get_db)):
    return crud.count_publications_by_author(db, author_id=author_id)

@app.post("/upload_authors/", tags=["authors"])
async def upload_authors_from_csv(file: UploadFile = File(...), db: Session = Depends(get_db)):
    df = pd.read_csv(file.file)
    df = df.fillna('')
    for _, row in df.iterrows():
        author_data = {
            'id': row['author.id'],
            'name': row['author.name'],
            'surname': row['author.surname'],
            'family': row['author.family'],
            'real_name': row['author.real_name'],
            'year_birth': str(int(row['author.year_birth'])) if pd.notna(row['author.year_birth']) and row['author.year_birth'] != '' else '',
            'year_death': str(int(row['author.year_death'])) if pd.notna(row['author.year_death']) and row['author.year_death'] != '' else '',
            'gender': row['author.gender'],
            'birth_location': row['author.birth_location'],
            'death_location': row['author.death_location']
        }
        author = schemas.AuthorBase(**author_data)
        crud.create_author(db=db, author=author)
    return {"filename": file.filename}

@app.post("/upload_group_texts/", tags=["group_texts"])
async def upload_group_texts(file: UploadFile = File(...), db: Session = Depends(get_db)):
    df = pd.read_csv(file.file)
    df = df.fillna('')
    for _, row in df.iterrows():
        author_id = int(row['group_text.author'])
        date_id = get_date(row, db, "group_text")
        group_data = {
            "id": row['group_text.id'],
            "title": row['group_text.title'],
            "author_id": author_id,
            "dedication": row['group_text.dedication'],
            #"supergroup": int(row['group_text.superpgroup']) if pd.notna(row['group_text.superpgroup']) and row['group_text.superpgroup'] != '' else None,
            "subtitle": "",
            "author_comment": "",
            "text_date_id": date_id,
            "location_id": None,
        }
        
        group = schemas.GroupTextCreate(**group_data)
        print(group)
        group_instance = crud.create_grouptext(db=db, grouptext=group)
        if 'group_text.epigraph' in row and pd.notna(row['group_text.epigraph']) and row['group_text.epigraph'] != '':
            epi = {
                "epi_text": row['group_text.epigraph'],
                "text_id": group_instance.id,
            }
            epi_data = schemas.EpigraphCreate(**epi)
            crud.create_epigraph(db=db, epigraph=epi_data)

    return {"filename": file.filename}

@app.post("/upload_epigraphs/", tags=["epigraphs"])
async def upload_epigraphs(file: UploadFile = File(...), db: Session = Depends(get_db)):
    df = pd.read_csv(file.file)
    df = df.fillna('')
    df.replace('<NULL>', '', inplace=True)
    for _, row in df.iterrows():
        text_id = int(row['epi.text'])
        # find textbase id
        textbase_id = crud.get_new_text_id_by_old_id(db=db, old_id=text_id)
        source_textbase_id = None
        if row["epi.epi_text_id"]:
            text_id = int(row['epi.epi_text_id'])
            source_textbase_id = crud.get_new_text_id_by_old_id(db=db, old_id=text_id)
        epi = {
            "id": row['epi.id'],
            "epi_text": row['epi.epi_text'],
            "epi_author": row['epi.epi_author'],
            "epi_author_id": int(row['epi.epi_author_id']) if pd.notna(row['epi.epi_author_id']) and row['epi.epi_author_id'] != '' else None,
            "epi_book": row['epi.epi_book'],
            "epi_book_id": source_textbase_id,
            "epi_filename": row['epi.epi_filename'],
            "textbase_id": textbase_id,
        }
        epi_data = schemas.EpigraphCreate(**epi)
        crud.create_epigraph(db=db, epigraph=epi_data)
    return {"filename": file.filename}

@app.post("/upload_old/", tags=["old"])
async def upload_old(file: UploadFile = File(...), db: Session = Depends(get_db)):
    df = pd.read_csv(file.file)
    df = df.fillna('')
    df.replace('<NULL>', '', inplace=True)
    for _, row in df.iterrows():
        author_id = int(row['old.author'])
        text_id = int(row['old.text'])
        # find textbase id
        text = crud.get_text(db=db, id=text_id)
        old_data = {
            "title": row['old.title'],
            #"old_variant_of_text": textbase,
            "old_variant_of_text_id": text_id,
            "first_string": row['old.first_string'],
            "filename": row['old.filename'],
            "dedication": row['old.dedication'],
            "date": int(row['old.year']) if pd.notna(row['old.year']) and row['old.year'] != '' else None,
            "author_id": author_id,
        }
        old = models.Old(**old_data)
        print(old)
        db.add(old)
    db.commit()
    return {"filename": file.filename}

@app.post("/upload_variants/", tags=["variants"])
async def upload_variants(file: UploadFile = File(...), db: Session = Depends(get_db)):
    df = pd.read_csv(file.file)
    df = df.fillna('')
    df.replace('<NULL>', '', inplace=True)
    for _, row in df.iterrows():
        variant_data = {
            "filename": row["drafts.filename"],
            "author_id": row["drafts.author"],
            "title": row["drafts.title"],
            "dedication": row.get("drafts.dedication"),
            "year": row.get("drafts.year"),
            "date": row.get("drafts.date"),
            "publication_id": int(row.get("drafts.book")),
            "book_page_start": row.get("drafts.book_page"),
            "variant_of_text_id": int(row["drafts.text"]),
            "epi_text": row.get("drafts.epi"),
            "epi_author": row.get("drafts.epi_author"),
        }
        variant = models.Variant(**variant_data)
        db.add(variant)
    db.commit()

    return {"filename": file.filename}

@app.post("/text/create/", tags=["texts"])
async def create_text(text: schemas.TextCreate, db: Session = Depends(get_db)):
    return crud.create_text(db=db, text=text)

@app.post("/upload_texts/", tags=["texts"])
async def upload_texts(file: UploadFile = File(...), db: Session = Depends(get_db)):
    df = pd.read_csv(file.file)
    df = df.fillna('')
    df.replace('<NULL>', '', inplace=True)
    for _, row in df.iterrows():
        author_id = int(row['text1.author'])
        date_id = get_date(row, db, "text1")
        text_data = {
            "text_id": row['text1.id'],
            "title": row['text1.title'],
            "first_string": row['text1.first_string'],
            "body": row['text1.body'],
            "filename": row['text1.filename'],
            "source": row['text1.book'],
            "author_id": author_id,
            "dedication": row['text1.dedication'],
            "subtitle": row["text1.under_title"],
            "author_comment": row["text1.v"],
            "text_date_id": date_id,
            "location_id": None,
            "publication_id": None,
            "book_page_start": "",
            "book_page_end": "",
            "n_in_group": int(row['text1.n_in_group']) if pd.notna(row['text1.n_in_group']) and row['text1.n_in_group'] != '' else 0,
            "group_text_id": int(row['text1.group_text']) if pd.notna(row['text1.group_text']) and row['text1.group_text'] != '' else None,
        }
       
        text = schemas.TextCreate(**text_data)
        text_instance = crud.create_text(db=db, text=text)
        if "text1.group_text" in row and pd.notna(row['text1.group_text']) and row['text1.group_text'] != '':
            group_text = crud.get_grouptext(db, grouptext_id=int(row['text1.group_text']))
            text_instance.group_text_id = group_text.id
            text_instance.group_text = group_text
            db.flush()
        
        author = crud.get_author(db, author_id=author_id)
        if author:
            text_instance.author_id = author_id
            text_instance.author = author
            db.flush()
        if date_id:
            text_instance.text_date_id = date_id
            text_instance.text_date = crud.get_date(db, date_id=date_id)
            db.flush()

        if 'text1.writing_location' in row and pd.notna(row['text1.writing_location']) and row['text1.writing_location'] != '':
            new_location = row['text1.writing_location'].strip()
            location = crud.get_location_by_name(db, name=new_location)
            if location is None:
                loc = {
                    "name": new_location,
                }
                loc_data = schemas.LocationCreate(**loc)
                location = crud.create_location(db=db, location=loc_data)
            if location:
                text_instance.location_id = location.id
                db.flush()
        db.commit()
    return {"filename": file.filename}

@app.get("/authors/{author_id}", response_model=schemas.AuthorInDBBase, tags=["authors"])
def read_author(author_id: int, db: Session = Depends(get_db)):
    db_author = crud.get_author(db, author_id=author_id)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return db_author

@app.post("/grouptexts/", response_model=schemas.GroupTextCreate, tags=["grouptexts"])
def create_grouptext(grouptext: schemas.GroupTextBase, db: Session = Depends(get_db)):
    return crud.create_grouptext(db=db, grouptext=grouptext)

@app.get("/all_grouptexts/", response_model=List[schemas.GroupTextBase], tags=["grouptexts"])
def read_all_grouptexts(db: Session = Depends(get_db)):
    db_grouptexts = crud.get_grouptexts(db)
    if db_grouptexts is None:
        raise HTTPException(status_code=404, detail="GroupText not found")
    return db_grouptexts

@app.get("/grouptexts/{grouptext_id}", response_model=schemas.GroupTextBase, tags=["grouptexts"])
def read_grouptext(grouptext_id: int, db: Session = Depends(get_db)):
    db_grouptext = crud.get_grouptext(db, grouptext_id=grouptext_id)
    if db_grouptext is None:
        raise HTTPException(status_code=404, detail="GroupText not found")
    return db_grouptext

@app.get("/texts/{id}", response_model=schemas.TextBase, tags=["texts"])
def read_text(id: int, db: Session = Depends(get_db)):
    db_text = crud.get_text(db, id=id)
    if db_text is None:
        raise HTTPException(status_code=404, detail="Text not found")
    return db_text

@app.get("/texts/author/", response_model=List[schemas.TextInDBBase], tags=["texts"])
def read_texts_by_author(author_id: int, db: Session = Depends(get_db)):
    db_texts = crud.get_texts_by_author(db, author_id=author_id)
    if db_texts is None:
        raise HTTPException(status_code=404, detail="Text not found")
    return db_texts

@app.get("/texts/author/with_group/", response_model=List[schemas.TextInDBBase], tags=["texts"])
def read_texts_by_author_with_group(author_id: int,db: Session = Depends(get_db)):
    db_texts = crud.get_texts_by_author_with_group(db, author_id=author_id)
    if db_texts is None:
        raise HTTPException(status_code=404, detail="Text not found")
    return db_texts

@app.post("/old/", response_model=schemas.OldInDBBase, tags=["old"])
async def create_old(old: schemas.OldCreate, db: Session = Depends(get_db)):
    db_old = crud.create_old(db=db, filename=old.filename, old_variant_of_text_id=old.old_variant_of_text_id)
    if db_old:
        raise HTTPException(status_code=400, detail="Old already registered")
    return crud.create_old(db=db, old=old)

@app.get("/old/{id}", response_model=schemas.OldInDBBase, tags=["old"])
def read_old(id, db: Session = Depends(get_db)):
    db_old = crud.get_old(db, id=id)
    if db_old is None:
        raise HTTPException(status_code=404, detail="Old not found")
    return db_old


@app.get("/old/text/{text_id}", response_model=schemas.OldInDBBase, tags=["old"])
async def get_old_for_text(text_id: int, db: Session = Depends(get_db)):
    text_id = crud.get_new_text_id_by_old_id(db, text_id)
    old = crud.get_old_for_text(db, text_id)
    if old is None:
        raise HTTPException(status_code=404, detail="Old not found")
    filename = old.filename
    filename = filename.replace("/home/concordance/web2py/applications/test/", "../")
    with open(filename, "r") as f:
        old.body = f.read()
   
    return old

@app.get("/variant/{id}", response_model=schemas.VariantInDBBase, tags=["variants"])
def read_variant(id, db: Session = Depends(get_db)):
    db_variant = crud.get_variant(db, id=id)
    if db_variant is None:
        raise HTTPException(status_code=404, detail="Variant not found")
    return db_variant

@app.get("/variant/text/{text_id}", tags=["variants"])
def read_variant_by_text_id(text_id: int, db: Session = Depends(get_db)):
    text_id = crud.get_new_text_id_by_old_id(db, text_id)
    db_variant = crud.get_variants_for_text_id(db, text_id)
    if len(db_variant) == 0:
        raise HTTPException(status_code=404, detail="Variant not found")
    for variant in db_variant:
        filename = variant.filename
        filename = filename.replace("/home/concordance/web2py/applications/test/", "../")
        with open(filename, "r") as f:
            variant.body = f.read()
    return db_variant

@app.get("/texts/count/author/", response_model=int, tags=["texts"])
def read_texts_count_by_author(author_id: int, db: Session = Depends(get_db)):
    db_texts = crud.get_texts_count_by_author(db, author_id=author_id)
    if db_texts is None:
        raise HTTPException(status_code=404, detail="Text not found")
    return db_texts

@app.get("/locations/", response_model=List[tuple], tags=["locations"])
def read_locations(db: Session = Depends(get_db)):
    db_locations = crud.get_locations(db)
    if db_locations is None:
        raise HTTPException(status_code=404, detail="Location not found")
    return db_locations[:200]


@app.get("/locations/{location_name}", response_model=schemas.LocationInDBBase, tags=["locations"])
def read_location(location_name: str, db: Session = Depends(get_db)):
    db_location = crud.get_location_by_name(db, name=location_name)
    if db_location is None:
        raise HTTPException(status_code=404, detail="Location not found")
    return db_location

@app.get("/texts/create_tei/{id}", tags=["texts"])
def create_tei(id: int, db: Session = Depends(get_db)):
    print(id)
    id = crud.get_new_text_id_by_old_id(db, id)
    print("new id", id)
    text = crud.get_text(db, id=id)
    if text is None:
        raise HTTPException(status_code=404, detail="Text not found")
    return create_TEI(text)