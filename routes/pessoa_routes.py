from fastapi import APIRouter, Depends, HTTPException, Request, status, File, UploadFile
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from models.imovel_model import Imovel
from models.pessoa_model import Pessoa
from repositories.cidade_repo import CidadeRepo
from repositories.imovel_repo import ImovelRepo
from repositories.pessoa_repo import PessoaRepo
from util.auth import checar_autorizacao, obter_pessoa_logada
from util.cookies import adicionar_mensagem_sucesso
import uuid
import firebaseconfig

router = APIRouter()

templates = Jinja2Templates(directory="templates")

@router.get("/perfil")
def get_root(request: Request, pessoa_logada: Pessoa = Depends(obter_pessoa_logada)):
    checar_autorizacao(pessoa_logada)
    return templates.TemplateResponse("perfil.html", {"request": request, "pessoa": pessoa_logada})

@router.get("/imoveis")
def get_root(request: Request, pessoa_logada: Pessoa = Depends(obter_pessoa_logada)):
    checar_autorizacao(pessoa_logada)
    return templates.TemplateResponse("imoveis.html", {"request": request, "pessoa": pessoa_logada})

@router.get("/cadastro_imovel")
def get_root(request: Request, pessoa_logada: Pessoa = Depends(obter_pessoa_logada)):
    checar_autorizacao(pessoa_logada)
    cidades = CidadeRepo.obter_todos()
    return templates.TemplateResponse("cadastro_imovel.html", {"request": request, "pessoa": pessoa_logada, "cidades": cidades})

@router.get("/sair", response_class=RedirectResponse)
async def get_sair(
    request: Request, pessoa_logada: Pessoa = Depends(obter_pessoa_logada)
):
    checar_autorizacao(pessoa_logada)
    if pessoa_logada:
        PessoaRepo.alterar_token(pessoa_logada.email, "")
    response = RedirectResponse("/", status.HTTP_303_SEE_OTHER)
    response.set_cookie(key="auth_token", value=" ", httponly=True, expires=0)
    adicionar_mensagem_sucesso(response, "Saída realizada com sucesso.")
    return response

@router.post("/post_cadastro_imovel", response_class=JSONResponse)
async def post_cadastro_imovel(request: Request, pessoa_logada: Pessoa = Depends(obter_pessoa_logada)):
    checar_autorizacao(pessoa_logada)
    
    dados = await request.json()
    try:
        imagem = dados.get("imagem", "")
        if isinstance(imagem, dict):
            imagem = ""

        # Verifique se o campo cidade_id está no JSON
        cidade_id = dados.get("cidade_id")
        if not cidade_id:
            raise HTTPException(status_code=400, detail="Cidade não selecionada ou inválida.")

        novo_imovel = Imovel(
            titulo=dados.get("titulo"),
            descricao=dados.get("descricao"),
            endereco=dados.get("endereco"),
            preco=dados.get("preco"),
            area=dados.get("area"),
            quartos=dados.get("quartos"),
            banheiros=dados.get("banheiros"),
            imagem=imagem,
            pessoa_id=pessoa_logada.id,
            cidade_id=cidade_id  # Use cidade_id diretamente
        )

        print(dados)
    except KeyError as e:
        raise HTTPException(status_code=400, detail=f"Campo obrigatório ausente: {e}")

    imovel_inserido = ImovelRepo.inserir(novo_imovel)
    if not imovel_inserido:
        raise HTTPException(status_code=400, detail="Erro ao cadastrar imóvel.")

    return {"redirect": {"url": "/imoveis", "message": "Cadastro de imóvel realizado com sucesso."}}
