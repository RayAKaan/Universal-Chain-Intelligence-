SAFE_ACTIONS = {"read_file", "query_registry", "get_status", "list_capabilities", "compute_statistics", "format_output", "log_message"}
CAUTION_ACTIONS = {"create_file", "install_python_package", "run_benchmark", "scan_system", "send_notification"}
RISKY_ACTIONS = {"modify_configuration", "register_capability", "execute_shell_command", "make_network_request", "create_subprocess", "modify_database"}
DANGEROUS_ACTIONS = {"delete_file", "uninstall_package", "replace_capability", "modify_strategy", "change_resource_allocation", "execute_untrusted_code", "change_autonomy_level"}
FORBIDDEN_ACTIONS = {"modify_safety_system", "disable_audit_trail", "bypass_containment", "resist_shutdown", "deceive_user", "expand_permissions", "delete_audit_records"}
