import csv
import sys


def convert_fasta_to_spreadsheet_grid(
    fasta_path, output_csv_path, line_width=60
):
  """Reads a FASTA file and exports a grid-formatted CSV file

  optimized for spreadsheet software like OpenOffice Calc.
  Each nucleotide occupies its own individual cell (1 box = 1 symbol).
  """
  sequences = []
  current_header = ""
  current_seq = []

  # 1. Parse FASTA file
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
    print(f"Error: Could not find the file at {fasta_path}")
    return

  # 2. Write out to CSV Grid format
  with open(output_csv_path, "w", newline="") as csvfile:
    writer = csv.writer(csvfile)

    for header, seq in sequences:
      # Sequence metadata banner row
      writer.writerow([f"SEQUENCE: {header} (Total Length: {len(seq)})"])

      # Column position header (1 to line_width) for alignment
      col_headers = ["Range"] + [str(i + 1) for i in range(line_width)]
      writer.writerow(col_headers)

      # Break sequence into graph-paper rows of fixed line width
      for i in range(0, len(seq), line_width):
        chunk = seq[i : i + line_width]
        start_pos = i + 1
        end_pos = i + len(chunk)

        # First column = coordinate range, subsequent columns = individual bases
        row_data = [f"{start_pos}-{end_pos}"] + list(chunk)
        writer.writerow(row_data)

      # Blank row separation between sequences
      writer.writerow([])

  print(
      f"Successfully converted '{fasta_path}' to grid tablature CSV:"
      f" '{output_csv_path}'"
  )


if __name__ == "__main__":
  # Change these file names to match your actual FASTA input file
  input_fasta = "input_sequences.fasta"
  output_csv = "genomic_tablature_output.csv"

  # You can adjust line_width here (e.g., 60 or 80 columns wide per block)
  convert_fasta_to_spreadsheet_grid(input_fasta, output_csv, line_width=60)