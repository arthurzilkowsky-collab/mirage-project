def parse_mirror_groups(sequence):
    """
    Parses a sequence into Mirror Groups based on the core definition:
    - A new group starts at index 1 and wherever two adjacent symbols are equal (si == si-1).
    - Returns a list of substrings (Mirror Groups).
    """
    if not sequence:
        return []
    
    groups = []
    current_group = [sequence[0]]
    
    for i in range(1, len(sequence)):
        if sequence[i] == sequence[i-1]:
            # Boundary hit: save current group and start a new one
            groups.append("".join(current_group))
            current_group = [sequence[i]]
        else:
            current_group.append(sequence[i])
            
    if current_group:
        groups.append("".join(current_group))
        
    return groups

# Example usage with the sequence from our earlier discussion: A AGTCT TGACG G
test_seq = "AAGTCTTGACGG"
print(f"Original Sequence: {test_seq}")
print(f"Parsed Mirror Groups: {parse_mirror_groups(test_seq)}")