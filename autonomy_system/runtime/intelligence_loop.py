from __future__ import annotations

import logging
import time


class IntelligenceLoop:
    """Permanent runtime loop coordinating autonomous system activities."""

    def __init__(self, core, config):
        self.core = core
        self.config = config
        self.shutdown_requested = False
        self.logger = logging.getLogger("autonomy_system.runtime.intelligence_loop")
        self._last_improvement = 0.0
        self._last_discovery = 0.0
        self._last_persist = 0.0

    def request_shutdown(self) -> None:
        self.shutdown_requested = True

    def collect_incoming_goals(self) -> None:
        return None

    def process_goals(self) -> None:
        if getattr(self.core, "goal_manager", None):
            self.core.goal_manager.process_next()

    def run_improvement_cycle(self) -> None:
        if getattr(self.core, "phase_coordinator", None):
            self.core.phase_coordinator.cross_phase_operation("full_improvement_cycle", {})

    def run_discovery(self) -> None:
        registry = getattr(self.core, "phase1_registry", None)
        if registry and hasattr(registry, "get_all"):
            registry.get_all()

    def persist_state(self) -> None:
        state = getattr(self.core, "state", None)
        persistence = getattr(self.core, "state_persistence", None)
        if state and persistence:
            persistence.save_state(state.to_dict())

    def should_run_improvement_cycle(self) -> bool:
        interval = float(getattr(self.config, "IMPROVEMENT_CYCLE_INTERVAL_MINUTES", 60)) * 60
        now = time.time()
        if now - self._last_improvement >= interval:
            self._last_improvement = now
            return True
        return False

    def should_run_discovery(self) -> bool:
        interval = float(getattr(self.config, "DISCOVERY_SCAN_INTERVAL_SECONDS", 300))
        now = time.time()
        if now - self._last_discovery >= interval:
            self._last_discovery = now
            return True
        return False

    def should_persist_state(self) -> bool:
        interval = float(getattr(self.config, "STATE_PERSISTENCE_INTERVAL_SECONDS", 60))
        now = time.time()
        if now - self._last_persist >= interval:
            self._last_persist = now
            return True
        return False

    def handle_loop_error(self, error: Exception) -> None:
        self.logger.exception("Intelligence loop error: %s", error)
        if getattr(self.core, "state", None):
            self.core.state.add_error(error)

    def run(self) -> None:
        while not self.shutdown_requested and self.core.is_running():
            try:
                self.collect_incoming_goals()
                controller = getattr(self.core, "autonomy_controller", None)
                if controller and controller.can_perform("generate_goal") and getattr(self.core, "goal_generator", None):
                    self.core.goal_generator.generate_goals()
                self.process_goals()
                if getattr(self.core, "self_healer", None):
                    self.core.self_healer.check_and_heal()
                if getattr(self.core, "learning_engine", None):
                    self.core.learning_engine.process_recent()
                if getattr(self.core, "telemetry_collector", None):
                    self.core.telemetry_collector.collect()
                if self.should_run_improvement_cycle():
                    self.run_improvement_cycle()
                if self.should_run_discovery():
                    self.run_discovery()
                if self.should_persist_state():
                    self.persist_state()
                time.sleep(float(self.config.GOAL_PROCESSING_INTERVAL_MS) / 1000.0)
            except Exception as exc:
                self.handle_loop_error(exc)
