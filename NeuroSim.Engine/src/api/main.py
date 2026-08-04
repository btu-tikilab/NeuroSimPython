from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(
    title="BitGA Engine API",
    version="1.0.0"
)

# ==================== MODELS ====================

class BitGARunRequest(BaseModel):
    """What frontend sends."""
    problem: str
    bitstringLength: int
    populationSize: int = 100
    generations: int = 100
    mutationRate: Optional[float] = None
    tournamentSize: int = 3
    seed: Optional[int] = 42

class GenerationInHistory(BaseModel):
    """Single generation result."""
    generation: int
    bestFitness: float
    avgFitness: float
    worstFitness: float
    bestGenome: List[int]

class BitGARunResponse(BaseModel):
    """Complete response after run."""
    runId: str
    bestFitness: float
    bestSolution: List[int]
    generationsToConvergence: int
    totalGenerations: int
    convergenceHistory: List[GenerationInHistory]
    executionTimeSeconds: float

# ==================== ENDPOINTS ====================

@app.get("/app-info")
def get_app_info():
    """Application information."""
    return {
        "appName": "NeuroSim",
        "version": "1.0.0"
    }

@app.get("/playgrounds")
def get_playgrounds():
    """List available playgrounds."""
    return {
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

@app.get("/bitga/problems")
def get_bitga_problems():
    """List available problems."""
    return {
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

@app.post("/bitga/run")
def run_bitga(request: BitGARunRequest) -> BitGARunResponse:
    """
    Run BitGA simulation.
    
    WEEK 1: Placeholder - returns mock data
    WEEKS 2-3: Will implement actual engine
    """
    
    # PLACEHOLDER - Real implementation in Weeks 2-3
    return BitGARunResponse(
        runId="run_placeholder_001",
        bestFitness=15.0,
        bestSolution=[1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
        generationsToConvergence=25,
        totalGenerations=100,
        convergenceHistory=[
            GenerationInHistory(
                generation=i,
                bestFitness=5.0 + (i * 0.1),
                avgFitness=3.0 + (i * 0.05),
                worstFitness=1.0 + (i * 0.02),
                bestGenome=[1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0]
            )
            for i in range(100)
        ],
        executionTimeSeconds=2.34
    )

@app.get("/bitga/generation/{generationId}")
def get_generation_snapshot(generationId: int):
    """Get generation stats."""
    return {
        "generation": generationId,
        "bestFitness": 0.74,
        "avgFitness": 0.51,
        "worstFitness": 0.23,
        "bestGenome": [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0]
    }

@app.get("/bitga/genome/{runId}/{generationId}")
def get_genome(runId: str, generationId: int):
    """Get genome for visualization."""
    return {
        "bitstring": [1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1],
        "fitness": 0.97,
        "generation": generationId,
        "problem": "onemax"
    }

# ==================== STARTUP ====================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)