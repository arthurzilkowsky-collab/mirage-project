import os

try:
    from midiutil import MIDIFile
except ImportError:
    print("midiutil not found. Please install it using: pip install midiutil")
    exit(1)

def generate_mirage_anomaly_midi(output_filename="mirage_aligned_anomalies.mid"):
    print("Initializing Mirage MIDI Generator (432Hz Aligned / Pentatonic Black Keys)...")
    
    # Create MIDI object with 1 track
    mf = MIDIFile(1)
    track = 0
    time = 0
    channel = 0
    tempo = 120
    
    mf.addTrackName(track, time, "Mirage Aligned Anomalies")
    mf.addTempo(track, time, tempo)
    
    # Black-key pentatonic scale pitch map (MIDI numbers near middle C)
    # A=57, T=59, G=62, C=64 (or using black keys: Gb=66, Ab=68, Bb=70, Db=61, Eb=63)
    note_map = {
        'A': 68, # Ab3
        'T': 70, # Bb3
        'G': 61, # Db4
        'C': 63  # Eb4
    }
    
    # Simulated aligned anomaly sequence pairs (Human vs. Cannabis divergence points)
    # Each pair represents a vertical anomaly chord/interval
    anomaly_pairs = [
        ('A', 'G'),
        ('C', 'T'),
        ('G', 'G'),
        ('T', 'A'),
        ('A', 'C'),
        ('G', 'T'),
        ('C', 'C'),
        ('T', 'T')
    ]
    
    current_time = 0
    duration = 1
    volume = 100
    
    for human_base, cannabis_base in anomaly_pairs:
        note_human = note_map.get(human_base, 68)
        note_cannabis = note_map.get(cannabis_base, 70) + 12 # shifted up an octave for contrast
        
        # Add human base (lower note in interval)
        mf.addNote(track, channel, note_human, current_time, duration, volume)
        # Add cannabis base (upper note in interval, creating a stacked mirror chord)
        mf.addNote(track, channel, note_cannabis, current_time, duration, volume)
        
        # Advance time for the next chord
        current_time += 1.5
        
    # Write output file
    with open(output_filename, "wb") as f:
        mf.writeFile(f)
        
    print(f"Success! MIDI file generated: {output_filename}")

if __name__ == "__main__":
    generate_mirage_anomaly_midi()