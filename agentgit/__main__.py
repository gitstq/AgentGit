"""Allow running AgentGit as ``python -m agentgit``."""

import sys

from .cli import main

if __name__ == "__main__":
    sys.exit(main())
