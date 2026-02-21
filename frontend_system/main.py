from __future__ import annotations

import argparse
import logging
from logging.handlers import RotatingFileHandler
import signal
import sys
import time
import webbrowser
from threading import Event, Thread
from datetime import datetime, timezone

from frontend_system import config
from frontend_system.integration.uci_connector import UCIConnector
from frontend_system.integration.realtime_feed import RealtimeFeed
from frontend_system.server.web_server import UCIWebServer


def _setup_logging():
    import os
    os.makedirs('logs', exist_ok=True)
    root = logging.getLogger()
    root.setLevel(getattr(logging, config.LOG_LEVEL, logging.INFO))
    root.handlers.clear()
    fmt = logging.Formatter('%(asctime)s | %(name)s | %(levelname)s | %(message)s')
    ch = logging.StreamHandler(); ch.setFormatter(fmt); ch.setLevel(logging.INFO)
    fh = RotatingFileHandler(config.LOG_FILE, maxBytes=5_000_000, backupCount=3); fh.setFormatter(fmt)
    root.addHandler(ch); root.addHandler(fh)


def _simulate_activity(connector: UCIConnector, feed: RealtimeFeed, stop: Event):
    while not stop.is_set():
        for g in connector.goals[:1]:
            if g['status'] in ('queued', 'active'):
                g['status'] = 'active'
                g['progress'] = min(100, g.get('progress', 0) + 10)
                if g['progress'] >= 100:
                    g['status'] = 'completed'
                evt = {'goal_id': g['record_id'], 'status': g['status'], 'progress': g['progress'], 'timestamp': datetime.now(timezone.utc).isoformat()}
                connector.timeline.append({'id': g['record_id'], 'phase': 'phase5', 'event_type': 'GOAL_PROGRESS', 'timestamp': evt['timestamp'], 'details': str(evt)})
                feed.push_event('GOAL_PROGRESS', evt)
        time.sleep(3)


def run(mode: str):
    _setup_logging()
    connector = UCIConnector(None if mode == 'standalone' else None)
    feed = RealtimeFeed()
    server = UCIWebServer(config.HOST, config.PORT, connector, config)
    server.start()

    stop = Event()
    sim_thread = Thread(target=_simulate_activity, args=(connector, feed, stop), daemon=True)
    sim_thread.start()

    print('╔══════════════════════════════════════════╗')
    print('║  Universal Chain Intelligence Frontend   ║')
    print(f'║  Dashboard: http://localhost:{config.PORT}        ║')
    print(f'║  API: http://localhost:{config.PORT}/api          ║')
    print('╚══════════════════════════════════════════╝')

    try:
        webbrowser.open(f'http://localhost:{config.PORT}')
    except Exception:
        pass

    def shutdown(*_):
        stop.set()
        server.stop()
        sys.exit(0)

    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGTERM, shutdown)

    while True:
        time.sleep(1)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--standalone', action='store_true')
    parser.add_argument('--connect', action='store_true')
    args = parser.parse_args()
    mode = 'connect' if args.connect else 'standalone'
    run(mode)


if __name__ == '__main__':
    main()
