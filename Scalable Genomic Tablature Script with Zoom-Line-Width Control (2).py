import csv


def generate_scalable_genomic_grid(
    fasta_path, output_csv_path, line_width=60, target_motif="MG"
):
  """Parses a FASTA file and generates a scalable grid-tablature CSV

  with adjustable 'zoom' (line_width) and integrated motif trajectory mapping.
  """
  sequences = []
  current_header = ""
  current_seq = []

  # 1. Read FASTA file
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

  # 2. Write scalable grid and trajectory report to CSV
  with open(output_csv_path, "w", newline="") as csvfile:
    writer = csv.writer(csvfile)

    for header, seq in sequences:
      # --- SECTION 1: THE GRAPH PAPER GRID (Adjustable Zoom) ---
      writer.writerow([
          f"=== GENOMIC TABLATURE GRID (Zoom / Width: {line_width} columns) ==="
      ])
      writer.writerow([f"SEQUENCE: {header} (Length: {len(seq)})"])

      # Column coordinate markers based on chosen zoom level
      col_headers = ["Range"] + [str(i + 1) for i in range(line_width)]
      writer.writerow(col_headers)

      # Build the grid rows
      for i in range(0, len(seq), line_width):
        chunk = seq[i : i + line_width]
        start_pos = i + 1
        end_pos = i + len(chunk)
        row_data = [f"{start_pos}-{end_pos}"] + list(chunk)
        writer.writerow(row_data)

      writer.writerow([])  # Spacing

      # --- SECTION 2: MOTIF TRAJECTORY & SPACING MAP ---
      writer.writerow([f"=== TRAJECTORY ANALYSIS FOR TARGET: {target_motif} ==="])
      writer.writerow(
          ["Occurrence #", "Start Position", "End Position", "Interval Distance"]
      )

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
        end_pos = pos + len(target_motif) - 1
        distance = (pos - prev_pos) if prev_pos > 0 else 0
        writer.writerow([idx, pos, end_pos, distance])
        prev_pos = pos

      writer.writerow([])
      writer.writerow([f"Total '{target_motif}' Clusters Found: {len(occurrences)}"])
      writer.writerow([])
      writer.writerow(
          ["=" * 40]
      )  # Separator between multiple sequences if present
      writer.writerow([])

  print(
      f"Scalable grid & trajectory report saved to: {output_csv_path} (Zoom"
      f" width: {line_width})"
  )


# --- Example execution ---
# To zoom in close, set line_width=30
# To zoom out for macro view, set line_width=100 or 120
# generate_scalable_genomic_grid("input_sequences.fasta", "genomic_tablature_zoom60.csv", line_width=60, target_motif="MG")