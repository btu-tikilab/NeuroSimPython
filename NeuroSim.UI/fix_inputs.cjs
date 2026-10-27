const fs = require('fs');

const filePath = "/Users/samruddhipowar5gmail.com/Desktop/Neuro/NeuroSim.UI/src/Pages/GraphGA/components/Configuration.jsx";
let content = fs.readFileSync(filePath, 'utf8');

const replacements = [
    [
        'type="number"\n                  value={nodeCount}\n                  onChange={(e) => setNodeCount(Number(e.target.value))}',
        'type="number"\n                  min="1"\n                  value={nodeCount}\n                  onChange={(e) => setNodeCount(Math.max(1, Number(e.target.value)))}'
    ],
    [
        'type="number"\n                  value={randomSeed}\n                  onChange={(e) => setRandomSeed(Number(e.target.value))}',
        'type="number"\n                  min="0"\n                  value={randomSeed}\n                  onChange={(e) => setRandomSeed(Math.max(0, Number(e.target.value)))}'
    ],
    [
        'type="number" \n                  value={connectivityBonus} \n                  onChange={(e) => setConnectivityBonus(Number(e.target.value))}',
        'type="number" \n                  min="0"\n                  value={connectivityBonus} \n                  onChange={(e) => setConnectivityBonus(Math.max(0, Number(e.target.value)))}'
    ],
    [
        'type="number" \n                  value={sparsityPenalty} \n                  onChange={(e) => setSparsityPenalty(Number(e.target.value))}',
        'type="number" \n                  min="0"\n                  value={sparsityPenalty} \n                  onChange={(e) => setSparsityPenalty(Math.max(0, Number(e.target.value)))}'
    ],
    [
        'type="number" \n                  value={populationSize} \n                  onChange={(e) => setPopulationSize(Number(e.target.value))}',
        'type="number" \n                  min="2"\n                  value={populationSize} \n                  onChange={(e) => setPopulationSize(Math.max(2, Number(e.target.value)))}'
    ],
    [
        'type="number" \n                  value={generations} \n                  onChange={(e) => setGenerations(Number(e.target.value))}',
        'type="number" \n                  min="1"\n                  value={generations} \n                  onChange={(e) => setGenerations(Math.max(1, Number(e.target.value)))}'
    ],
    [
        'type="number" \n                  value={tournamentSize} \n                  onChange={(e) => setTournamentSize(Number(e.target.value))}',
        'type="number" \n                  min="1"\n                  value={tournamentSize} \n                  onChange={(e) => setTournamentSize(Math.max(1, Number(e.target.value)))}'
    ],
    [
        'type="number" \n                  step="0.05"\n                  value={crossoverRate} \n                  onChange={(e) => setCrossoverRate(Number(e.target.value))}',
        'type="number" \n                  step="0.05"\n                  min="0" max="1"\n                  value={crossoverRate} \n                  onChange={(e) => setCrossoverRate(Math.max(0, Math.min(1, Number(e.target.value))))}'
    ],
    [
        'type="number" \n                  step="0.01"\n                  value={mutationRate} \n                  onChange={(e) => setMutationRate(Number(e.target.value))}',
        'type="number" \n                  step="0.01"\n                  min="0" max="1"\n                  value={mutationRate} \n                  onChange={(e) => setMutationRate(Math.max(0, Math.min(1, Number(e.target.value))))}'
    ],
    [
        'type="number" \n                  value={eliteCount} \n                  onChange={(e) => setEliteCount(Number(e.target.value))}',
        'type="number" \n                  min="0"\n                  value={eliteCount} \n                  onChange={(e) => setEliteCount(Math.max(0, Number(e.target.value)))}'
    ],
    [
        'type="number" \n                  value={targetFitness} \n                  onChange={(e) => setTargetFitness(Number(e.target.value))}',
        'type="number" \n                  min="0"\n                  value={targetFitness} \n                  onChange={(e) => setTargetFitness(Math.max(0, Number(e.target.value)))}'
    ]
];

for (const [oldStr, newStr] of replacements) {
    content = content.replace(oldStr, newStr);
}

fs.writeFileSync(filePath, content, 'utf8');
console.log("Done");
