from fastapi import APIRouter, Request, Form, Depends, HTTPException, UploadFile, File
from fastapi.responses import RedirectResponse
from apps import templates
from models.user import User
from sqlalchemy.orm import Session
from apps.deps import get_db
from utils.s3 import S3Client
import uuid

user = APIRouter(prefix="/users")
s3_client = S3Client()

@user.post("/{user_id}/avatar")
def upload_avatar(user_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    # check file type
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="必需是圖檔")
    # check user exist
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="查無使用者")
    # 檔名生成
    file_extension = file.filename.split(".")[-1]
    unique_filename = f"{user_id}_{uuid.uuid4()}.{file_extension}"
    # upload to S3
    file_url = s3_client.upload_file(file.file, unique_filename)
    if not file_url:
        raise HTTPException(status_code=500, detail="檔案上傳錯誤")
    # update user avatar_url
    user.avatar_url = file_url
    db.commit()
    return {"avatar_url": file_url}

@user.get("/")
def index(request: Request, db: Session = Depends(get_db)):
    users = db.query(User).order_by(User.id).all()
    return templates.TemplateResponse("users/index.html", {"request": request, "users": users})

@user.get("/new")
def new(request: Request):
    return templates.TemplateResponse("users/new.html", {"request": request})

@user.get("/{user_id}")
def show(request: Request, user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        return templates.TemplateResponse("users/show.html", {"request": request, "user": user})
    else:
        return templates.TemplateResponse("errors/404.html", {"request": request, "message": "查無使用者"}, status_code=404)

@user.post("/")
def create(request: Request, name: str = Form(...), email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    try:
        new_user = User(name=name, email=email, password=password)
        db.add(new_user)
        db.commit()
        return RedirectResponse(url="/users", status_code=303)
    except Exception as e:
        return templates.TemplateResponse("users/new.html", {"request": request, "error": str(e)})

@user.get("/{user_id}/edit")
def edit(request: Request, user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        return templates.TemplateResponse("users/edit.html", {"request": request, "user": user})
    else:
        return templates.TemplateResponse("errors/404.html", {"request": request, "message": "查無使用者"}, status_code=404)

@user.post("/{user_id}/edit")
def update(user_id: int, name: str = Form(...), email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        user.name = name
        user.email = email
        user.password = password
        db.commit()
        return RedirectResponse(url="/users", status_code=303)
    else:
        return HTTPException(status_code=404, detail="查無使用者")

@user.post("/{user_id}/delete")
def delete(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        db.delete(user)
        db.commit()
        return RedirectResponse(url="/users", status_code=303)
    else:
        return HTTPException(status_code=404, detail="查無使用者")