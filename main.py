import uvicorn
import pkgutil
import importlib
import controllers
from fastapi import FastAPI

app = FastAPI()

# auto-import
for _, module_name, _ in pkgutil.iter_modules(controllers.__path__):
    module = importlib.import_module(f"controllers.{module_name}")
    if hasattr(module, "router"):
        app.include_router(module.router)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        timeout_keep_alive=300,
        timeout_graceful_shutdown=300
    )

@app.get("/")
async def root():
    return {"message": "Astro-moment is working"}

