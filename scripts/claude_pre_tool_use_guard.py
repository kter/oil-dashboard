#!/usr/bin/env python3
"""Guard script to block dangerous commands in Claude tool use."""

import json
import re
import sys


DANGEROUS_PATTERNS = [
    (r"\brm\s+.*-[^\s]*r[^\s]*f", "rm -rf (recursive force deletion)"),
    (r"\brm\s+.*-[^\s]*f[^\s]*r", "rm -rf (recursive force deletion)"),
    (r"\bterraform\s+destroy\b", "terraform destroy"),
    (r"\bgit\s+reset\s+--hard\b", "git reset --hard"),
    (r"\bgit\s+clean\s+-[^\s]*f", "git clean -f (force clean)"),
    (r"\bgit\s+push\s+.*--force\b", "git push --force"),
    (r"\bfind\s+.*-delete\b", "find -delete"),
]


def check_command(command: str) -> tuple[bool, str]:
    """Check if a command matches dangerous patterns."""
    # Strip sudo, env, bash -c wrappers
    cleaned = re.sub(r"^(sudo\s+|env\s+\S+=\S+\s+|bash\s+-[a-z]*c\s+['\"]?)", "", command.strip())

    for pattern, description in DANGEROUS_PATTERNS:
        if re.search(pattern, cleaned):
            return False, description
    return True, ""


def main() -> None:
    try:
        payload = json.load(sys.stdin)
        command = payload.get("tool_input", {}).get("command", "")

        if not command:
            print(json.dumps({}))
            return

        allowed, reason = check_command(command)
        if not allowed:
            print(json.dumps({
                "permissionDecision": "deny",
                "reason": f"Blocked dangerous command pattern: {reason}. Run manually if needed.",
            }))
        else:
            print(json.dumps({}))
    except (json.JSONDecodeError, KeyError):
        print(json.dumps({}))


if __name__ == "__main__":
    main()
