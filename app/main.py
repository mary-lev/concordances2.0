from typing import List
import pandas as pd
from fastapi import FastAPI, Depends, HTTPException, File, UploadFile
from sqlalchemy.orm import Session
import crud, models, schemas
from database import SessionLocal, engine
from utils import get_date

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/authors/", response_model=schemas.AuthorBase)
def create_author(author: schemas.AuthorBase, db: Session = Depends(get_db)):
    return crud.create_author(db=db, author=author)

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
    for _, row in df.iterrows():
        author_id = int(row['group_text.author'])
        year = row['group_text.year']
        year_from_db = None
        if pd.notna(year) and year != '':
            year_from_db = crud.get_date(db=db, date_id=year)
            if not year_from_db:
                if "—" in year:
                    date_data = schemas.DateOfWritingCreate(**{
                        "start_year": int(year.split("—")[0]),
                        "end_year": int(year.split("—")[1]),
                    })
                elif "–" in year:
                    date_data = schemas.DateOfWritingCreate(**{
                        "start_year": int(year.split("–")[0]),
                        "end_year": int(year.split("–")[1]),
                    })

                elif "-" in year:
                    start_year, end_year = year.split("-")
                    date_data = schemas.DateOfWritingCreate(**{
                        "start_year": int(start_year),
                        "end_year": int(end_year),
                    })
                else:
                    date_data = schemas.DateOfWritingCreate(**{"exact_year": year})
                print(date_data)
                year_from_db = crud.create_date(db=db, date=date_data)
            if year_from_db:
                year_from_db = year_from_db.id
        group_data = {
            "id": row['group_text.id'],
            "title": row['group_text.title'],
            "author_id": author_id,
            "dedication": row['group_text.dedication'],
            "supergroup": int(row['group_text.superpgroup']) if pd.notna(row['group_text.superpgroup']) and row['group_text.superpgroup'] != '' else None,
            "subtitle": "",
            "author_comment": "",
            "date_of_writing_id": year_from_db or None,
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
    for _, row in df.iterrows():
        author_id = int(row['text1.author'])
        date_of_writing = get_date(row, db)
        # epi, publication, location
        text_data = {
            "id": row['text1.id'],
            "title": row['text1.title'],
            "first_string": row['text1.first_string'],
            "body": row['text1.body'],
            "filename": row['text1.filename'],
            "author_id": author_id,
            "dedication": row['text1.dedication'],
            "group_text_id": int(row['text1.group_text']) if pd.notna(row['text1.group_text']) and row['text1.group_text'] != '' else None,
            "subtitle": row["text1.under_title"],
            "author_comment": row["text1.v"],
            "date_of_writing_id": date_of_writing or None,
            "writing_location_id": None,
            "publication_id": None,
            "book_page_start": "",
            "book_page_end": "",
            "n_in_group": int(row['text1.n_in_group']) if pd.notna(row['text1.n_in_group']) and row['text1.n_in_group'] != '' else None,
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

@app.post("/dateofwritings/", response_model=schemas.DateOfWritingBase)
def create_date(date: schemas.DateOfWritingBase, db: Session = Depends(get_db)):
    return crud.create_date(db=db, date=date)

