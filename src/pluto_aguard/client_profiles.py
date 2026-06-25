"""Client HITL profiles for severity adjustment.

Different MCP clients have different built-in security behaviors.
Claude Desktop, Cursor, and VS Code Copilot prompt for approval before
executing dangerous tool calls. Custom or unknown clients may not.

When a known HITL-enforcing client is specified, findings for dangerous
server packages are downgraded from CRITICAL/HIGH to MEDIUM since the
client itself provides an approval gate.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class ClientProfile:
    """Describes an MCP client's built-in security capabilities."""

    name: str
    display_name: str
    has_hitl: bool  # Client prompts user before dangerous tool calls
    description: str
    downgrade_ids: frozenset[str] = field(default_factory=frozenset)


# Known client profiles
_CLIENT_PROFILES: dict[str, ClientProfile] = {
    "claude-desktop": ClientProfile(
        name="claude-desktop",
        display_name="Claude Desktop",
        has_hitl=True,
        description="Claude Desktop prompts for user approval before executing tool calls.",
        downgrade_ids=frozenset({"DANGEROUS-PKG", "DANGEROUS-POPULAR"}),
    ),
    "cursor": ClientProfile(
        name="cursor",
        display_name="Cursor",
        has_hitl=True,
        description="Cursor prompts for user approval on tool calls in agent mode.",
        downgrade_ids=frozenset({"DANGEROUS-PKG", "DANGEROUS-POPULAR"}),
    ),
    "vscode-copilot": ClientProfile(
        name="vscode-copilot",
        display_name="VS Code Copilot",
        has_hitl=True,
        description="VS Code Copilot agent mode requires user confirmation for tool calls.",
        downgrade_ids=frozenset({"DANGEROUS-PKG", "DANGEROUS-POPULAR"}),
    ),
    "custom": ClientProfile(
        name="custom",
        display_name="Custom / Unknown",
        has_hitl=False,
        description="No HITL assumption — conservative severity ratings.",
    ),
}

# Default when no --client is specified: assume no HITL (conservative)
DEFAULT_CLIENT = "custom"


def get_client_profile(client_name: str | None) -> ClientProfile | None:
    """Get a client profile by name. Returns None if no client specified."""
    if client_name is None:
        return None
    return _CLIENT_PROFILES.get(client_name)


def list_client_names() -> list[str]:
    """Return all valid client profile names."""
    return sorted(_CLIENT_PROFILES.keys())


def should_downgrade(finding_id: str, profile: ClientProfile) -> bool:
    """Check if a finding should be downgraded for this client profile."""
    if not profile.has_hitl:
        return False
    return any(finding_id.startswith(prefix) for prefix in profile.downgrade_ids)
