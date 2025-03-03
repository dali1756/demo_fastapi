from fastapi import Request
import uvicorn
from apps import app
from apps.user.views import user
from fastapi.responses import RedirectResponse
from fastapi.exceptions import HTTPException
from apps import templates
from fastapi.staticfiles import StaticFiles

@app.get("/")
def root():
    return RedirectResponse(url="/users")

@app.exception_handler(404)
async def custom_404_handler(request: Request, exc: HTTPException):
    return templates.TemplateResponse("errors/404.html", {"request": request, "message": "找不到您要的頁面"}, status_code=404)

app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(user)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)