import csv


def scan_motif_trajectory(
    fasta_path, output_csv_path, target_motif="MG", line_width=60
):
  """Scans a FASTA sequence for a target motif/MG cluster,

  records all occurrence coordinates, and outputs a trajectory spreadsheet.
  """
  # Read FASTA
  sequences = []
  current_header = ""
  current_seq = []

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

  # Process and write trajectory data
  with open(output_csv_path, "w", newline="") as csvfile:
    writer = csv.writer(csvfile)

    for header, seq in sequences:
      writer.writerow([f"SEQUENCE: {header} | TARGET MOTIF: {target_motif}"])
      writer.writerow(
          ["Occurrence #", "Start Position", "End Position", "Distance from Prev"]
      )

      # Find all occurrences of the motif (case-insensitive)
      seq_upper = seq.upper()
      motif_upper = target_motif.upper()
      occurrences = []

      start_idx = 0
      while True:
        pos = seq_upper.find(motif_upper, start_idx)
        if pos == -1:
          break
        occurrences.append(pos + 1)  # 1-based index
        start_idx = pos + 1  # allow overlapping or shift by len(motif_upper)

      # Record each hit and calculate the interval distance
      prev_pos = 0
      for idx, pos in enumerate(occurrences, start=1):
        end_pos = pos + len(target_motif) - 1
        distance = (pos - prev_pos) if prev_pos > 0 else 0
        writer.writerow([idx, pos, end_pos, distance])
        prev_pos = pos

      writer.writerow([])
      writer.writerow([f"Total Occurrences found: {len(occurrences)}"])
      writer.writerow([])

  print(
      f"Trajectory report for '{target_motif}' saved to: {output_csv_path}"
  )


# --- Example execution ---
# scan_motif_trajectory("sequence.fasta", "mg_trajectory_report.csv", target_motif="MG", line_width=60)