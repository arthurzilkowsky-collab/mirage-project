import math
from collections import Counter

def analyze_genome_harmonics(sequence: str):
    """
    Calculates nucleotide frequencies, binary switch distributions, 
    and local entropy across a sequence.
    """
    clean_seq = sequence.upper().strip()
    length = len(clean_seq)
    
    # 1. Base frequencies
    counts = Counter(clean_seq)
    
    # 2. Shannon Entropy calculation (harmonic stability indicator)
    entropy = -sum((count / length) * math.log2(count / length) for count in counts.values() if count > 0)
    
    # 3. Binary Switch tracking (e.g., AT/TA, CG/GC pairs)
    switches = {
        "AT_TA": clean_seq.count("AT") + clean_seq.count("TA"),
        "CG_GC": clean_seq.count("CG") + clean_seq.count("GC"),
        "TG_GT": clean_seq.count("TG") + clean_seq.count("GT"),
        "CT_TC": clean_seq.count("CT") + clean_seq.count("TC")
    }
    
    print("--- HARMONIC & BINARY SWITCH PROFILE ---")
    print(f"Sequence Length: {length:,} bp")
    print(f"Harmonic Entropy Score: {entropy:.4f} bits (lower = higher structural order)")
    print("Binary Switch Counts:")
    for pair, count in switches.items():
        print(f"  - {pair}: {count}")

# Run analysis on our test sequence
analyze_genome_harmonics(test_sequence)