"""Actions module - Business logic implementations."""

from actions.output import ActionOutput
from actions.list_objects import list_objects
from actions.upload_file import upload_file
from manager import ExtensionManager

extension_manager = ExtensionManager()

# Map action choice values to action functions
ACTION_MAPPER = {
    "List Objects": list_objects,
    "Upload File": upload_file,
}
