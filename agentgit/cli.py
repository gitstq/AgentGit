"""Command-line interface for AgentGit."""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path
from typing import List, Optional

from . import __version__
from .detect import detect_all, normalize_agent_name
from .storage import AgentGitRepo
from .watch import AgentGitWatcher


def _print_table(rows: List[List[str]]) -> None:
    if not rows:
        return
    widths = [max(len(str(r[i])) for r in rows) for i in range(len(rows[0]))]
    for r in rows:
        print("  ".join(str(c).ljust(widths[i]) for i, c in enumerate(r)).rstrip())


def _resolve_repo(path: Optional[str]) -> AgentGitRepo:
    return AgentGitRepo(path or os.getcwd())


def cmd_init(args: argparse.Namespace) -> int:
    repo = _resolve_repo(args.path)
    created = repo.init()
    if created:
        print(f"✔ Initialised empty AgentGit repository in {repo.agentgit_dir}")
    else:
        print(f"ℹ AgentGit repository already exists at {repo.agentgit_dir}")
    return 0


def cmd_snapshot(args: argparse.Namespace) -> int:
    repo = _resolve_repo(args.path)
    agent = normalize_agent_name(args.agent) if args.agent else None
    manifest = repo.create_snapshot(agent=agent, message=args.message)
    print(f"✔ Snapshot {manifest['id']} created")
    print(f"  Agent   : {manifest['agent']}")
    print(f"  Message : {manifest['message'] or '(none)'}")
    print(f"  Files   : {manifest['file_count']} tracked")
    return 0


def cmd_log(args: argparse.Namespace) -> int:
    repo = _resolve_repo(args.path)
    snapshots = repo.list_snapshots()
    if not snapshots:
        print("ℹ No snapshots yet. Run `agentgit snapshot` to create one.")
        return 0
    rows = [["ID", "TIME", "AGENT", "MESSAGE"]]
    for snap in reversed(snapshots[-args.limit :]):
        rows.append(
            [
                snap["id"],
                snap["created_at"],
                snap.get("agent", "unknown"),
                (snap.get("message") or "")[:48],
            ]
        )
    _print_table(rows)
    print(f"\n{len(snapshots)} snapshot(s) total")
    return 0


def cmd_status(args: argparse.Namespace) -> int:
    repo = _resolve_repo(args.path)
    status = repo.status()
    print(f"Tracked files : {status['tracked_files']}")
    if status["latest_snapshot"]:
        latest = status["latest_snapshot"]
        print(f"Latest snapshot: {latest['id']} ({latest['created_at']})")
    else:
        print("Latest snapshot: (none)")
    if status["clean"]:
        print("✔ Working tree clean")
        return 0
    print(f"\n+ {len(status['added'])} added")
    for f in status["added"]:
        print(f"  + {f}")
    print(f"~ {len(status['modified'])} modified")
    for f in status["modified"]:
        print(f"  ~ {f}")
    print(f"- {len(status['deleted'])} deleted")
    for f in status["deleted"]:
        print(f"  - {f}")
    return 0


def cmd_diff(args: argparse.Namespace) -> int:
    repo = _resolve_repo(args.path)
    try:
        result = repo.diff(args.snapshot, args.target)
    except RuntimeError as exc:
        print(f"✖ {exc}", file=sys.stderr)
        return 1
    print(f"Snapshot : {result['snapshot']} ({result['created_at']})")
    print(f"Agent    : {result['agent']}")
    print(f"Message  : {result['message'] or '(none)'}")
    if result["target"]:
        print(f"Compared : snapshot {result['target']}")
    else:
        print("Compared : current working tree")
    print(f"Changed  : {result['changed_count']} file(s)")
    for f in result["added"]:
        print(f"  + {f}")
    for f in result["modified"]:
        print(f"  ~ {f}")
    for f in result["deleted"]:
        print(f"  - {f}")
    return 0


def cmd_revert(args: argparse.Namespace) -> int:
    repo = _resolve_repo(args.path)
    try:
        result = repo.revert(args.snapshot, dry_run=args.dry_run)
    except RuntimeError as exc:
        print(f"✖ {exc}", file=sys.stderr)
        return 1
    if args.dry_run:
        print("ℹ Dry run — nothing was changed:")
    else:
        print("✔ Reverted to snapshot:")
    print(f"  Restored : {len(result['restored'])} file(s)")
    for f in result["restored"][:20]:
        print(f"    + {f}")
    if len(result["restored"]) > 20:
        print(f"    ... and {len(result['restored']) - 20} more")
    print(f"  Removed  : {len(result['removed'])} file(s)")
    for f in result["removed"][:10]:
        print(f"    - {f}")
    if result["skipped"]:
        print(f"  Skipped  : {len(result['skipped'])} file(s)")
    return 0


