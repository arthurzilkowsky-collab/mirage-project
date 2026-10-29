import hashlib
import json
import logging
from pathlib import Path
from typing import Dict

logger = logging.getLogger("MirageIntegrity")

class IntegrityWatchdog:
    def __init__(self, target_dir: str = ".", manifest_name: str = "integrity_manifest.json"):
        self.target_dir = Path(target_dir)
        self.manifest_path = self.target_dir / manifest_name
        self.baseline_hashes: Dict[str, str] = {}

    def _hash_file(self, file_path: Path) -> str:
        """Computes the SHA-256 hash of a given file."""
        hasher = hashlib.sha256()
        try:
            with open(file_path, "rb") as f:
                while chunk := f.read(8192):
                    hasher.update(chunk)
            return hasher.hexdigest()
        except Exception as e:
            logger.error(f"Failed to hash {file_path}: {e}")
            return ""

    def create_baseline(self, file_patterns: list = ["*.py", "*.json"]):
        """Scans target files and establishes a baseline integrity manifest."""
        logger.info("Creating integrity baseline for system files...")
        self.baseline_hashes.clear()
        
        for pattern in file_patterns:
            for file_path in self.target_dir.rglob(pattern):
                if "venv" in file_path.parts or ".git" in file_path.parts:
                    continue
                file_hash = self._hash_file(file_path)
                if file_hash:
                    relative_path = str(file_path.relative_to(self.target_dir))
                    self.baseline_hashes[relative_path] = file_hash

        try:
            with open(self.manifest_path, "w", encoding="utf-8") as f:
                json.dump(self.baseline_hashes, f, indent=4)
            logger.info(f"Baseline saved with {len(self.baseline_hashes)} file signatures.")
        except Exception as e:
            logger.error(f"Failed to save integrity manifest: {e}")

    def verify_integrity(self) -> bool:
        """Compares current file states against the saved baseline manifest."""
        if not self.manifest_path.exists():
            logger.warning("No integrity manifest found. Creating a new baseline.")
            self.create_baseline()
            return True

        try:
            with open(self.manifest_path, "r", encoding="utf-8") as f:
                saved_hashes = json.load(f)
        except Exception as e:
            logger.error(f"Failed to load integrity manifest: {e}")
            return False

        logger.info("Verifying system file integrity...")
        tampered_files = []

        for rel_path, original_hash in saved_hashes.items():
            file_path = self.target_dir / rel_path
            if not file_path.exists():
                tampered_files.append((rel_path, "MISSING"))
                continue
            
            current_hash = self._hash_file(file_path)
            if current_hash != original_hash:
                tampered_files.append((rel_path, "MODIFIED"))

        if tampered_files:
            logger.warning(f"INTEGRITY ALERT: Anomalies detected in {len(tampered_files)} files!")
            for path, status in tampered_files:
                logger.warning(f" -> [{status}] {path}")
            return False

        logger.info("System integrity verified. All signatures match.")
        return True