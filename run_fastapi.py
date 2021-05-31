import uvicorn
from config import Uvicorn


if __name__ == "__main__":
    uvicorn.run("app:app", host=Uvicorn.HOST, port=Uvicorn.PORT,
                debug=Uvicorn.DEBUG, reload=Uvicorn.RELOAD)
