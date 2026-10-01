#!/usr/bin/env python3
"""
device_lock.py — a tiny, file-based lock so the same project checkout
isn't edited from two machines at once (e.g. a cloud-synced folder, or
you forgot to `git push` before switching computers).

Local and gitignored on purpose: this is about "this checkout, right
now," not repo ownership. Cross-machine handoff for work that's already
committed happens through git itself + docs/ai/HANDOFF.md, not this file.

No dependencies beyond the standard library.

Usage:
    python scripts/device_lock.py status
    python scripts/device_lock.py acquire --device "TD-laptop" [--note "..."] [--ttl 240]
    python scripts/device_lock.py renew --device "TD-laptop"
    python scripts/device_lock.py release --device "TD-laptop" [--force]
"""

from __future__ import annotations

import argparse
import json
import socket
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

LOCK_PATH = Path(__file__).resolve().parent.parent / ".device-lock.json"
DEFAULT_TTL_MINUTES = 240  # longer default than a same-machine agent lock —
                            # cross-machine sessions run longer between checks


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _read_lock() -> dict | None:
    if not LOCK_PATH.exists():
        return None
    try:
        return json.loads(LOCK_PATH.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None


def _is_expired(lock: dict) -> bool:
    try:
        started = datetime.fromisoformat(lock["started_at"])
        ttl = timedelta(minutes=lock.get("ttl_minutes", DEFAULT_TTL_MINUTES))
    except (KeyError, ValueError):
        return True
    return _now() > started + ttl


def cmd_status(_args: argparse.Namespace) -> int:
    lock = _read_lock()
    if lock is None:
        print("unlocked")
        return 0
    expired = _is_expired(lock)
    state = "EXPIRED (stale)" if expired else "ACTIVE"
    print(f"{state} — device={lock.get('device')} host={lock.get('host')} "
          f"started={lock.get('started_at')} ttl={lock.get('ttl_minutes')}m")
    if lock.get("note"):
        print(f"  note: {lock['note']}")
    return 1 if not expired else 0


def cmd_acquire(args: argparse.Namespace) -> int:
    existing = _read_lock()
    if existing is not None and not _is_expired(existing) and existing.get("device") != args.device:
        print(f"BLOCKED — locked by '{existing.get('device')}' since {existing.get('started_at')} "
              f"({existing.get('note', 'no note')}). Read docs/ai/HANDOFF.md before proceeding — "
              f"that device may not have pushed yet.", file=sys.stderr)
        return 1

    lock = {
        "device": args.device,
        "host": socket.gethostname(),
        "started_at": _now().isoformat(),
        "ttl_minutes": args.ttl,
        "note": args.note or "",
    }
    LOCK_PATH.write_text(json.dumps(lock, indent=2) + "\n", encoding="utf-8")
    print(f"locked by {args.device} (ttl {args.ttl}m)")
    return 0


def cmd_renew(args: argparse.Namespace) -> int:
    lock = _read_lock()
    if lock is None or lock.get("device") != args.device:
        print("nothing to renew — no active lock held by this device", file=sys.stderr)
        return 1
    lock["started_at"] = _now().isoformat()
    LOCK_PATH.write_text(json.dumps(lock, indent=2) + "\n", encoding="utf-8")
    print(f"renewed lock for {args.device}")
    return 0


def cmd_release(args: argparse.Namespace) -> int:
    lock = _read_lock()
    if lock is None:
        print("already unlocked")
        return 0
    if lock.get("device") != args.device and not args.force:
        print(f"BLOCKED — lock is held by '{lock.get('device')}', not '{args.device}'. "
              f"Pass --force to release it anyway.", file=sys.stderr)
        return 1
    LOCK_PATH.unlink(missing_ok=True)
    print("unlocked")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("status", help="show current lock state").set_defaults(func=cmd_status)

    p_acquire = sub.add_parser("acquire", help="take the lock")
    p_acquire.add_argument("--device", required=True, help="free-text device name, e.g. 'TD-laptop', 'Blender-desktop'")
    p_acquire.add_argument("--note", default="")
    p_acquire.add_argument("--ttl", type=int, default=DEFAULT_TTL_MINUTES)
    p_acquire.set_defaults(func=cmd_acquire)

    p_renew = sub.add_parser("renew", help="push the TTL out from now")
    p_renew.add_argument("--device", required=True)
    p_renew.set_defaults(func=cmd_renew)

    p_release = sub.add_parser("release", help="drop the lock")
    p_release.add_argument("--device", required=True)
    p_release.add_argument("--force", action="store_true")
    p_release.set_defaults(func=cmd_release)

    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
