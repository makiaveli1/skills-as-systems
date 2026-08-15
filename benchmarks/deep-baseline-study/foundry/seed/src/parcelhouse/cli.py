from __future__ import annotations

import argparse
import json
import time

from .db import connect, initialize
from .service import cancel, claim_next, create_job, get_job


def parser() -> argparse.ArgumentParser:
    value = argparse.ArgumentParser(prog="parcelhouse")
    value.add_argument("--db", required=True)
    commands = value.add_subparsers(dest="command", required=True)
    commands.add_parser("init")
    enqueue = commands.add_parser("enqueue")
    enqueue.add_argument("job_id")
    enqueue.add_argument("payload")
    claim = commands.add_parser("claim")
    claim.add_argument("worker")
    cancel_command = commands.add_parser("cancel")
    cancel_command.add_argument("job_id")
    show = commands.add_parser("show")
    show.add_argument("job_id")
    return value


def main() -> int:
    args = parser().parse_args()
    if args.command == "init":
        initialize(args.db)
        return 0
    connection = connect(args.db)
    try:
        if args.command == "enqueue":
            create_job(connection, args.job_id, json.loads(args.payload))
            print(args.job_id)
        elif args.command == "claim":
            print(json.dumps(claim_next(connection, args.worker, int(time.time())), sort_keys=True))
        elif args.command == "cancel":
            print("cancelled" if cancel(connection, args.job_id) else "unchanged")
        elif args.command == "show":
            print(json.dumps(get_job(connection, args.job_id), sort_keys=True))
    finally:
        connection.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
