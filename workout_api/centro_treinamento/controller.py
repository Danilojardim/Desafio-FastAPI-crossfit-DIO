from uuid import uuid4
from fastapi import APIRouter, Body, HTTPException, status
from pydantic import UUID4
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select

from workout_api.centro_treinamento.schemas import CentroTreinamentoIn, CentroTreinamentoOut
from workout_api.centro_treinamento.models import CentroTreinamentoModel
from workout_api.contrib.dependencies import DatabaseDependency

router = APIRouter()

@router.post(
    '/', 
    summary='Criar um novo Centro de Treinamento',
    status_code=status.HTTP_201_CREATED,
    response_model=CentroTreinamentoOut,
)
async def post(
    db_session: DatabaseDependency, 
    centro_in: CentroTreinamentoIn = Body(...)
) -> CentroTreinamentoOut:
    centro_out = CentroTreinamentoOut(id=uuid4(), **centro_in.model_dump())
    centro_model = CentroTreinamentoModel(**centro_out.model_dump())

    try:
        db_session.add(centro_model)
        await db_session.commit()
    except IntegrityError:
        await db_session.rollback()
        raise HTTPException(
            status_code=status.HTTP_303_SEE_OTHER,
            detail=f"Já existe um centro de treinamento cadastrado com o nome: {centro_in.nome}"
        )
    except Exception:
        await db_session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro inesperado ao salvar o centro de treinamento no banco de dados."
        )

    return centro_out


@router.get(
    '/', 
    summary='Consultar todos os Centros de Treinamento',
    status_code=status.HTTP_200_OK,
    response_model=list[CentroTreinamentoOut],
)
async def query(db_session: DatabaseDependency) -> list[CentroTreinamentoOut]:
    centros = (await db_session.execute(select(CentroTreinamentoModel))).scalars().all()
    return [CentroTreinamentoOut.model_validate(centro) for centro in centros]


@router.get(
    '/{id}', 
    summary='Consultar um Centro de Treinamento pelo id',
    status_code=status.HTTP_200_OK,
    response_model=CentroTreinamentoOut,
)
async def get(id: UUID4, db_session: DatabaseDependency) -> CentroTreinamentoOut:
    centro = (
        await db_session.execute(select(CentroTreinamentoModel).filter_by(id=id))
    ).scalars().first()

    if not centro:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f'Centro de Treinamento não encontrado no id: {id}'
        )
    
    return centro
