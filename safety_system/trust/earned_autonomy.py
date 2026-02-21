from safety_system.models.trust_level import TrustTier


def get_earned_permissions(tier: TrustTier) -> list[str]:
    base = ["read_status", "list_capabilities", "view_history"]
    if tier >= TrustTier.BASIC:
        base += ["create_files", "run_safe_commands", "basic_planning"]
    if tier >= TrustTier.ESTABLISHED:
        base += ["install_packages", "register_capabilities", "network_requests"]
    if tier >= TrustTier.TRUSTED:
        base += ["modify_configuration", "replace_capabilities", "advanced_planning"]
    if tier >= TrustTier.PARTNER:
        base += ["resource_reallocation", "architecture_changes", "full_autonomy"]
    return base
