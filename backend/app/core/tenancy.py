"""Contexto de estúdio (tenant) para RLS.

O contexto é `app.studio_id`, aplicado com `set_config(..., true)` (equivale a
`SET LOCAL`): vale só na transação corrente e é zerado no commit/rollback. Por isso
é reaplicado a cada início de transação da sessão (evento `after_begin`).
Valores sempre via bind e validados como UUID; nunca interpolados em SQL.
"""
from uuid import UUID

from sqlalchemy import event, text
from sqlalchemy.engine import Connection
from sqlalchemy.orm import Session as ORMSession
from sqlalchemy.orm import SessionTransaction

_INFO_KEY = "pics.studio_id"
_SET_CONTEXT = text("SELECT set_config('app.studio_id', :studio_id, true)")


def _apply(connection: Connection, studio_id: UUID) -> None:
    connection.execute(_SET_CONTEXT, {"studio_id": str(studio_id)})


@event.listens_for(ORMSession, "after_begin")
def _reapply_studio_context(
    session: ORMSession, transaction: SessionTransaction, connection: Connection
) -> None:
    studio_id = session.info.get(_INFO_KEY)
    if studio_id is not None:
        _apply(connection, studio_id)


def set_studio_context(session: ORMSession, studio_id: UUID) -> None:
    """Fixa o estúdio da sessão (aceita só `uuid.UUID`) e aplica já, se houver
    transação aberta; as próximas transações reaplicam sozinhas."""
    if not isinstance(studio_id, UUID):
        raise TypeError("studio_id must be a uuid.UUID")
    session.info[_INFO_KEY] = studio_id
    if session.in_transaction():
        _apply(session.connection(), studio_id)


def clear_studio_context(session: ORMSession) -> None:
    """Remove o estúdio da sessão e zera o contexto da transação corrente."""
    session.info.pop(_INFO_KEY, None)
    if session.in_transaction():
        session.connection().execute(
            text("SELECT set_config('app.studio_id', '', true)")
        )


def resolve_user_studios(session: ORMSession, user_id: UUID) -> list[tuple[UUID, str]]:
    """Estúdios ativos do usuário (função definer, pré-contexto). `user_id` deve
    vir da sessão autenticada, nunca do cliente."""
    rows = session.execute(
        text("SELECT studio_id, role FROM public.resolve_user_studios(:user_id)"),
        {"user_id": user_id},
    ).all()
    return [(row[0], row[1]) for row in rows]


def create_studio(
    session: ORMSession, name: str, slug: str, owner_user_id: UUID
) -> UUID:
    """Cria o estúdio e o vínculo `studio_owner` de forma atômica (função definer)."""
    studio_id = session.execute(
        text("SELECT public.create_studio(:name, :slug, :owner)"),
        {"name": name, "slug": slug, "owner": owner_user_id},
    ).scalar_one()
    if not isinstance(studio_id, UUID):
        raise RuntimeError("create_studio did not return a uuid")
    return studio_id
