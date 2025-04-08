from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import shutil, os, uuid

# ✅ Import emotion analyzer function
from videos_analysis import analyze_emotion

# ✅ Define Pydantic model for filename input
class VideoRequest(BaseModel):
    filename: str

# ✅ Initialize FastAPI app
app = FastAPI()
print("✅ main.py loaded")

# ✅ Create uploads folder if not exists
UPLOAD_FOLDER = os.path.abspath("uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ✅ Setup CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Home route
@app.get("/")
def home():
    return {"message": "Depression Detection API is running"}

# ✅ Video upload route
@app.post("/upload_video")
async def upload_video(file: UploadFile = File(...)):
    try:
        filename = f"{uuid.uuid4().hex}_{file.filename}"
        file_path = os.path.join(UPLOAD_FOLDER, filename)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        return {"message": "Video uploaded successfully", "filename": filename}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ✅ Emotion analysis route using Pydantic model
@app.post("/analyze_video")
async def analyze_video(req: VideoRequest):
    filename = req.filename
    video_path = os.path.join(UPLOAD_FOLDER, filename)

    if not os.path.exists(video_path):
        raise HTTPException(status_code=404, detail="Video not found")

    try:
        result = analyze_emotion(video_path)
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
