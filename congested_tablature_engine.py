import csv


def process_tablature_with_congestion_control(
    fasta_path,
    output_csv_path,
    window_levels=[30, 60, 120],
    target_motif="MG",
    congestion_threshold=10,
):
  """Parses a FASTA file, manages multi-window overlays, and flags

  high-density/congested cluster regions to keep data organized.
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

  # 2. Write Output CSV with Congestion Analytics
  with open(output_csv_path, "w", newline="") as csvfile:
    writer = csv.writer(csvfile)

    for header, seq in sequences:
      seq_len = len(seq)

      writer.writerow([f"=== CONGESTION-CONTROLLED TABLATURE: {header} ==="])
      writer.writerow([f"Total Length: {seq_len} bp | Congestion Gap Limit: < {congestion_threshold} bp"])
      writer.writerow([])

      # --- TIER 1: MULTI-WINDOW ZOOM TIERS ---
      for width in window_levels:
        writer.writerow([f"--- WINDOW LEVEL / ZOOM: {width} COLUMNS ---"])
        col_headers = ["Range"] + [str(i + 1) for i in range(width)]
        writer.writerow(col_headers)

        for i in range(0, seq_len, width):
          chunk = seq[i : i + width]
          start_pos = i + 1
          end_pos = i + len(chunk)
          writer.writerow([f"{start_pos}-{end_pos}"] + list(chunk))

        writer.writerow([])

      # --- TIER 2: SYNCHRONIZATION & CONGESTION REPORT ---
      writer.writerow([f"=== TRAJECTORY & CONGESTION ANALYSIS FOR '{target_motif}' ==="])
      
      overlay_headers = ["Occurrence #", "Position"] + [f"Win {w} Row" for w in window_levels] + ["Interval", "Density Status"]
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
        distance = (pos - prev_pos) if prev_pos > 0 else 9999
        
        # Determine if this cluster is part of a congested/dense zone
        density_status = "CONGESTED (Dense)" if (0 < distance <= congestion_threshold) else "Clear / Spaced"
        
        row_mappings = [f"Row {((pos - 1) // w) + 1}" for w in window_levels]
        
        row_data = [idx, pos] + row_mappings + [(distance if prev_pos > 0 else "N/A"), density_status]
        writer.writerow(row_data)
        prev_pos = pos

      writer.writerow([])
      writer.writerow([f"Total '{target_motif}' Clusters Mapped: {len(occurrences)}"])
      writer.writerow([])
      writer.writerow(["=" * 60])
      writer.writerow([])

  print(
      f"Congestion-managed tablature successfully exported to:"
      f" '{output_csv_path}'"
  )


if __name__ == "__main__":
  input_fasta_file = "my_sequences.fasta"
  output_csv_file = "congested_tablature_output.csv"

  # Active window zoom levels & congestion spacing threshold
  ACTIVE_WINDOW_LEVELS = [30, 60, 120]
  TARGET_MOTIF = "MG"
  CONGESTION_GAP_LIMIT = 12  # Flags clusters closer than 12 base pairs apart

  process_tablature_with_congestion_control(
      input_fasta_file,
      output_csv_file,
      window_levels=ACTIVE_WINDOW_LEVELS,
      target_motif=TARGET_MOTIF,
      congestion_threshold=CONGESTION_GAP_LIMIT,
  )