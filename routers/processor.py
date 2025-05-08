from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional
import os
import shutil

from your_script import TextIn

router = APIRouter()

class ProcessRequest(BaseModel):
    start: int
    end: int
    skiplinks: bool
    debug: bool
    title: str
    author: str
    chapters_per_file: int = 1
    customwords: str = "custom_words.txt"

@router.post("/process_epub/")
async def process_epub(file: UploadFile = File(...), start: int = Form(...), end: int = Form(...),
                       skiplinks: bool = Form(...), debug: bool = Form(...),
                       title: str = Form(...), author: str = Form(...),
                       chapters_per_file: int = Form(1),
                       customwords: str = Form("custom_words.txt")):
    try:
        temp_file_path = f"temp_{file.filename}"
        with open(temp_file_path, "wb") as temp_file:
            shutil.copyfileobj(file.file, temp_file)

        text_processor = TextIn(
            source=temp_file_path,
            start=start,
            end=end,
            skiplinks=skiplinks,
            debug=debug,
            title=title,
            author=author,
            chapters_per_file=chapters_per_file,
            customwords=customwords
        )
        text_processor.get_chapters_epub()

        return JSONResponse(content={"message": "EPUB file processed successfully."}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=400)
    finally:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)

@router.post("/process_txt/")
async def process_txt(file: UploadFile = File(...), start: int = Form(...), end: int = Form(...),
                      skiplinks: bool = Form(...), debug: bool = Form(...),
                      title: str = Form(...), author: str = Form(...),
                      chapters_per_file: int = Form(1),
                      customwords: str = Form("custom_words.txt")):
    try:
        temp_file_path = f"temp_{file.filename}"
        with open(temp_file_path, "wb") as temp_file:
            shutil.copyfileobj(file.file, temp_file)

        text_processor = TextIn(
            source=temp_file_path,
            start=start,
            end=end,
            skiplinks=skiplinks,
            debug=debug,
            title=title,
            author=author,
            chapters_per_file=chapters_per_file,
            customwords=customwords
        )
        text_processor.get_chapters_epub()

        return JSONResponse(content={"message": "TXT file processed successfully."}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=400)
    finally:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)

@router.get("/get_customwords/")
async def get_customwords():
    try:
        with open("custom_words.txt", 'r') as f:
            words = f.read().splitlines()
        return {"custom_words": words}
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=400)

@router.post("/add_customword/")
async def add_customword(word: str = Form(...), pronunciation: str = Form(...)):
    try:
        entry = f"{word}|{pronunciation}\n"
        with open("custom_words.txt", "a", encoding="utf-8") as f:
            f.write(entry)
        return {"message": f"Word '{word}' added successfully."}
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=400)
