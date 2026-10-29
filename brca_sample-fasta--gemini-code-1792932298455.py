from mirage.vision.parser import MirrorParser
from mirage.vision.fasta_loader import FastaLoader

# 1. Initialize parser and loader
parser = MirrorParser(window_size=6) # Look for 6-base symmetry windows
loader = FastaLoader(parser=parser)

# 2. Run analysis on your gene library file
results = loader.analyze_gene_file("brca_sample.fasta")

# 3. Inspect results
for res in results:
    print(f"Gene: {res['header']}")
    print(f"Total Length: {res['length']} base pairs")
    print(f"Mirrors/Palindromes Detected: {res['analysis']['mirrors_detected']}")