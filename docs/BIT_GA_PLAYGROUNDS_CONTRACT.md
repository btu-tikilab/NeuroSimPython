<!-- AUTH:DEVNEUROSIM:7A3F9E2B | docs/BIT_GA_PLAYGROUNDS_CONTRACT.md -->
# Evolutionary Playgrounds Data Contract

This document specifies the communication protocol, parameters, and payload schemas between the React frontend UI and the FastAPI backend engine for the NeuroSim evolutionary algorithm playgrounds.

---

## 1. Playground Directory Info
**Endpoint:** `GET /api/playgrounds`  
**Description:** Retrieves the metadata of all available evolutionary playgrounds.  
**Response Schema:**
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
    },
    {
      "id": "tsp",
      "name": "TSP",
      "description": "Travelling Salesman Problem Playground"
    },
    {
      "id": "maze_neat",
      "name": "Maze NEAT",
      "description": "Neuroevolution Maze Solver Playground"
    }
  ]
}
```

---

## 2. GraphGA Contract

### Run Experiment
**Endpoint:** `POST /api/graphga/run`  
**Description:** Runs a complete evolutionary execution cycle on a graph genome using the provided configuration parameters.  
**Request Payload Schema:**
```json
{
  "populationSize": 100,
  "generations": 250,
  "mutationRate": 0.02,
  "crossoverRate": 0.80,
  "seed": 42,
  "nodeCount": 20,
  "graphMode": "Directed",
  "allowSelfLoop": false,
  "parentSelection": "Tournament",
  "tournamentSize": 5,
  "crossoverType": "Uniform",
  "mutationType": "Bit Flip",
  "eliteCount": 2,
  "targetFitness": 100.0,
  "connectivityBonus": 10.0,
  "sparsityPenalty": 2.0
}
```
**Response Payload Schema:**
```json
{
  "generation": 250,
  "bestFitness": 98.4,
  "avgFitness": 76.2,
  "worstFitness": 15.0
}
```

### Best Genome Extraction
**Endpoint:** `GET /api/graphga/best`  
**Description:** Returns the best genome found from the last execution run, serialized in a format compatible with cytoscape.js.  
**Response Schema:**
```json
{
  "nodes": [
    { "id": "n0", "type": "input", "value": 1.0 },
    { "id": "n1", "type": "hidden", "value": 0.0 },
    { "id": "n2", "type": "output", "value": 1.0 }
  ],
  "edges": [
    { "source": "n0", "target": "n1", "weight": 1.0 },
    { "source": "n1", "target": "n2", "weight": 1.0 }
  ],
  "fitness": 98.4,
  "generation": 250
}
```

### Evolution History
**Endpoint:** `GET /api/graphga/history`  
**Description:** Retrieves the fitness trace across all generations of the last run.  
**Response Schema:**
```json
[
  {
    "generation": 0,
    "bestFitness": 45.2,
    "avgFitness": 20.1,
    "worstFitness": 2.0
  },
  {
    "generation": 1,
    "bestFitness": 48.0,
    "avgFitness": 24.5,
    "worstFitness": 4.0
  }
]
```

### Generation Snapshot
**Endpoint:** `GET /api/graphga/snapshot/{generation}`  
**Description:** Returns the snapshot info and best genome layout at a specific generation.  
**Response Schema:**
```json
{
  "generation": 120,
  "bestFitness": 85.0,
  "avgFitness": 60.5,
  "worstFitness": 10.0,
  "bestGenome": {
    "nodes": [ ... ],
    "edges": [ ... ],
    "fitness": 85.0,
    "generation": 120
  }
}
```
