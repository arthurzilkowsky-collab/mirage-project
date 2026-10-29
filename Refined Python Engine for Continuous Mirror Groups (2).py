def parse_continuous_mirror_groups(sequence):
    """
    Parses a sequence into continuous Mirror Groups (MGs) and remainders,
    where groups share transition boundaries (end of one is the start/frame of the next).
    """
    if not sequence or len(sequence) < 2:
        return {"groups": [], "remainders": [sequence]}

    groups = []
    remainders = []
    
    i = 0
    while i < len(sequence) - 1:
        start_char = sequence[i]
        # Look ahead for the furthest matching character to form the longest valid core
        match_idx = -1
        for j in range(len(sequence) - 1, i, -1):
            if sequence[j] == start_char:
                core = sequence[i + 1:j]
                # Check for internal adjacent repeats
                has_repeats = any(core[k] == core[k+1] for k in range(len(core) - 1))
                if not has_repeats:
                    match_idx = j
                    break
        
        if match_idx != -1:
            core = sequence[i+1:match_idx]
            groups.append({
                "left_mirror": start_char,
                "core": core,
                "right_mirror": sequence[match_idx],
                "start": i,
                "end": match_idx
            })
            # Advance i to match_idx so the next group shares this boundary letter
            i = match_idx
        else:
            # If no valid mirror frame found, treat as remainder and advance
            remainders.append(sequence[i])
            i += 1
            
    if i < len(sequence):
        remainders.append(sequence[i:])
        
    return {"groups": groups, "remainders": remainders}

# Test the refined logic
if __name__ == "__main__":
    test_seq = "AGTCTTGACG"
    result = parse_continuous_mirror_groups(test_seq)
    print("Sequence:", test_seq)
    print("Continuous Mirror Groups:")
    for g in result["groups"]:
        print(f"  {g['left_mirror']}[{g['core']}]{g['right_mirror']}")
    print("Remainders:", result["remainders"])