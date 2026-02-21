from __future__ import annotations

import threading

from autonomy_system.runtime.intelligence_loop import IntelligenceLoop


class DaemonManager:
    def __init__(self, core, config):
        self.core = core
        self.config = config
        self.running = False
        self.loop = IntelligenceLoop(core, config)
        self.thread = None

    def start_daemon(self) -> None:
        if self.running:
            return
        self.running = True
        self.thread = threading.Thread(target=self.main_loop, daemon=True)
        self.thread.start()

    def main_loop(self) -> None:
        self.loop.run()

    def stop_daemon(self) -> None:
        self.running = False
        self.loop.request_shutdown()
        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=2)
