import logging
from pathlib import Path
from typing import Dict, Any, List
from mirage.vision.parser import MirrorParser

logger = logging.getLogger("MirageFastaLoader")

class FastaLoader:
    def __init__(self, parser: MirrorParser):
        self.parser = parser
        logger.info("FastaLoader initialized.")

    def parse_fasta_file(self, file_path: str) -> List[Dict[str, Any]]:
        """Reads a FASTA file and extracts records (Headers and Sequences)."""
        path = Path(file_path)
        if not path.exists():
            logger.error(f"FASTA file not found at: {path}")
            return []

        records = []
        current_header = ""
        current_seq_chunks = []

        try:
            with open(path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    if line.startswith(">"):
                        # If we were already building a record, save it first
                        if current_header:
                            full_seq = "".join(current_seq_chunks).upper()
                            records.append({"header": current_header, "sequence": full_seq})
                            current_seq_chunks = []
                        current_header = line[1:] # Drop the '>'
                    else:
                        current_seq_chunks.append(line)
                
                # Don't forget the last record in the file
                if current_header:
                    full_seq = "".join(current_seq_chunks).upper()
                    records.append({"header": current_header, "sequence": full_seq})

            logger.info(f"Successfully loaded {len(records)} record(s) from {path.name}")
            return records

        except Exception as e:
            logger.error(f"Failed to parse FASTA file: {e}")
            return []

    def analyze_gene_file(self, file_path: str) -> List[Dict[str, Any]]:
        """Loads a gene FASTA file and runs the mirror/palindrome scanning pipeline."""
        records = self.parse_fasta_file(file_path)
        analysis_results = []

        for record in records:
            header = record["header"]
            sequence = record["sequence"]
            
            logger.info(f"Running MirrorParser on gene record: [{header}] (Length: {len(sequence)} bp)")
            
            # Process the sequence through the Vision engine
            parse_result = self.parser.process(sequence)
            
            analysis_results.append({
                "header": header,
                "length": len(sequence),
                "analysis": parse_result
            })

        return analysis_results