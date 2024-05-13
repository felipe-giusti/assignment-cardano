from fastapi import APIRouter, File, UploadFile
from fastapi.responses import Response
from api.enrich_data import enrich_data
import io

router = APIRouter()

@router.post("/enrich")
async def enrich_file(file: UploadFile = File(...)):

    file_contents = await file.read()

    csv_data = await enrich_data(io.BytesIO(file_contents))

    csv_io = io.StringIO(csv_data)

    headers = {
        'Content-Disposition': f'attachment; filename=enriched_{file.filename}',
        'Content-Type': 'text/csv',
    }

    return Response(content=csv_io.getvalue(), headers=headers)
