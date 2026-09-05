import uuid

from app.database import get_db
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

router = APIRouter(prefix="/documents")


@router.post("/", status_code=status.HTTP_200_OK)
async def upload_file(
    file: UploadFile = File(...),
    user_id: uuid.UUID = Form(...),
    db: Session = Depends(get_db),
):
    return {"id": user_id, "file": file.filename}
