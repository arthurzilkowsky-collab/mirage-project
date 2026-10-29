import csv


def generate_multilayer_genomic_grid(
    fasta_path, output_csv_path, window_levels=[30, 60, 90], target_motif="MG"
):
  """Parses a FASTA file and generates a multi-window spreadsheet CSV featuring:

  1. Multiple distinct zoom/width tiers for side-by-side or stacked cross-comparison.
  2. An Overlay Synchronization Table mapping exact coordinates and row-levels
     for every target motif occurrence across all zoom windows.
  """
  # 1. Parse FASTA
  sequences = []
  current_header = ""
  current_seq = []

  try:
    with open(fasta_path, "r") as f:
      for line in f:
        line = line.strip()
        if not line:
          continue
        if line.startswith(">"):
          if current_header:
            sequences.append((current_header, "".join(current_seq)))
          current_header = line[1:]
          current_seq = []
        else:
          current_seq.append(line)
      if current_header:
        sequences.append((current_header, "".join(current_seq)))
  except FileNotFoundError:
    print(f"Error: Could not locate FASTA file at '{fasta_path}'")
    return

  # 2. Write multi-level grid & overlay reports
  with open(output_csv_path, "w", newline="") as csvfile:
    writer = csv.writer(csvfile)

    for header, seq in sequences:
      seq_len = len(seq)

      writer.writerow([f"=== MULTI-LEVEL GENOMIC TABLATURE: {header} ==="])
      writer.writerow([f"Total Sequence Length: {seq_len} bp"])
      writer.writerow([])

      # --- TIER 1: MULTIPLE ZOOM/WINDOW LEVELS ---
      for width in window_levels:
        writer.writerow([f"--- WINDOW LEVEL / ZOOM: {width} COLUMNS ---"])
        col_headers = ["Range"] + [str(i + 1) for i in range(width)]
        writer.writerow(col_headers)

        for i in range(0, seq_len, width):
          chunk = seq[i : i + width]
          start_pos = i + 1
          end_pos = i + len(chunk)
          writer.writerow([f"{start_pos}-{end_pos}"] + list(chunk))

        writer.writerow([])  # Blank separation between zoom tiers

      # --- TIER 2: OVERLAY SYNCHRONIZATION & TRAJECTORY MAPPING ---
      writer.writerow([f"=== OVERLAY SYNCHRONIZATION FOR TARGET: '{target_motif}' ==="])
      
      # Dynamically build header columns based on active window levels
      overlay_headers = ["Occurrence #", "Position"] + [f"Win {w} Row" for w in window_levels] + ["Interval Distance"]
      writer.writerow(overlay_headers)

      seq_upper = seq.upper()
      motif_upper = target_motif.upper()
      occurrences = []

      start_idx = 0
      while True:
        pos = seq_upper.find(motif_upper, start_idx)
        if pos == -1:
          break
        occurrences.append(pos + 1)
        start_idx = pos + 1

      prev_pos = 0
      for idx, pos in enumerate(occurrences, start=1):
        distance = (pos - prev_pos) if prev_pos > 0 else 0
        
        # Calculate row coordinate mapping for each window level
        row_mappings = [f"Row {((pos - 1) // w) + 1}" for w in window_levels]
        
        row_data = [idx, pos] + row_mappings + [distance]
        writer.writerow(row_data)

      writer.writerow([])
      writer.writerow([f"Total '{target_motif}' Clusters Found: {len(occurrences)}"])
      writer.writerow([])
      writer.writerow(["=" * 60])
      writer.writerow([])

  print(
      f"Multi-level tablature overlay successfully exported to:"
      f" '{output_csv_path}'"
  )


if __name__ == "__main__":
  input_fasta_file = "my_sequences.fasta"
  output_csv_file = "multilayer_tablature_output.csv"

  # Define your custom zoom/window levels for simultaneous comparison:
  # e.g., 30 (close-up micro inspection), 60 (standard view), 120 (macro-structural view)
  ACTIVE_WINDOW_LEVELS = [30, 60, 120]
  TARGET_MOTIF = "MG"

  generate_multilayer_genomic_grid(
      input_fasta_file,
      output_csv_file,
      window_levels=ACTIVE_WINDOW_LEVELS,
      target_motif=TARGET_MOTIF,
  )