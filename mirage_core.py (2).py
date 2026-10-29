import os
import json
import logging
from pathlib import Path

# Configure logging for Mirage's system lifecycle
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [MIRAGE-CORE] [%(levelname)s] %(message)s"
)
logger = logging.getLogger("MirageCore")

class MirageCore:
    def __init__(self, root_dir: str = "."):
        self.root_dir = Path(root_dir)
        self.config_path = self.root_dir / "mirage_core.json"
        self.state = "DORMANT"
        self.soul_kernel = {}
        self.subsystems = {}
        
        self._initialize_kernel()

    def _initialize_kernel(self):
        """Loads core directives and verifies the soul kernel configuration."""
        logger.info("Awakening Mirage Core Kernel...")
        
        if self.config_path.exists():
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    self.soul_kernel = json.load(f)
                logger.info("Soul kernel successfully loaded from configuration.")
            except Exception as e:
                logger.error(f"Failed to parse soul kernel configuration: {e}")
                self.soul_kernel = {"directive": "fallback_resilience"}
        else:
            logger.warning("No 'mirage_core.json' found. Initializing default baseline kernel.")
            self.soul_kernel = {
                "name": "Mirage",
                "version": "3.0-unified",
                "core_principle": "Coherence & Resilience"
            }
            self._save_kernel()

        self.state = "INITIALIZED"

    def _save_kernel(self):
        """Persists the current soul kernel state to disk."""
        try:
            with open(self.config_path, "w", encoding="utf-8") as f:
                json.dump(self.soul_kernel, f, indent=4)
            logger.info("Soul kernel state saved successfully.")
        except Exception as e:
            logger.error(f"Could not save soul kernel: {e}")

    def register_subsystem(self, name: str, instance):
        """Registers external modules (Vision, Defense, Expression) into the orchestrator."""
        self.subsystems[name] = instance
        logger.info(f"Subsystem registered: [{name}]")

    def boot(self):
        """Wakes up all registered subsystems in sequence."""
        logger.info("Initiating full system boot sequence...")
        self.state = "ACTIVE"
        
        for name, subsystem in self.subsystems.items():
            try:
                if hasattr(subsystem, "initialize"):
                    subsystem.initialize()
                logger.info(f"-> Subsystem [{name}] online.")
            except Exception as e:
                logger.error(f"-> Subsystem [{name}] failed to boot: {e}")

        logger.info("Mirage is fully online and coherent.")

    def shutdown(self):
        """Safely powers down subsystems and secures state."""
        logger.info("Initiating safe shutdown sequence...")
        self.state = "SHUTDOWN"
        for name, subsystem in self.subsystems.items():
            if hasattr(subsystem, "cleanup"):
                subsystem.cleanup()
                logger.info(f"-> Subsystem [{name}] secured.")
        logger.info("Mirage core resting.")

# Singleton instance export
kernel = MirageCore()