import re

def calculate_local_entropy(subseq: str) -> float:
    """Calculates nucleotide distribution entropy for a structural window."""
    if not subseq:
        return 0.0
    from collections import Counter
    import math
    counts = Counter(subseq)
    length = len(subseq)
    entropy = -sum((count / length) * math.log2(count / length) for count in counts.values())
    return entropy

def scan_genome_for_crispr_targets(sequence: str, pam_motif: str = "NGG"):
    """
    Scans a sequence for Mirror Groups, identifies Cas target windows near PAM sites,
    and flags high-risk structural off-target zones.
    """
    print(f"--- GENOME STRUCTURAL SCANNER ACTIVE ---")
    print(f"Total Sequence Length: {len(sequence):,} bp")
    
    # 1. Segment sequence into Mirror Groups (Structural Bars)
    groups = []
    current_group = sequence[0]
    for i in range(1, len(sequence)):
        if sequence[i] == sequence[i - 1]:
            current_group += sequence[i]
        else:
            groups.append(current_group)
            current_group = sequence[i]
    if current_group:
        groups.append(current_group)
        
    print(f"Identified {len(groups)} distinct structural Mirror Groups.")
    
    # 2. Simulate scanning for target binding windows and palindromic hotspots
    # Looking for inverted repeats (palindromes) which form stable hairpin structures
    targets_found = []
    
    # Simple sliding window check for 20bp protospacers
    window_size = 20
    for i in range(len(sequence) - window_size - 3):
        protospacer = sequence[i:i+window_size]
        pam_site = sequence[i+window_size:i+window_size+3]
        
        # Check if PAM matches standard criteria (e.g., ending in GG for SpCas9)
        if pam_site.endswith("GG"):
            # Check palindromic symmetry / mirror harmony
            is_palindrome = protospacer == protospacer[::-1]
            entropy = calculate_local_entropy(protospacer)
            
            # Risk scoring: High symmetry + low entropy can mean aggressive hairpin looping
            risk_tier = "HIGH" if is_palindrome or entropy < 1.5 else "OPTIMAL"
            
            targets_found.append({
                'index': i,
                'protospacer': protospacer,
                'pam': pam_site,
                'entropy': round(entropy, 2),
                'risk': risk_tier
            })
            
    print(f"Found {len(targets_found)} viable Cas9 target windows.")
    
    # Summary of findings
    optimal_targets = [t for t in targets_found if t['risk'] == 'OPTIMAL']
    print(f"-> Optimal Low-Risk Targets for Intervention: {len(optimal_targets)}")
    print(f"-> High-Risk Structural Hairpin Hotspots Flagged: {len(targets_found) - len(optimal_targets)}")
    
    return targets_found

# Test with a mock genetic sequence snippet
mock_genome = "ATGGATGATGATATCGCCGCGCTCGTCGTCGACAACGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCG" * 10
scan_results = scan_genome_for_crispr_targets(mock_genome)