import os.path

from fastapi import FastAPI, UploadFile, File, HTTPException

app = FastAPI(debug=True)

@app.post('/upload')
async def upload(file: UploadFile = File(...)) -> dict:
    allowed_extentions = [".dcm", ".jpg", ".png", ".pdf"]
    file_extention = os.path.splitext(file.filename)[1].lower()
    if file_extention not in allowed_extentions:
        raise HTTPException(status_code=400, detail='Wrong extention')

    return {
        "responce": "All is OK",
        "file_name": file.filename
    }

    #DICOM(.dcm), JPG, PNG, PDF

