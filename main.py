from fastapi import FastAPI
import pkgutil
import importlib
import controllers

app = FastAPI()

# auto-import
for _, module_name, _ in pkgutil.iter_modules(controllers.__path__):
    module = importlib.import_module(f"controllers.{module_name}")
    if hasattr(module, "router"):
        app.include_router(module.router)

@app.get("/")
async def root():
    return {"message": "Astro-moment is working"}
