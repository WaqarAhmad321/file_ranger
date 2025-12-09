from pathlib import Path

# Simple icon mapping based on file extensions

ICON_MAP = {
    # Programming
    ".py": "",
    ".cpp": "",
    ".c": "",
    ".h": "",
    ".hpp": "",
    ".js": "",
    ".ts": "",
    ".html": "",
    ".css": "",
    ".json": "",
    ".md": "",
    ".txt": "",
    ".sh": "",
    ".yml": "",
    ".yaml": "",
    ".xml": "󰗀",
    ".sql": "",
    ".java": "",
    ".go": "",
    ".rs": "",
    ".php": "",
    
    # Images
    ".png": "",
    ".jpg": "",
    ".jpeg": "",
    ".gif": "",
    ".svg": "",
    ".ico": "",
    
    # Documents
    ".pdf": "",
    ".doc": "",
    ".docx": "",
    ".xls": "",
    ".xlsx": "",
    ".ppt": "",
    ".pptx": "",
    
    # Archives
    ".zip": "",
    ".tar": "",
    ".gz": "",
    ".rar": "",
    ".7z": "",
    
    # Config
    ".ini": "⚙",
    ".conf": "⚙",
    ".cfg": "⚙",
    ".toml": "⚙",
    ".gitignore": "",
    ".dockerignore": "",
    "Dockerfile": "",
    "Makefile": "",
    "CMakeLists.txt": "",
}

DEFAULT_FILE_ICON = ""
DEFAULT_DIR_ICON = ""

def get_icon(name: str, is_directory: bool) -> str:
    if is_directory:
        return DEFAULT_DIR_ICON
    
    # Check exact filename first (e.g. Dockerfile)
    if name in ICON_MAP:
        return ICON_MAP[name]
        
    # Check extension
    ext = Path(name).suffix.lower()
    return ICON_MAP.get(ext, DEFAULT_FILE_ICON)
