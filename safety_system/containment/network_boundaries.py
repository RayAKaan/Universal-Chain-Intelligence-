from urllib.parse import urlparse

from safety_system.scope.boundary_definitions import ALLOWED_NETWORK_DOMAINS, FORBIDDEN_NETWORK_PATTERNS


class NetworkBoundaries:
    def is_allowed(self, url: str, method: str) -> bool:
        host = (urlparse(url).hostname or "").lower()
        if any(p in host for p in FORBIDDEN_NETWORK_PATTERNS):
            return False
        return host in ALLOWED_NETWORK_DOMAINS
