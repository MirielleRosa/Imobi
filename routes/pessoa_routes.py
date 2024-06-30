from typing import List
from datetime import datetime
import os
from urllib.parse import urlencode
from fastapi import APIRouter, Depends, HTTPException, Request, status, File, UploadFile,  Form
from fastapi.responses import JSONResponse, RedirectResponse
from models.cidade_model import Cidade
from models.imovel_model import Imovel
from models.pessoa_model import Pessoa
from firebase_admin import storage as admin_storage
from repositories.cidade_repo import CidadeRepo
from repositories.imovel_repo import ImovelRepo
from repositories.pessoa_repo import PessoaRepo
from util.auth import *
from util.cookies import *
import uuid
import util.firebaseconfig as firebaseconfig
from util.templates import obter_jinja_templates
from pathlib import Path

UPLOAD_DIR = Path("static/img")
router = APIRouter()
templates = obter_jinja_templates("templates/pessoa")

@router.get("/perfil")
def get_perfil(request: Request, pessoa_logada: Pessoa = Depends(obter_pessoa_logada)):
    checar_autorizacao(pessoa_logada)
    return templates.TemplateResponse("pages/perfil.html", {"request": request, "pessoa": pessoa_logada})

@router.post("/alterar_perfil")
async def post_alterar_perfil(
    request: Request,
    imagem: UploadFile = File(None),
    pessoa_logada: Pessoa = Depends(obter_pessoa_logada)
):
    checar_autorizacao(pessoa_logada)

    form_data = await request.form()
    dados = {key: form_data[key] for key in form_data}

    try:
        if imagem and imagem.filename:
            file_name = f"{uuid.uuid4()}.png"
            image_path = f"imagens_perfil/{file_name}"

            with open(file_name, "wb") as buffer:
                buffer.write(await imagem.read())

            firebaseconfig.storage.child(image_path).put(file_name)

            image_url = firebaseconfig.storage.child(image_path).get_url(None)

            os.remove(file_name)
        else:
            image_url = pessoa_logada.imagem_perfil 
        
        data_nascimento_str = dados.get("data_nascimento")
        if data_nascimento_str:
            try:
                data_nascimento = datetime.strptime(data_nascimento_str, "%Y-%m-%d").date()
            except ValueError as e:
                raise HTTPException(status_code=400, detail=f"Erro ao converter data de nascimento: {str(e)}")

        alterar_perfil = Pessoa(
            id=pessoa_logada.id,
            nome=dados.get("nome"),
            cpf=dados.get("cpf"),
            data_nascimento=data_nascimento,
            endereco=dados.get("endereco"),
            telefone=dados.get("telefone"),
            email=dados.get("email"),
            senha=pessoa_logada.senha, 
            imagem_perfil=image_url, 
            descricao=dados.get("descricao")
        )
        PessoaRepo.alterar(alterar_perfil)

    except KeyError as e:
        raise HTTPException(status_code=400, detail=f"Campo obrigatório ausente: {e}")

    return RedirectResponse(url="/perfil", status_code=status.HTTP_303_SEE_OTHER)

@router.post("/post_cadastro_cidade", response_class=JSONResponse)
async def post_cadastro_cidade(request: Request, pessoa_logada: Pessoa = Depends(obter_pessoa_logada)):
    checar_autorizacao(pessoa_logada)
    
    form_data = await request.form()
    nome = form_data.get("nome")
    estado = form_data.get("estado")
    
    nova_cidade = Cidade(nome=nome, estado=estado)  

    try:
        cidade_inserida = CidadeRepo.inserir(nova_cidade)
        if cidade_inserida:
            return RedirectResponse(url="/cadastro_imovel", status_code=status.HTTP_303_SEE_OTHER)
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Erro ao cadastrar a cidade!")
    except Exception as e:
        print(f"Erro ao inserir cidade no banco de dados: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Erro interno ao cadastrar cidade")

