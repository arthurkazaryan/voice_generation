from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.router import generation_v1
import uvicorn

app = FastAPI(openapi_url='/api/v1/generation/openapi.json', docs_url='/api/v1/generation/docs')

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

app.include_router(generation_v1, prefix='/api/v1/generation')

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=7861)
