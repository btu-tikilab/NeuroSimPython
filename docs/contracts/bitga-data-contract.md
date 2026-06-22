# BitGA Data Contract

This is the "agreement" between backend (Unit A) and frontend (Unit B).

Frontend will send requests in this format.
Backend promises to return responses in this format.

Once frozen, no changes without approval.

---

## 1. Application Information

**Endpoint:** `GET /app-info`

Frontend receives:

```json
{
  "appName": "NeuroSim",
  "version": "1.0.0"
}
```

## 2. Available Playgrounds

**Endpoint:** `GET /playgrounds`

Frontend receives:

```json
{
  "playgrounds": [
    {
      "id": "bitga",
      "name": "BitGA",
      "description": "Binary Genetic Algorithm Playground"
    },
    {
      "id": "graphga",
      "name": "GraphGA",
      "description": "Graph Based Genetic Algorithm Playground"
    }
  ]
}
```

## 3. BitGA Problems List

**Endpoint:** `GET /bitga/problems`

Frontend receives:

```json
{
  "problems": [
    {
      "id": "onemax",
      "name": "OneMax",
      "description": "Maximize number of 1s in bitstring"
    },
    {
      "id": "knapsack",
      "name": "0/1 Knapsack",
      "description": "Maximize value while respecting weight"
    }
  ]
}
```

## 4. BitGA Configuration (Frontend sends to Backend)

Frontend sends this to start a run:

```json
{
  "problem": "onemax",
  "bitstringLength": 20,
  "populationSize": 100,
  "generations": 100,
  "mutationRate": 0.05,
  "tournamentSize": 3,
  "seed": 42
}
```

Field Descriptions:

* `problem`: Which problem to solve (onemax, knapsack)
* `bitstringLength`: How many bits in the solution
* `populationSize`: How many individuals per generation
* `generations`: How many generations to run
* `mutationRate`: Probability of flipping each bit (0-1)
* `tournamentSize`: Tournament selection size (2-5)
* `seed`: Random seed for reproducibility

## 5. Generation Snapshot (Live Progress)

**Endpoint:** `GET /bitga/generation/{generationId}`

Backend returns current generation stats:

```json
{
  "generation": 50,
  "bestFitness": 0.74,
  "avgFitness": 0.51,
  "worstFitness": 0.23,
  "bestGenome": [1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1]
}
```

## 6. Complete Run Result (Final Response)

**Endpoint:** `POST /bitga/run`

Frontend sends config (see #4) → Backend runs GA → Returns:

```json
{
  "runId": "run_abc12345",
  "bestFitness": 18.0,
  "bestSolution": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
  "generationsToConvergence": 35,
  "totalGenerations": 100,
  "convergenceHistory": [
    {
      "generation": 0,
      "bestFitness": 9.0,
      "avgFitness": 5.2,
      "worstFitness": 2.0,
      "bestGenome": [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0]
    },
    {
      "generation": 1,
      "bestFitness": 10.0,
      "avgFitness": 5.8,
      "worstFitness": 2.0,
      "bestGenome": [1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0]
    },
    ...
    {
      "generation": 99,
      "bestFitness": 18.0,
      "avgFitness": 16.2,
      "worstFitness": 14.0,
      "bestGenome": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0]
    }
  ],
  "executionTimeSeconds": 2.34
}
```

Field Descriptions:

* `runId`: Unique ID for this run
* `bestFitness`: Best fitness found (number of 1s for OneMax)
* `bestSolution`: The best bitstring found
* `generationsToConvergence`: When best solution was found
* `totalGenerations`: Total generations run
* `convergenceHistory`: List of every generation (for progress chart)
* `executionTimeSeconds`: How long it took

## 7. Bitstring Genome Schema (For Visualization)

**Endpoint:** `GET /bitga/genome/{runId}/{generationId}`

Frontend receives (for displaying solution):

```json
{
  "bitstring": [1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1],
  "fitness": 0.97,
  "generation": 187,
  "problem": "onemax"
}
```
