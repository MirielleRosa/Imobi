from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import uvicorn
from routes import main_routes

app = FastAPI()
#app.middleware(middleware_type="http")(atualizar_cookie_autenticacao)
#configurar_excecoes(app)
app.mount(path="/static", app=StaticFiles(directory="static"), name="static")
app.include_router(main_routes.router)

if __name__ == "__main__":
    uvicorn.run(app="main:app", port=8000, reload=True)