@router.get("/imoveis")
def get_imoveis(request: Request, pessoa_logada: Pessoa = Depends(obter_pessoa_logada)):
    checar_autorizacao(pessoa_logada)
    imoveis = ImovelRepo.obter_todos_pessoa(pessoa_logada.id) 
    return templates.TemplateResponse("pages/imoveis.html", {"request": request, "pessoa": pessoa_logada, "imoveis": imoveis})

@router.get("/cadastro_imovel")
def get_cadastro_imovel(request: Request, pessoa_logada: Pessoa = Depends(obter_pessoa_logada)):
    checar_autorizacao(pessoa_logada)
    cidades = CidadeRepo.obter_todos()
    return templates.TemplateResponse("pages/cadastro_imovel.html", {"request": request, "pessoa": pessoa_logada, "cidades": cidades})
 
@router.post("/post_cadastro_imovel")
async def post_cadastro_imovel(
    request: Request,
    imagem_principal: UploadFile = File(None),
    imagens_secundarias: List[UploadFile] = File(None),
    pessoa_logada: Pessoa = Depends(obter_pessoa_logada)
):
    checar_autorizacao(pessoa_logada)
    
    form_data = await request.form()
    dados = {key: form_data[key] for key in form_data}
    
    try:
        # Processar imagem principal se não for None
        image_url_principal = None
        if imagem_principal and imagem_principal.size > 0:
            file_name_principal = f"{uuid.uuid4()}.png"
            image_path_principal = f"imagens_imoveis/{file_name_principal}"
            
            with open(file_name_principal, "wb") as buffer:
                buffer.write(await imagem_principal.read())
            
            firebaseconfig.storage.child(image_path_principal).put(file_name_principal)
            image_url_principal = firebaseconfig.storage.child(image_path_principal).get_url(None)
            os.remove(file_name_principal)
        
        total_size = sum(imagem.size for imagem in imagens_secundarias)

        imagens_urls_secundarias = []
        if total_size > 0:
            for imagem in imagens_secundarias:
                file_name_secundario = f"{uuid.uuid4()}.png"
                image_path_secundario = f"imagens_imoveis/{file_name_secundario}"
                
                with open(file_name_secundario, "wb") as buffer:
                    buffer.write(await imagem.read())
                
                firebaseconfig.storage.child(image_path_secundario).put(file_name_secundario)
                image_url_secundaria = firebaseconfig.storage.child(image_path_secundario).get_url(None)
                imagens_urls_secundarias.append(image_url_secundaria)
                
                os.remove(file_name_secundario)

        imagens_secundarias_str = ",".join(imagens_urls_secundarias)

        novo_imovel = Imovel(
            titulo=dados.get("titulo"),
            tipo=dados.get("tipo"),
            descricao=dados.get("descricao"),
            endereco=dados.get("endereco"),
            preco=float(dados.get("preco")),
            area=int(dados.get("area")),
            quartos=int(dados.get("quartos")),
            banheiros=int(dados.get("banheiros")),
            garagem=int(dados.get("garagem")),
            piscina=bool(dados.get("piscina")),
            ar_condicionado=bool(dados.get("ar_condicionado")),
            churrasqueira=bool(dados.get("churrasqueira")),
            jardim=bool(dados.get("jardim")),
            portaria=bool(dados.get("portaria")),
            academia=bool(dados.get("academia")),
            imagem_principal=image_url_principal, 
            imagens_secundarias=imagens_secundarias_str, 
            pessoa_id=pessoa_logada.id,
            cidade_id=int(dados.get("cidade_id"))
        )

        imovel_inserido = ImovelRepo.inserir(novo_imovel)
        if not imovel_inserido:
            error_message = "Erro ao cadastrar imóvel."
            return RedirectResponse(url=f"/cadastro_imovel?error={error_message}", status_code=status.HTTP_303_SEE_OTHER)

    except KeyError as e:
        return RedirectResponse(url=f"/cadastro_imovel?error={e}", status_code=status.HTTP_303_SEE_OTHER)

    return RedirectResponse(url="/imoveis", status_code=status.HTTP_303_SEE_OTHER)

