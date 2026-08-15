"""Credit-event application service."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from .db import LedgerRepository


@dataclass(frozen=True)
class CreditEvent:
    event_id: str
    account_id: str
    amount_cents: int
    currency: str = "EUR"


Checkpoint = Callable[[str], None]


def process_credit(
    repository: LedgerRepository,
    event: CreditEvent,
    checkpoint: Checkpoint | None = None,
) -> str:
    if event.currency != "EUR":
        raise ValueError("Ledgerbox supports EUR credits only")

    with repository.transaction():
        if repository.has_processed(event.event_id):
            return "duplicate"

        repository.append_credit(
            event.event_id,
            event.account_id,
            event.amount_cents,
            event.currency,
        )

        if checkpoint is not None:
            checkpoint("after_credit")

        repository.mark_processed(event.event_id)
    return "applied"
