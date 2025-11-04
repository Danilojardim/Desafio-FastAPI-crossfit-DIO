from datetime import datetime
from uuid import uuid4
from typing import Optional

from fastapi import APIRouter, Body, HTTPException, status, Query
from pydantic import UUID4
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from sqlalchemy.exc import IntegrityError

from fastapi_pagination import Page, add_pagination, paginate

from workout_api.atleta.schemas import AtletaIn, AtletaOut, AtletaUpdate
from workout_api.atleta.models import AtletaModel
from workout_api.categorias.models import CategoriaModel
from workout_api.centro_treinamento.models import CentroTreinamentoModel
from workout_api.contrib.dependencies import DatabaseDependency

router = APIRouter()

# ==========================================================
# ✅ POST - Criar novo atleta (com tratamento de duplicidade)
# ==========================================================
@router.post(
    '/',
    summary='Criar um novo atleta',
    status_code=status.HTTP_201_CREATED,
    response_model=AtletaOut
)
async def post(
    db_session: DatabaseDependency,
    atleta_in: AtletaIn = Body(...)
):
    categoria_nome = atleta_in.categoria.nome
    centro_treinamento_nome = atleta_in.centro_treinamento.nome

    categoria = (await db_session.execute(
        select(CategoriaModel).filter_by(nome=categoria_nome))
    ).scalars().first()

    if not categoria:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'A categoria {categoria_nome} não foi encontrada.'
        )

    centro_treinamento = (await db_session.execute(
        select(CentroTreinamentoModel).filter_by(nome=centro_treinamento_nome))
    ).scalars().first()

    if not centro_treinamento:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'O centro de treinamento {centro_treinamento_nome} não foi encontrado.'
        )

    try:
        atleta_out = AtletaOut(id=uuid4(), created_at=datetime.utcnow(), **atleta_in.model_dump())
        atleta_model = AtletaModel(**atleta_out.model_dump(exclude={'categoria', 'centro_treinamento'}))

        atleta_model.categoria_id = categoria.pk_id
        atleta_model.centro_treinamento_id = centro_treinamento.pk_id

        db_session.add(atleta_model)
        await db_session.commit()

    except IntegrityError:
        await db_session.rollback()
        raise HTTPException(
            status_code=status.HTTP_303_SEE_OTHER,
            detail=f"Já existe um atleta cadastrado com o CPF: {atleta_in.cpf}"
        )

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Ocorreu um erro ao inserir os dados no banco.'
        )

    return atleta_out


# ==========================================================
# ✅ GET ALL - com filtros, resposta customizada e paginação
# ==========================================================
@router.get(
    '/',
    summary='Consultar todos os Atletas (com filtros e paginação)',
    status_code=status.HTTP_200_OK,
    response_model=Page[dict],
)
async def query(
    db_session: DatabaseDependency,
    nome: Optional[str] = Query(default=None, description="Filtrar por nome (contém)"),
    cpf: Optional[str] = Query(default=None, description="Filtrar por CPF (igual)")
):
    # Carregar relações de categoria e centro_treinamento
    stmt = select(AtletaModel).options(
        joinedload(AtletaModel.categoria),
        joinedload(AtletaModel.centro_treinamento)
    )

    # Aplicar filtros opcionais
    if nome:
        stmt = stmt.where(AtletaModel.nome.ilike(f"%{nome}%"))
    if cpf:
        stmt = stmt.where(AtletaModel.cpf == cpf)

    atletas = (await db_session.execute(stmt)).scalars().all()

    # Customizar retorno: apenas os campos solicitados
    response = [
        {
            "nome": atleta.nome,
            "categoria": atleta.categoria.nome if atleta.categoria else None,
            "centro_treinamento": atleta.centro_treinamento.nome if atleta.centro_treinamento else None
        }
        for atleta in atletas
    ]

    # Paginação aplicada na lista customizada
    return paginate(response)


# ==========================================================
# ✅ GET BY ID
# ==========================================================
@router.get(
    '/{id}',
    summary='Consulta um Atleta pelo id',
    status_code=status.HTTP_200_OK,
    response_model=AtletaOut,
)
async def get(id: UUID4, db_session: DatabaseDependency) -> AtletaOut:
    atleta: AtletaOut = (
        await db_session.execute(select(AtletaModel).filter_by(id=id))
    ).scalars().first()

    if not atleta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Atleta não encontrado no id: {id}'
        )

    return atleta


# ==========================================================
# ✅ PATCH - Atualizar atleta
# ==========================================================
@router.patch(
    '/{id}',
    summary='Editar um Atleta pelo id',
    status_code=status.HTTP_200_OK,
    response_model=AtletaOut,
)
async def patch(id: UUID4, db_session: DatabaseDependency, atleta_up: AtletaUpdate = Body(...)) -> AtletaOut:
    atleta: AtletaOut = (
        await db_session.execute(select(AtletaModel).filter_by(id=id))
    ).scalars().first()

    if not atleta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Atleta não encontrado no id: {id}'
        )

    atleta_update = atleta_up.model_dump(exclude_unset=True)
    for key, value in atleta_update.items():
        setattr(atleta, key, value)

    await db_session.commit()
    await db_session.refresh(atleta)

    return atleta


# ==========================================================
# ✅ DELETE - Remover atleta
# ==========================================================
@router.delete(
    '/{id}',
    summary='Deletar um Atleta pelo id',
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete(id: UUID4, db_session: DatabaseDependency) -> None:
    atleta: AtletaOut = (
        await db_session.execute(select(AtletaModel).filter_by(id=id))
    ).scalars().first()

    if not atleta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Atleta não encontrado no id: {id}'
        )

    await db_session.delete(atleta)
    await db_session.commit()


# ==========================================================
# ✅ Registrar paginação global
# ==========================================================
add_pagination(router)
