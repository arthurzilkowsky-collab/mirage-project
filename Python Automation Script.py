import csv


def fasta_to_grid_csv(fasta_path, output_csv_path, line_width=60):
  """Reads a FASTA file and writes it out in a fixed-width grid format (CSV)

  suitable for spreadsheet applications like OpenOffice Calc (1 cell = 1
  symbol).
  """
  sequences = []
  current_header = ""
  current_seq = []

  # 1. Parse the FASTA file
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

  # 2. Write out to CSV as a grid
  with open(output_csv_path, "w", newline="") as csvfile:
    writer = csv.writer(csvfile)

    for header, seq in sequences:
      # Optional: Add a header row for the sequence name
      writer.writerow([f"SEQUENCE: {header}"])

      # Break sequence into fixed chunks (e.g., 60 columns wide)
      for i in range(0, len(seq), line_width):
        chunk = seq[i : i + line_width]
        # Split every single character into its own list element (own column)
        row_cells = list(chunk)
        writer.writerow(row_cells)

      # Add a blank row between sequences if there are multiple
      writer.writerow([])

  print(
      f"Successfully converted {fasta_path} to grid CSV: {output_csv_path}"
  )


# Example usage:
# fasta_to_grid_csv("my_sequence.fasta", "genomic_tablature_grid.csv", line_width=50)