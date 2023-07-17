from typing import List, Dict
import pandas as pd
from fastapi import FastAPI, Depends, HTTPException, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import crud, models, schemas
from database import SessionLocal, engine
#from utils import get_date

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


@app.post("/authors/", response_model=schemas.AuthorBase)
def create_author(author: schemas.AuthorBase, db: Session = Depends(get_db)):
    return crud.create_author(db=db, author=author)

@app.get("/authors/", response_model=List[schemas.AuthorInDBBase])
def read_authors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    authors = crud.get_authors(db, skip=skip, limit=limit)
    return authors

@app.post("/upload_publications/")
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

@app.post("/upload_authors/")
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

@app.post("/upload_group_texts/")
async def upload_group_texts(file: UploadFile = File(...), db: Session = Depends(get_db)):
    df = pd.read_csv(file.file)
    df = df.fillna('')
    date_data = {}
    for _, row in df.iterrows():
        author_id = int(row['group_text.author'])
        year = row['group_text.year']
        if pd.notna(year) and year != '':
            if "—" in year:
                date_data["start_year"] = int(year.split("—")[0])
                date_data["end_year"] = int(year.split("—")[1])
            elif "–" in year:
                date_data["start_year"] = int(year.split("–")[0])
                date_data["end_year"] = int(year.split("–")[1])
            elif "-" in year:
                start_year, end_year = year.split("-")
                date_data["start_year"] = int(start_year)
                date_data["end_year"] = int(end_year)
            else:
                date_data["exact_year"] = int(year)

        group_data = {
            "id": row['group_text.id'],
            "title": row['group_text.title'],
            "author_id": author_id,
            "dedication": row['group_text.dedication'],
            "supergroup": int(row['group_text.superpgroup']) if pd.notna(row['group_text.superpgroup']) and row['group_text.superpgroup'] != '' else None,
            "subtitle": "",
            "author_comment": "",
            "exact_year": date_data.get("exact_year"),
            "start_year": date_data.get("start_year"),
            "end_year": date_data.get("end_year"),
            "writing_location_id": None,
            "publication_id": None,
            "book_page_start": "",
            "book_page_end": "",
        }
        
        group = schemas.GroupTextCreate(**group_data)
        group_instance = crud.create_grouptext(db=db, grouptext=group)
        if 'group_text.epigraph' in row and pd.notna(row['group_text.epigraph']) and row['group_text.epigraph'] != '':
            epi = {
                "epi_text": row['group_text.epigraph'],
                "textbase_id": group_instance.id,
            }
            epi_data = schemas.EpigraphCreate(**epi)
            crud.create_epigraph(db=db, epigraph=epi_data)

    return {"filename": file.filename}

