import time

# Define a species-specific sound/pitch map for the 4 bases
SPECIES_MAPS = {
    "bee": {'A': 69, 'T': 72, 'G': 76, 'C': 79},      # Brighter intervals (Major pentatonic flavor)
    "cannabis": {'A': 60, 'T': 63, 'G': 67, 'C': 70}  # Mellow intervals (Minor/ambient flavor)
}

def mg_to_piano_roll(sequence: str, profile: str = "cannabis"):
    """
    Parses a sequence into Mirror Groups and maps them to piano roll notes.
    """
    mapping = SPECIES_MAPS.get(profile, SPECIES_MAPS["cannabis"])
    
    # 1. Segment into Mirror Groups based on consecutive repeats
    groups = []
    current_group = sequence[0]
    for i in range(1, len(sequence)):
        if sequence[i] == sequence[i - 1]:
            groups.append(current_group)
            current_group = sequence[i]
        else:
            current_group += sequence[i]
    if current_group:
        groups.append(current_group)
        
    # 2. Convert groups into piano roll note events
    piano_roll_timeline = []
    time_cursor = 0.0
    
    for bar_idx, group in enumerate(groups):
        bar_events = []
        for char in group:
            pitch = mapping.get(char, 60)
            bar_events.append({
                'time': time_cursor,
                'pitch': pitch,
                'base': char,
                'bar': bar_idx + 1
            })
            time_cursor += 0.25  # Quarter-note step per base
            
        piano_roll_timeline.append({
            'bar_id': bar_idx + 1,
            'group_structure': group,
            'events': bar_events
        })
        
    return piano_roll_timeline

# Test the engine with a snippet
sample_dna = "ATGGATGATGATATCGCCGCGCTCGTCGTCGACAACG"
score = mg_to_piano_roll(sample_dna, profile="cannabis")

print("--- SCROLL OF ECHOES: PIANO ROLL SCORE ---")
for bar in score[:4]:
    print(f"Bar {bar['bar_id']} [MG: {bar['group_structure']}]: {len(bar['events'])} note events")