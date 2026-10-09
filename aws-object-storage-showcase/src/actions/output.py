"""ActionOutput dataclass for action return values."""

import json
from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class ActionOutput:
    """Output from action functions.

    Fields:
        result: Structured result dict for the Extension Output JSON.
                For List Objects: {"bucket": ..., "count": ..., "truncated": ..., "objects": [...]}
                For Upload File: {"bucket": ..., "key": ..., "local_file": ...}
        status_description: Human-readable summary used as the task status description.
        exit_code: Extension exit code (0 = success, 1 = operational error, 20 = validation error).
    """

    result: Optional[Dict[str, Any]] = None
    status_description: Optional[str] = None
    exit_code: int = 0

    def print_output(self) -> None:
        """Print to STDOUT.

        The actions in this extension write STDOUT directly during execution
        (tabulate table for List Objects, confirmation line for Upload File).
        This method is a no-op because no deferred STDOUT control fields exist
        in the template.
        """

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dict for Extension Output (unv_output).

        Returns a dict with a single ``result`` key containing the structured
        result data. No output_options control field exists in the template,
        so all result data is always included.

        Returns:
            Dict containing the ``result`` key (omitted when result is None).
        """
        output: Dict[str, Any] = {}
        if self.result is not None:
            output["result"] = self.result
        return output
