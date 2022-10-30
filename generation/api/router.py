from fastapi import APIRouter, HTTPException, status
from api.models import GenerationGETStatus, GenerationGETResult
from api.tasks import run_generation
from celery.result import AsyncResult
from fastapi.responses import JSONResponse, FileResponse
from pathlib import Path

generation_v1 = APIRouter()


@generation_v1.post('/push', tags=['generation'])
async def post_generation(voice: str, text: str):

    task = run_generation.delay(
        voice=voice,
        text=text,
    )
    launched_task = AsyncResult(str(task))
    return JSONResponse(
        content=GenerationGETStatus(task_id=str(task), status=launched_task.status, state=launched_task.state).dict(),
        status_code=status.HTTP_202_ACCEPTED
    )


@generation_v1.get('/status', tags=['generation'])
async def get_status(task_id: str):
    task = AsyncResult(task_id)
    if task.ready() and task.status != 'REVOKED':
        path = task.get()
        return JSONResponse(
            content=GenerationGETStatus(task_id=str(task), status=task.status, state=task.state,
                                        result=GenerationGETResult(file_path=path)).dict(),
            status_code=status.HTTP_200_OK
        )
    else:
        return JSONResponse(
            content=GenerationGETStatus(task_id=str(task), status=task.status, state=task.state).dict(),
            status_code=status.HTTP_200_OK
        )


@generation_v1.get('/download', tags=['generation'])
async def get_result(file_path: str):
    if not Path(file_path).is_file():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'{file_path} not found')

    return FileResponse(file_path)
