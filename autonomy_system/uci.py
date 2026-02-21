#!/usr/bin/env python3
"""Universal Chain Intelligence - Entry Point"""

from __future__ import annotations

import argparse
import json

from autonomy_system import config as default_config
from autonomy_system.main import build_core, setup_logging
from autonomy_system.models.goal_record import GoalSource
from autonomy_system.runtime.daemon_manager import DaemonManager


class UCI:
    """The Universal Chain Intelligence System."""

    def __init__(self, config: dict = None):
        self.config = config or default_config
        self.core = None
        self.daemon = None

    def _ensure_core(self):
        if self.core is None:
            setup_logging()
            self.core = build_core()

    def start(self, autonomy_level: str = "guided", daemon: bool = False) -> None:
        self._ensure_core()
        self.set_autonomy(autonomy_level)
        if daemon:
            self.daemon = DaemonManager(self.core, self.config)
            self.daemon.start_daemon()
        print(f"{self.config.SYSTEM_NAME} started at autonomy={autonomy_level}")

    def stop(self) -> None:
        if self.daemon:
            self.daemon.stop_daemon()
        if self.core:
            self.core.shutdown(True)
        print("UCI stopped")

    def submit_goal(self, goal: str, priority: int = 50) -> dict:
        self._ensure_core()
        record = self.core.submit_goal(goal, GoalSource.EXTERNAL_API, priority)
        result = self.core.goal_manager.process_next()
        return {
            "record_id": record.record_id,
            "status": result.status.value if result else "QUEUED",
            "result": result.result if result else None,
        }

    def get_status(self) -> dict:
        self._ensure_core()
        return self.core.get_status().__dict__

    def get_capabilities(self) -> list:
        self._ensure_core()
        return self.core.get_capabilities()

    def ask(self, question: str) -> str:
        self._ensure_core()
        return self.core.consciousness.answer_question(question)

    def set_autonomy(self, level: str) -> None:
        self._ensure_core()
        self.core.set_autonomy_level(level)


def main():
    parser = argparse.ArgumentParser(prog="uci", description="Universal Chain Intelligence")
    sub = parser.add_subparsers(dest="command")

    p_start = sub.add_parser("start")
    p_start.add_argument("--autonomy", default=default_config.DEFAULT_AUTONOMY_LEVEL)
    p_start.add_argument("--daemon", action="store_true")
    p_start.add_argument("--port", type=int, default=default_config.HTTP_PORT)

    p_goal = sub.add_parser("goal")
    p_goal.add_argument("goal")
    p_goal.add_argument("--priority", type=int, default=50)

    sub.add_parser("status")
    sub.add_parser("capabilities")

    p_ask = sub.add_parser("ask")
    p_ask.add_argument("question")

    sub.add_parser("stop")
    sub.add_parser("version")

    args = parser.parse_args()
    uci = UCI()

    if args.command == "start":
        uci.start(args.autonomy, args.daemon)
    elif args.command == "goal":
        print(json.dumps(uci.submit_goal(args.goal, args.priority), indent=2))
    elif args.command == "status":
        print(json.dumps(uci.get_status(), indent=2, default=str))
    elif args.command == "capabilities":
        print(json.dumps(uci.get_capabilities(), indent=2, default=str))
    elif args.command == "ask":
        print(uci.ask(args.question))
    elif args.command == "stop":
        uci.stop()
    elif args.command == "version":
        print(default_config.SYSTEM_VERSION)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
