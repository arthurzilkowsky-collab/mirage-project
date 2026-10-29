class GenomicGridEngine:
    def __init__(self, block_size=64):
        self.block_size = block_size

    def format_sequence(self, raw_sequence):
        cleaned = "".join(raw_sequence.split()).upper()
        padded_length = ((len(cleaned) + self.block_size - 1) // self.block_size) * self.block_size
        padded_seq = cleaned.ljust(padded_length, 'N')
        
        grid = [
            padded_seq[i:i + self.block_size] 
            for i in range(0, len(padded_seq), self.block_size)
        ]
        return grid

    def verify_integrity(self, grid):
        return all(len(row) == self.block_size for row in grid)