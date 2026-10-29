import csv


def fasta_to_genomic_grid(fasta_path, output_csv_path, line_width=60):
  """Parses a FASTA file and exports a grid-formatted CSV file

  with coordinate markers for OpenOffice Calc (1 box = 1 symbol).
  """
  sequences = []
  current_header = ""
  current_seq = []

  # 1. Read FASTA file
  with open(fasta_path, "r") as f:
    for line in f:
      line = line.strip()
      if line.startswith(">"):
        if current_header:
          sequences.append((current_header, "".join(current_seq)))
        current_header = line[1:]
        current_seq = []
      else:
        current_seq.append(line)
    if current_header:
      sequences.append((current_header, "".join(current_seq)))

  # 2. Write to CSV with Grid and Position Labels
  with open(output_csv_path, "w", newline="") as csvfile:
    writer = csv.writer(csvfile)

    for header, seq in sequences:
      # Header banner for the sequence
      writer.writerow([f"SEQUENCE: {header}"])

      # Column header numbers (1 to line_width) for visual alignment
      col_headers = ["Range"] + [str(i + 1) for i in range(line_width)]
      writer.writerow(col_headers)

      # Chunk the sequence into fixed line widths (graph paper rows)
      for i in range(0, len(seq), line_width):
        chunk = seq[i : i + line_width]
        start_pos = i + 1
        end_pos = i + len(chunk)

        # First column is the coordinate label (e.g., "1-60")
        row_data = [f"{start_pos}-{end_pos}"] + list(chunk)
        writer.writerow(row_data)

      # Blank row separator between different sequences
      writer.writerow([])

  print(
      f"Successfully exported genomic grid tablature to: {output_csv_path}"
  )


# --- Example execution ---
# fasta_to_genomic_grid("input_sequence.fasta", "genomic_tablature_output.csv", line_width=60)