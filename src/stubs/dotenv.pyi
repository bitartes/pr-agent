"""Type stubs for python-dotenv."""
from typing import Optional

def load_dotenv(
    dotenv_path: Optional[str] = None,
    stream: Optional[str] = None,
    verbose: bool = False,
    override: bool = False,
    encoding: Optional[str] = None,
) -> bool: ...
