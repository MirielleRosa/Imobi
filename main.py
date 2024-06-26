from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import uvicorn
from repositories.cidade_repo import CidadeRepo
from repositories.imovel_repo import ImovelRepo
from repositories.pessoa_repo import PessoaRepo
from routes import main_routes, pessoa_routes
from util.auth import atualizar_cookie_autenticacao
from util.exceptions import configurar_excecoes

PessoaRepo.criar_tabela()
CidadeRepo.criar_tabela()
ImovelRepo.criar_tabela()

CidadeRepo.inserir_cidades_json("sql/json/cidades.json")

app = FastAPI()
app.middleware(middleware_type="http")(atualizar_cookie_autenticacao)
configurar_excecoes(app)
app.mount(path="/static", app=StaticFiles(directory="static"), name="static")
app.include_router(main_routes.router)
app.include_router(pessoa_routes.router)

if __name__ == "__main__":
    uvicorn.run(app="main:app", port=8000, reload=True)
