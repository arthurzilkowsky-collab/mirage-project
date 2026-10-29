def parse_mirror_groups(sequence: str):
    """
    Automatically segments a nucleotide sequence into Mirror Groups (structural bars)
    based on consecutive repeating characters.
    """
    clean_seq = sequence.upper().strip()
    if not clean_seq:
        return []
        
    groups = []
    current_group = clean_seq[0]
    
    for i in range(1, len(clean_seq)):
        if clean_seq[i] == clean_seq[i - 1]:
            current_group += clean_seq[i]
        else:
            groups.append(current_group)
            current_group = clean_seq[i]
            
    if current_group:
        groups.append(current_group)
        
    return groups

# Example test using a snippet of sequence data
test_sequence = "ATGGATGATGATATCGCCGCGCTCGTCGTCGACAACG"
mirror_bars = parse_mirror_groups(test_sequence)

print(f"Total Sequence Length: {len(test_sequence)} bp")
print(f"Total Structural Mirror Groups: {len(mirror_bars)}")
print(f"First 6 Bars: {mirror_bars[:6]}e")