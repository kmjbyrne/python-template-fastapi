"""Main router entrypoint."""

import logging
from datetime import UTC, datetime, timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request, Response
from pydantic import BaseModel
from sqlmodel import Session, col, select
from starlette import status

from app.adapter.repository.sqlite.models import Ditloid, DitloidBase, GuessModel
from app.dependencies import get_session

router = APIRouter()


class GuessSchema(BaseModel):
    """API schema for encapsulating given guest guesses."""

    solution: str
    guid: str
    guest_guid: str


class DitloidWithGuesses(DitloidBase):
    """Public facing Ditloid with relationships."""

    guess_count: int


def check_ditloid_complete(payload: GuessSchema, session: Annotated[Session, Depends(get_session)]):
    """Verify the Guest has solved or not solved their daily attempt."""
    # in the event a call to the API contains a bad GUID
    ditloid = session.exec(select(Ditloid).where(Ditloid.guid == payload.guid)).one_or_none()
    if not ditloid:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    last_guess = session.exec(
        select(GuessModel).where(
            GuessModel.ditloid_id == ditloid.id,
            GuessModel.guest_guid == payload.guest_guid,
            GuessModel.solved,
        )
    ).first()
    if last_guess and last_guess.solved:
        logging.info("Last guess was the correct solution")
        message = {
            "info": "This Ditloid has already been solved!",
            "solution": last_guess.guess_value,
        }
        session.exec(select(GuessModel).where(GuessModel.guest_guid == payload.guest_guid))
        raise HTTPException(detail=message, status_code=status.HTTP_409_CONFLICT)
    last_guess = session.exec(
        select(GuessModel).where(
            GuessModel.ditloid_id == ditloid.id,
            GuessModel.guest_guid == payload.guest_guid,
            GuessModel.guess_value == payload.solution.strip().lower(),
        )
    ).first()
    if last_guess:
        raise HTTPException(status_code=status.HTTP_418_IM_A_TEAPOT)


@router.post("/check", dependencies=[Depends(check_ditloid_complete)])
def check_guess(
    response: Response,
    request: Request,
    payload: GuessSchema,
    session: Annotated[Session, Depends(get_session)],
):
    """Check the incoming guess against the DB record."""
    ditloid = session.exec(select(Ditloid).where(Ditloid.guid == payload.guid)).one_or_none()
    # Get current time
    now = datetime.now(UTC)
    # Calculate midnight (start of next day)
    midnight = (now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
    if not ditloid:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    guess = GuessModel(
        ditloid_id=ditloid.id,
        guess_value=payload.solution,
        solved=False,
        guest_guid=payload.guest_guid,
    )
    if ditloid.solution.lower().strip() == payload.solution.lower().strip():
        guess.solved = True
        session.add(guess)
        session.commit()
        response.set_cookie("ditloid.status", "true", expires=int((midnight - now).total_seconds()))
        return {"status": True, "data": payload}
    session.add(guess)
    session.commit()
    attempts = int(request.cookies.get("ditloid.attempts", 0)) + 1
    response.set_cookie(
        "ditloid.attempts", str(attempts), expires=int((midnight - now).total_seconds())
    )
    return {"status": False, "data": payload.model_dump(), "attempts": attempts}


@router.get("/")
def get_today_ditloid(session: Annotated[Session, Depends(get_session)]):
    """Get the Ditloid for the day."""
    ditloid = session.exec(
        select(Ditloid).where(Ditloid.schedule == datetime.now(UTC).date())
    ).first()
    return {"data": ditloid.short, "guid": ditloid.guid}


@router.get("/history", response_model=list[DitloidWithGuesses])
def get_previous_ditloids(
    session: Annotated[Session, Depends(get_session)],
):
    """Get all previous Ditloids."""
    return session.exec(
        select(Ditloid)
        .where(Ditloid.schedule < datetime.now().date())
        .order_by(col(Ditloid.schedule).desc())
    ).all()
