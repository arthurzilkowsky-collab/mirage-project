def compare_sequences(reference_seq, variant_seq):
    print(f"\n--- MIRAGE Structural Comparison ---")
    print(f"Reference: {reference_seq}")
    print(f"Variant:   {variant_seq}\n")
    
    ref_parsed = parse_continuous_mirror_groups(reference_seq)
    var_parsed = parse_continuous_mirror_groups(variant_seq)
    
    print("Reference Mirror Groups:")
    for g in ref_parsed["groups"]:
        print(f"  {g['left_mirror']}[{g['core']}]{g['right_mirror']}")
        
    print("\nVariant Mirror Groups:")
    for g in var_parsed["groups"]:
        print(f"  {g['left_mirror']}[{g['core']}]{g['right_mirror']}")
        
    # Structural Delta Check
    ref_cores = [g['core'] for g in ref_parsed["groups"]]
    var_cores = [g['core'] for g in var_parsed["groups"]]
    
    print("\n[Structural Delta Analysis]:")
    if ref_cores == var_cores:
        print("  ✅ Structural integrity intact. Mirror geometry matches reference.")
    else:
        print("  ⚠️ Structural anomaly detected! Mirror group cores diverge.")
        print(f"     Ref Cores: {ref_cores}")
        print(f"     Var Cores: {var_cores}")

# Example Run: Healthy vs Damaged
if __name__ == "__main__":
    healthy_dna = "AGTCTTGACG"
    damaged_dna = "AGTCTTGGACG"  # Added duplicate G (mutation/repeat disruption)
    compare_sequences(healthy_dna, damaged_dna)