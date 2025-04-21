from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from db.database import engine, Base
from routers import add_user, recommendations
import uvicorn

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI Resume Analyzer",
    version="1.0.0",
)

# CORS config
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(add_user.router, prefix="/add_user", tags=["Add User"])
app.include_router(recommendations.router, prefix="/recommend", tags=["Recommendations"])


@app.get("/")
async def root():
    return {"message": "Al Okay"}


# Run with uvicorn
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)