// Schillinger Resultant Generator
function generateSchillingerResultant(a, b) {
    let period = a * b;
    let result = [];
    
    for (let i = 0; i < period; i++) {
        let hitA = (i % a === 0);
        let hitB = (i % b === 0);
        
        if (hitA && hitB) {
            result.push("accent"); // Coincident pulse
        } else if (hitA || hitB) {
            result.push("pulse");  // Single pulse
        } else {
            result.push("rest");   // Silence
        }
    }
    return result;
}

// Example: Interference of 3 against 4 (generates a 12-step asymmetric cell)
const schillingerCell = generateSchillingerResultant(3, 4);
console.log(schillingerCell);