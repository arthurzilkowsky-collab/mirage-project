import os
from pathlib import Path

def build_mirage_directory():
    # Define the target structure
    directories = [
        "mirage",
        "mirage/vision",
        "mirage/defense",
        "mirage/expression",
        "mirage/memory"
    ]
    
    # Create directories
    for dir_path in directories:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
        # Create an __init__.py to make it a proper Python package
        init_file = Path(dir_path) / "__init__.py"
        if not init_file.exists():
            init_file.touch()

    # Create a baseline core config if it doesn't exist
    config_path = Path("mirage_core.json")
    if not config_path.exists():
        default_config = {
            "name": "Mirage",
            "version": "3.0-unified",
            "core_principle": "Coherence & Resilience"
        }
        import json
        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(default_config, f, indent=4)
            
    print("[+] Mirage file structure successfully verified and aligned.")

if __name__ == "__main__":
    build_mirage_directory()