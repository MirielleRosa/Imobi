import logging
from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from models.pessoa_model import Pessoa
from util.cookies import adicionar_mensagem_erro
from util.auth import obter_pessoa_logada
from util.templates import obter_jinja_templates

templates = obter_jinja_templates("templates")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def configurar_excecoes(app: FastAPI):
    @app.exception_handler(401)
    async def unauthorized_exception_handler(request: Request, _):
        return_url = f"?return_url={request.url.path}"
        response = RedirectResponse(
            f"/entrar{return_url}", status_code=status.HTTP_302_FOUND
        )
        adicionar_mensagem_erro(
            response,
            f"A página {request.url.path} é restrita a usuários logados. Identifique-se para poder prosseguir.",
        )
        return response

    @app.exception_handler(403)
    async def forbidden_exception_handler(request: Request, _):
        usuario = await obter_pessoa_logada(request)
        return_url = f"?return_url={request.url.path}"
        response = RedirectResponse(
            f"/entrar{return_url}", status_code=status.HTTP_302_FOUND
        )
        adicionar_mensagem_erro(
            response,
            f"Você está logado como <b>{usuario.nome}</b> e seu perfil de usuário não tem autorização de acesso à página <b>{request.url.path}</b>. Entre com um usuário do perfil adequado para poder acessar a página em questão.",
        )
        return response

    @app.exception_handler(404)
    async def page_not_found_exception_handler(
        request: Request, pessoa_logada=Depends(obter_pessoa_logada)
    ):
        return templates.TemplateResponse(
            "pages/404.html", {"request": request, "pessoa": pessoa_logada}
        )

    @app.exception_handler(HTTPException)
    async def http_exception_handler(
        request: Request,
        ex: HTTPException,
        pessoa_logada: Pessoa = Depends(obter_pessoa_logada),
    ):
        logger.error("Ocorreu uma exceção não tratada: %s", ex)
        view_model = {
            "request": request,
            "pessoa": pessoa_logada,
            "detail": "Erro na requisição HTTP.",
        }
        return templates.TemplateResponse(
            "pages/erro.html", view_model, status_code=ex.status_code
        )

    @app.exception_handler(Exception)
    async def general_exception_handler(
        request: Request,
        ex: Exception,
        pessoa_logada: Pessoa = Depends(obter_pessoa_logada),
    ):
        logger.error("Ocorreu uma exceção não tratada: %s", ex)
        view_model = {
            "request": request,
            "pessoa": pessoa_logada,
            "detail": "Erro interno do servidor.",
        }
        return templates.TemplateResponse("pages/erro.html", view_model, status_code=500)
