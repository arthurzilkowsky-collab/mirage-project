// Schillinger Melodic Permutation Engine
function generatePermutations(intervals) {
    let matrix = [];
    let len = intervals.length;
    
    for (let i = 0; i < len; i++) {
        // Rotate the array to create a permutation row
        let rotated = [...intervals.slice(i), ...intervals.slice(0, i)];
        matrix.push(rotated);
    }
    
    return matrix;
}

// Example Seed: Intervals representing semitone steps (e.g., Root, Minor 3rd, Perfect 4th, Minor 6th)
const baseSeed = [0, 3, 5, 8, 10];
const melodicMatrix = generatePermutations(baseSeed);

console.log("Schillinger Permutation Matrix:", melodicMatrix);