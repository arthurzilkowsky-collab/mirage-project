import sys
from mirage.core import kernel
from mirage.vision.parser import MirrorParser
from mirage.defense.integrity import IntegrityWatchdog
from mirage.defense.ai_defense import AIDefense
from mirage.expression.audio_engine import AudioEngine

def main():
    print("=== INITIALIZING MIRAGE UNIFIED ECOSYSTEM ===")
    
    # 1. Register Subsystems into the Core Kernel
    kernel.register_subsystem("vision_parser", MirrorParser(window_size=4))
    kernel.register_subsystem("integrity_watchdog", IntegrityWatchdog())
    kernel.register_subsystem("ai_defense", AIDefense())
    kernel.register_subsystem("audio_engine", AudioEngine())
    
    # 2. Boot Sequence
    kernel.boot()
    
    # 3. Quick System Health Check
    watchdog = kernel.subsystems["integrity_watchdog"]
    is_secure = watchdog.verify_integrity()
    
    if is_secure:
        print("\n[+] System integrity check passed. Mirage is fully operational.")
    else:
        print("\n[!] Warning: Integrity anomalies detected during boot.")

    # 4. Graceful Shutdown Test
    kernel.shutdown()

if __name__ == "__main__":
    main()