@router.get("/editar_imovel/{imovel_id}")
def get_editar_imovel(imovel_id: int, request: Request, pessoa_logada: Pessoa = Depends(obter_pessoa_logada)):
    checar_autorizacao(pessoa_logada)
    imovel = ImovelRepo.obter_um(imovel_id)
    if not imovel or imovel.pessoa_id != pessoa_logada.id:
        raise HTTPException(status_code=404, detail="Imóvel não encontrado ou sem permissão.")
    
    cidades = CidadeRepo.obter_todos()
    return templates.TemplateResponse("pages/editar_imovel.html", {
        "request": request,
        "pessoa": pessoa_logada,
        "imovel": imovel,
        "cidades": cidades
    })

@router.post("/post_editar_imovel/{imovel_id}", response_class=JSONResponse)
async def post_editar_imovel(
    request: Request,
    imovel_id: int,
    imagem_principal: UploadFile = File(None),
    imagens_secundarias: List[UploadFile] = File(None),
    pessoa_logada: Pessoa = Depends(obter_pessoa_logada)
):
    checar_autorizacao(pessoa_logada)

    imovel = ImovelRepo.obter_um(imovel_id)
    if not imovel or imovel.pessoa_id != pessoa_logada.id:
        raise HTTPException(status_code=404, detail="Imóvel não encontrado ou sem permissão.")
    
    form_data = await request.form()

    try:

        if imagem_principal and imagem_principal.filename:
            file_name_principal = f"{uuid.uuid4()}.png"
            image_path_principal = f"imagens_imoveis/{file_name_principal}"

            with open(file_name_principal, "wb") as buffer:
                buffer.write(await imagem_principal.read())

            firebaseconfig.storage.child(image_path_principal).put(file_name_principal)
            image_url_principal = firebaseconfig.storage.child(image_path_principal).get_url(None)
            os.remove(file_name_principal)
        else:
            image_url_principal = imovel.imagem_principal

        total_size = 0
        for imagem_secundaria in imagens_secundarias:
            total_size += imagem_secundaria.size

        imagens_urls_secundarias = []
        imagens_secundarias_str = ""

        if total_size > 0:
            for imagem in imagens_secundarias:
                file_name_secundario = f"{uuid.uuid4()}.png"
                image_path_secundario = f"imagens_imoveis/{file_name_secundario}"
                
                with open(file_name_secundario, "wb") as buffer:
                    buffer.write(await imagem.read())
                

                firebaseconfig.storage.child(image_path_secundario).put(file_name_secundario)
                image_url_secundaria = firebaseconfig.storage.child(image_path_secundario).get_url(None)
                imagens_urls_secundarias.append(image_url_secundaria)
                os.remove(file_name_secundario)
            
            imagens_secundarias_str = ",".join(imagens_urls_secundarias)
        else:
            imagens_secundarias_str = imovel.imagens_secundarias
            
        alterar_imovel = Imovel(
            id=imovel.id,
            titulo=form_data.get("titulo"),
            tipo=form_data.get("tipo"),
            descricao=form_data.get("descricao"),
            endereco=form_data.get("endereco"),
            preco=float(form_data.get("preco")),
            area=int(form_data.get("area")),
            quartos=int(form_data.get("quartos")),
            banheiros=int(form_data.get("banheiros")),
            garagem=int(form_data.get("garagem")),
            piscina=bool(form_data.get("piscina")),
            ar_condicionado=bool(form_data.get("ar_condicionado")),
            churrasqueira=bool(form_data.get("churrasqueira")),
            jardim=bool(form_data.get("jardim")),
            portaria=bool(form_data.get("portaria")),
            academia=bool(form_data.get("academia")),
            imagem_principal=image_url_principal,
            imagens_secundarias=imagens_secundarias_str,
            cidade_id=int(form_data.get("cidade_id")),
            pessoa_id=imovel.pessoa_id,
            nome_cidade=imovel.nome_cidade, 
            estado=imovel.estado, 
            nome_corretor=imovel.nome_corretor,  
            imagem_corretor=imovel.imagem_corretor  
        )

        imovel_alterado = ImovelRepo.alterar(alterar_imovel)
        if not imovel_alterado:
            raise HTTPException(status_code=400)

    except KeyError as e:
        raise HTTPException(status_code=400, detail=f"Campo obrigatório ausente: {e}")
    except Exception as e:
        print(f"Ocorreu uma exceção não tratada: {type(e).__name__}: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro interno durante a atualização do imóvel.")

    return RedirectResponse(url="/imoveis", status_code=status.HTTP_303_SEE_OTHER)

