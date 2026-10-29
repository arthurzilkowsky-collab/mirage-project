import csv
import sys


def process_genomic_tablature(
    fasta_path, output_csv_path, line_width=60, target_motif="MG"
):
  """Parses a FASTA file and generates an automated spreadsheet CSV containing:

  1. The graph-paper grid layout (1 symbol per cell) with coordinate range markers.
  2. Adjustable zoom/line-width control.
  3. A complete MG cluster trajectory and spacing report.
  """
  sequences = []
  current_header = ""
  current_seq = []

  # 1. Parse the FASTA file
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

  # 2. Write the combined grid and trajectory data to CSV
  with open(output_csv_path, "w", newline="") as csvfile:
    writer = csv.writer(csvfile)

    for header, seq in sequences:
      seq_len = len(seq)

      # --- SECTION 1: GRAPH PAPER TABLATURE GRID ---
      writer.writerow([
          f"=== GENOMIC TABLATURE GRID (Zoom / Width: {line_width} columns) ==="
      ])
      writer.writerow([f"SEQUENCE: {header} | Total Length: {seq_len} bp"])

      # Column position header markers (1 to line_width)
      col_headers = ["Range"] + [str(i + 1) for i in range(line_width)]
      writer.writerow(col_headers)

      # Write out the grid rows (1 cell = 1 symbol)
      for i in range(0, seq_len, line_width):
        chunk = seq[i : i + line_width]
        start_pos = i + 1
        end_pos = i + len(chunk)
        row_data = [f"{start_pos}-{end_pos}"] + list(chunk)
        writer.writerow(row_data)

      writer.writerow([])  # Spacing separator

      # --- SECTION 2: MOTIF & MG CLUSTER TRAJECTORY REPORT ---
      writer.writerow([f"=== TRAJECTORY ANALYSIS FOR TARGET: '{target_motif}' ==="])
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
        occurrences.append(pos + 1)  # 1-based indexing
        start_idx = pos + 1

      # Calculate spacing/intervals between cluster occurrences
      prev_pos = 0
      for idx, pos in enumerate(occurrences, start=1):
        end_pos = pos + len(target_motif) - 1
        distance = (pos - prev_pos) if prev_pos > 0 else 0
        writer.writerow([idx, pos, end_pos, distance])
        prev_pos = pos

      writer.writerow([])
      writer.writerow([f"Total '{target_motif}' Clusters Located: {len(occurrences)}"])
      writer.writerow([])
      writer.writerow(["=" * 50])
      writer.writerow([])

  print(
      f"Success! Tablature spreadsheet generated: '{output_csv_path}' (Zoom"
      f" width: {line_width})"
  )


if __name__ == "__main__":
  # Change these parameters to match your input file and preferred zoom scale
  input_fasta_file = "my_sequences.fasta"
  output_csv_file = "genomic_tablature_output.csv"

  # Choose your zoom level:
  # - Smaller width (e.g., 30 or 40) = Close-up inspection view
  # - Wider width (e.g., 80 or 100) = Macro structural view
  ZOOM_LINE_WIDTH = 60
  TARGET_MOTIF = "MG"

  process_genomic_tablature(
      input_fasta_file,
      output_csv_file,
      line_width=ZOOM_LINE_WIDTH,
      target_motif=TARGET_MOTIF,
  )