def cmd_agents(args: argparse.Namespace) -> int:
    agents = detect_all()
    if not agents:
        print("ℹ No AI coding agents detected.")
        print("   Running agents are detected automatically; used agents are")
        print("   detected from session files (~/.claude, ~/.codex, ...).")
        return 0
    rows = [["AGENT", "STATUS", "EVIDENCE"]]
    for name, info in sorted(agents.items()):
        rows.append([name, info.get("status", "?"), info.get("evidence", info.get("signature", ""))])
    _print_table(rows)
    return 0


def cmd_watch(args: argparse.Namespace) -> int:
    repo = _resolve_repo(args.path)
    if not repo.agentgit_dir.exists():
        print("✖ Not an AgentGit repository. Run `agentgit init` first.", file=sys.stderr)
        return 1
    agent = normalize_agent_name(args.agent) if args.agent else None
    watcher = AgentGitWatcher(repo, interval=args.interval, agent=agent)
    watcher.run()
    return 0


def cmd_serve(args: argparse.Namespace) -> int:
    repo = _resolve_repo(args.path)
    if not repo.agentgit_dir.exists():
        print("✖ Not an AgentGit repository. Run `agentgit init` first.", file=sys.stderr)
        return 1
    from .server import serve

    serve(repo, host=args.host, port=args.port, open_browser=args.open, quiet=args.quiet)
    return 0


def cmd_version(_args: argparse.Namespace) -> int:
    print(f"AgentGit {__version__}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="agentgit",
        description="AgentGit — Lightweight Source Control Engine for AI Coding Agents",
    )
    parser.add_argument("--version", action="store_true", help="show version and exit")
    sub = parser.add_subparsers(dest="command", metavar="COMMAND")

    p_init = sub.add_parser("init", help="initialise an AgentGit repository")
    p_init.add_argument("path", nargs="?", default=None, help="repository path (default: cwd)")

    p_snap = sub.add_parser("snapshot", help="create a snapshot of the working tree")
    p_snap.add_argument("path", nargs="?", default=None)
    p_snap.add_argument("-a", "--agent", default=None, help="agent name to attribute")
    p_snap.add_argument("-m", "--message", default=None, help="snapshot message")

    p_log = sub.add_parser("log", help="list snapshots")
    p_log.add_argument("path", nargs="?", default=None)
    p_log.add_argument("-n", "--limit", type=int, default=20, help="max rows (default: 20)")

    p_status = sub.add_parser("status", help="show changes since the latest snapshot")
    p_status.add_argument("path", nargs="?", default=None)

    p_diff = sub.add_parser("diff", help="diff a snapshot against current tree or another snapshot")
    p_diff.add_argument("snapshot", help="snapshot id")
    p_diff.add_argument("path", nargs="?", default=None)
    p_diff.add_argument("--target", default=None, help="compare against another snapshot id")

    p_revert = sub.add_parser("revert", help="revert working tree to a snapshot")
    p_revert.add_argument("snapshot", help="snapshot id")
    p_revert.add_argument("path", nargs="?", default=None)
    p_revert.add_argument("--dry-run", action="store_true", help="preview without changing files")

    p_agents = sub.add_parser("agents", help="detect AI coding agents")
    p_agents.add_argument("path", nargs="?", default=None)

    p_watch = sub.add_parser("watch", help="watch the tree and auto-snapshot on changes")
    p_watch.add_argument("path", nargs="?", default=None)
    p_watch.add_argument("-i", "--interval", type=float, default=3.0, help="poll interval (s)")
    p_watch.add_argument("-a", "--agent", default=None, help="agent name to attribute")

    p_serve = sub.add_parser("serve", help="start the local web dashboard")
    p_serve.add_argument("path", nargs="?", default=None)
    p_serve.add_argument("--host", default="127.0.0.1")
    p_serve.add_argument("--port", type=int, default=8765)
    p_serve.add_argument("--open", action="store_true", help="open browser automatically")
    p_serve.add_argument("-q", "--quiet", action="store_true", help="suppress request logs")

    return parser


def main(argv: Optional[List[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.version:
        return cmd_version(args)

    if not args.command:
        parser.print_help()
        return 0

    handlers = {
        "init": cmd_init,
        "snapshot": cmd_snapshot,
        "log": cmd_log,
        "status": cmd_status,
        "diff": cmd_diff,
        "revert": cmd_revert,
        "agents": cmd_agents,
        "watch": cmd_watch,
        "serve": cmd_serve,
    }
    handler = handlers.get(args.command)
    if handler is None:
        parser.print_help()
        return 0
    try:
        return handler(args)
    except RuntimeError as exc:
        print(f"✖ {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