@app.post("/upload_texts/")
async def upload_texts(file: UploadFile = File(...), db: Session = Depends(get_db)):
    df = pd.read_csv(file.file)
    df = df.fillna('')
    df.replace('<NULL>', '', inplace=True)
    for _, row in df.iterrows():
        print(row['text1.id'])
        author_id = int(row['text1.author'])
        text_data = {
            "id": row['text1.id'],
            "title": row['text1.title'],
            "first_string": row['text1.first_string'],
            "body": row['text1.body'],
            "filename": row['text1.filename'],
            "author_id": author_id,
            "dedication": row['text1.dedication'],
            "subtitle": row["text1.under_title"],
            "author_comment": row["text1.v"],
            "exact_year": int(row['text1.year_writing']) if pd.notna(row['text1.year_writing']) and row['text1.year_writing'] != '' else None,
            "exact_month": int(row['text1.month_writing']) if pd.notna(row['text1.month_writing']) and row['text1.month_writing'] != '' else None,
            "exact_day": int(row['text1.day_writing']) if pd.notna(row['text1.day_writing']) and row['text1.day_writing'] != '' else None,
            "dubious_year": row['text1.dyear_writing'],
            "dubious_month": row['text1.dmonth_writing'],
            "dubious_day": row['text1.dday_writing'],
            "season": row['text1.season_writing'],
            "writing_location_id": None,
            "publication_id": None,
            "book_page_start": "",
            "book_page_end": "",
            "n_in_group": int(row['text1.n_in_group']) if pd.notna(row['text1.n_in_group']) and row['text1.n_in_group'] != '' else 0,
            "group_text_id": int(row['text1.group_text']) if pd.notna(row['text1.group_text']) and row['text1.group_text'] != '' else None,
        }
        
        text = schemas.TextCreate(**text_data)
        text_instance = crud.create_text(db=db, text=text)
        """if "text.epigraph_author" in row and pd.notna(row['text.epigraph_author']) and row['text.epigraph_author'] != '':
            author = {
                "name": row['text.epigraph_author'],
                "textbase_id": text_instance.id,
            }
            author_data = schemas.AuthorCreate(**author)
            crud.create_author(db=db, author=author_data)"""
        """if 'text.epigraph' in row and pd.notna(row['text.epigraph']) and row['text.epigraph'] != '':
            epi = {
                "epi_text": row['text.epigraph'],
                "epi_author": row['text.epigraph_author'],
                "epi_book": row['text.epigraph_text_name'],
                "textbase_id": text_instance.id,
            }
            epi_data = schemas.EpigraphCreate(**epi)
            crud.create_epigraph(db=db, epigraph=epi_data)"""
        if 'text1.book' in row and pd.notna(row['text1.book']) and row['text1.book'] != '':
            # find book
            book = crud.get_publication_by_title(db, title=row['text1.book'])
            if book is None:
                pub = {
                    "title": row['text1.book'],
                }
                pub_data = schemas.PublicationCreate(**pub)
                book = crud.create_publication(db=db, publication=pub_data)
                if book:
                    text_instance.publication_id = book.id
                    db.commit()
        if 'text1.writing_location' in row and pd.notna(row['text1.writing_location']) and row['text1.writing_location'] != '':
            location = crud.get_location_by_name(db, name=row['text1.writing_location'])
            if location is None:
                loc = {
                    "name": row['text1.writing_location'],
                }
                loc_data = schemas.LocationCreate(**loc)
                location = crud.create_location(db=db, location=loc_data)
                if location:
                    text_instance.writing_location_id = location.id
                    db.commit()
        
    return {"filename": file.filename}

@app.get("/authors/{author_id}", response_model=schemas.AuthorInDBBase)
def read_author(author_id: int, db: Session = Depends(get_db)):
    db_author = crud.get_author(db, author_id=author_id)
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return db_author

@app.post("/grouptexts/", response_model=schemas.GroupTextCreate)
def create_grouptext(grouptext: schemas.GroupTextBase, db: Session = Depends(get_db)):
    return crud.create_grouptext(db=db, grouptext=grouptext)

@app.get("/all_grouptexts/", response_model=List[schemas.GroupTextBase])
def read_all_grouptexts(db: Session = Depends(get_db)):
    db_grouptexts = crud.get_grouptexts(db)
    if db_grouptexts is None:
        raise HTTPException(status_code=404, detail="GroupText not found")
    return db_grouptexts

@app.get("/grouptexts/{grouptext_id}", response_model=schemas.GroupTextBase)
def read_grouptext(grouptext_id: int, db: Session = Depends(get_db)):
    db_grouptext = crud.get_grouptext(db, grouptext_id=grouptext_id)
    if db_grouptext is None:
        raise HTTPException(status_code=404, detail="GroupText not found")
    return db_grouptext

@app.get("/texts/{text_id}", response_model=schemas.TextInDBBase)
def read_text(text_id: int, db: Session = Depends(get_db)):
    db_text = crud.get_text(db, text_id=text_id)
    if db_text is None:
        raise HTTPException(status_code=404, detail="Text not found")
    return db_text

@app.get("/texts/author/", response_model=List[schemas.TextInDBBase])
def read_texts_by_author(author_id: int, db: Session = Depends(get_db)):
    db_texts = crud.get_texts_by_author(db, author_id=author_id)
    if db_texts is None:
        raise HTTPException(status_code=404, detail="Text not found")
    return db_texts

@app.get("/texts/count/author/", response_model=int)
def read_texts_count_by_author(author_id: int, db: Session = Depends(get_db)):
    db_texts = crud.get_texts_count_by_author(db, author_id=author_id)
    if db_texts is None:
        raise HTTPException(status_code=404, detail="Text not found")
    return db_texts