@router.post("/trocar_senha")
async def post_trocar_senha(
    request: Request,
    pessoa_logada: Pessoa = Depends(obter_pessoa_logada)
):
    checar_autorizacao(pessoa_logada)

    form_data = await request.form()
    dados = {key: form_data[key] for key in form_data}

    try:
        senha_atual = dados.get("senha_atual")
        nova_senha = dados.get("nova_senha")
        confirmar_nova_senha = dados.get("confirmar_nova_senha")

        if not conferir_senha(senha_atual, pessoa_logada.senha):
            error_message = "Senha atual incorreta!"
            return RedirectResponse(url=f"/perfil?{urlencode({'error': error_message})}", status_code=status.HTTP_303_SEE_OTHER)

        if nova_senha != confirmar_nova_senha:
            error_message = "A nova senha e a confirmação não coincidem!"
            return RedirectResponse(url=f"/perfil?{urlencode({'error': error_message})}", status_code=status.HTTP_303_SEE_OTHER)

        nova_senha_hash = obter_hash_senha(nova_senha)
        PessoaRepo.alterar_senha(pessoa_logada.id, nova_senha_hash)

    except KeyError as e:
        error_message = f"Campo obrigatório ausente: {e}"
        return RedirectResponse(url=f"/perfil?{urlencode({'error': error_message})}", status_code=status.HTTP_303_SEE_OTHER)

    message = "Senha alterada com sucesso!"
    return RedirectResponse(url=f"/perfil?{urlencode({'error': message})}", status_code=status.HTTP_303_SEE_OTHER)

@router.post("/excluir", response_class=JSONResponse)
async def excluir_imovel(id_imovel: int = Form(...), pessoa_logada: Pessoa = Depends(obter_pessoa_logada)):
    checar_autorizacao(pessoa_logada)
    
    try:
        imovel = ImovelRepo.obter_um(id_imovel)
        if not imovel:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Imóvel não encontrado.")
        
        if imovel.pessoa_id != pessoa_logada.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Você não tem permissão para excluir este imóvel.")
        
        if ImovelRepo.excluir(id_imovel):
            response = RedirectResponse(url="/imoveis", status_code=status.HTTP_303_SEE_OTHER)
            adicionar_mensagem_sucesso(response, "Imóvel excluído com sucesso.")
            return response
        else:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Falha ao excluir o imóvel.")
    except HTTPException as e:
        raise e
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Erro interno ao excluir o imóvel: {ex}")

@router.get("/sair", response_class=RedirectResponse)
async def get_sair(request: Request, pessoa_logada: Pessoa = Depends(obter_pessoa_logada)):
    checar_autorizacao(pessoa_logada)
    if pessoa_logada:
        PessoaRepo.alterar_token(pessoa_logada.email, "")
    response = RedirectResponse("/", status.HTTP_303_SEE_OTHER)
    response.set_cookie(key="auth_token", value=" ", httponly=True, expires=0)
    adicionar_mensagem_sucesso(response, "Saída realizada com sucesso.")
    return response