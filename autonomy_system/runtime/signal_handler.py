from __future__ import annotations
import signal
def setup_signal_handlers(on_shutdown,on_reload=None,on_dump=None):
    signal.signal(signal.SIGINT, lambda s,f:on_shutdown())
    signal.signal(signal.SIGTERM, lambda s,f:on_shutdown())
    if hasattr(signal,'SIGHUP') and on_reload: signal.signal(signal.SIGHUP, lambda s,f:on_reload())
    if hasattr(signal,'SIGUSR1') and on_dump: signal.signal(signal.SIGUSR1, lambda s,f:on_dump())
