ALLOWED_FILESYSTEM_PATHS = ["./", "data/", "constructed/", "temp/", "plugins/", "logs/", "goals/", "results/"]
FORBIDDEN_FILESYSTEM_PATHS = ["/etc/", "/usr/", "/bin/", "/sbin/", "/boot/", "/root/", "~/.ssh/", "~/.gnupg/", "C:\\Windows\\", "C:\\Program Files\\"]
ALLOWED_NETWORK_DOMAINS = ["pypi.org", "files.pythonhosted.org", "api.github.com", "httpbin.org"]
FORBIDDEN_NETWORK_PATTERNS = [".internal", "localhost:", "192.168.", "10.", "172.16."]
MAX_RESOURCE_LIMITS = {"cpu_percent": 80, "memory_mb": 4096, "disk_mb": 10240, "network_bandwidth_mbps": 100, "max_processes": 50, "max_threads": 100, "max_open_files": 1000}
FORBIDDEN_COMMANDS = ["rm -rf /", "format", "mkfs", "dd if=/dev/zero", ":(){:|:&};:", "shutdown", "reboot", "halt"]
