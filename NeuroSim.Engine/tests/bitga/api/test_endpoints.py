# NeuroSim.Engine/tests/api/test_bitga_endpoints.py
import pytest
from fastapi.testclient import TestClient

from api.main import app

client = TestClient(app)


class TestBasicEndpoints:
    def test_app_info(self):
        r = client.get("/app-info")
        assert r.status_code == 200
        assert r.json()["appName"] == "NeuroSim"

    def test_playgrounds_lists_bitga_and_graphga(self):
        r = client.get("/playgrounds")
        assert r.status_code == 200
        ids = [p["id"] for p in r.json()["playgrounds"]]
        assert "bitga" in ids
        assert "graphga" in ids

    def test_bitga_problems_lists_onemax_and_knapsack(self):
        r = client.get("/bitga/problems")
        assert r.status_code == 200
        ids = [p["id"] for p in r.json()["problems"]]
        assert "onemax" in ids
        assert "knapsack" in ids


class TestRunOneMax:
    def test_basic_run_succeeds(self):
        payload = {
            "problem": "onemax",
            "bitstringLength": 20,
            "populationSize": 50,
            "generations": 50,
            "seed": 42,
        }
        r = client.post("/bitga/run", json=payload)
        assert r.status_code == 200
        data = r.json()
        assert len(data["bestSolution"]) == 20
        assert data["bestFitness"] > 0
        assert data["totalGenerations"] == 50
        assert len(data["convergenceHistory"]) == 51
        assert data["executionTimeSeconds"] > 0
        assert data["runId"].startswith("run_")
        assert isinstance(data["isOptimal"], bool)

    def test_reproducible_with_same_seed(self):
        payload = {"problem": "onemax", "bitstringLength": 15, "populationSize": 30, "generations": 20, "seed": 7}
        r1 = client.post("/bitga/run", json=payload).json()
        r2 = client.post("/bitga/run", json=payload).json()
        assert r1["bestSolution"] == r2["bestSolution"]
        assert r1["bestFitness"] == r2["bestFitness"]

    def test_well_trained_run_reports_optimal(self):
        payload = {"problem": "onemax", "bitstringLength": 12, "populationSize": 60, "generations": 100, "seed": 42}
        r = client.post("/bitga/run", json=payload)
        data = r.json()
        assert data["bestFitness"] == 12
        assert data["isOptimal"] is True

    def test_missing_required_bitstring_length_returns_422(self):
        r = client.post("/bitga/run", json={"problem": "onemax"})
        assert r.status_code == 422

    def test_non_positive_bitstring_length_returns_400(self):
        r = client.post("/bitga/run", json={"problem": "onemax", "bitstringLength": 0})
        assert r.status_code == 400


class TestRunKnapsack:
    def _valid_payload(self, **overrides):
        payload = {
            "problem": "knapsack",
            "bitstringLength": 3,
            "values": [10, 20, 30],
            "weights": [5, 10, 15],
            "capacity": 20,
            "seed": 42,
            "populationSize": 50,
            "generations": 50,
        }
        payload.update(overrides)
        return payload

    def test_basic_run_succeeds(self):
        r = client.post("/bitga/run", json=self._valid_payload())
        assert r.status_code == 200
        data = r.json()
        assert len(data["bestSolution"]) == 3

    def test_finds_true_optimum_on_easy_instance(self):
        r = client.post("/bitga/run", json=self._valid_payload())
        data = r.json()
        assert data["bestFitness"] == 40
        assert data["isOptimal"] is True

    def test_missing_values_weights_capacity_returns_400(self):
        r = client.post("/bitga/run", json={"problem": "knapsack", "bitstringLength": 3})
        assert r.status_code == 400
        assert "requires" in r.json()["detail"]

    def test_values_length_mismatch_returns_400(self):
        payload = self._valid_payload(values=[10, 20])
        r = client.post("/bitga/run", json=payload)
        assert r.status_code == 400
        assert "must equal" in r.json()["detail"]

    def test_negative_value_returns_400(self):
        payload = self._valid_payload(values=[10, -5, 30])
        r = client.post("/bitga/run", json=payload)
        assert r.status_code == 400

    def test_negative_weight_returns_400(self):
        payload = self._valid_payload(weights=[5, -10, 15])
        r = client.post("/bitga/run", json=payload)
        assert r.status_code == 400

    def test_non_positive_capacity_returns_400(self):
        payload = self._valid_payload(capacity=0)
        r = client.post("/bitga/run", json=payload)
        assert r.status_code == 400

    def test_too_many_items_returns_400(self):
        n = 201
        payload = self._valid_payload(
            bitstringLength=n, values=[1] * n, weights=[1] * n, capacity=10,
        )
        r = client.post("/bitga/run", json=payload)
        assert r.status_code == 400
        assert "too many items" in r.json()["detail"]

    def test_exactly_at_item_limit_succeeds(self):
        n = 200
        payload = self._valid_payload(
            bitstringLength=n, values=[1] * n, weights=[1] * n, capacity=10,
            populationSize=10, generations=2,
        )
        r = client.post("/bitga/run", json=payload)
        assert r.status_code == 200

    def test_capacity_too_large_returns_400(self):
        payload = self._valid_payload(capacity=100_001)
        r = client.post("/bitga/run", json=payload)
        assert r.status_code == 400
        assert "capacity too large" in r.json()["detail"]


class TestUnknownTypes:
    def test_unknown_problem_type_returns_400(self):
        r = client.post("/bitga/run", json={"problem": "traveling_salesman", "bitstringLength": 10})
        assert r.status_code == 400

    def test_unknown_crossover_type_returns_400(self):
        r = client.post("/bitga/run", json={
            "problem": "onemax", "bitstringLength": 10, "crossoverType": "Not Real",
        })
        assert r.status_code == 400

    def test_unknown_mutation_type_returns_400(self):
        r = client.post("/bitga/run", json={
            "problem": "onemax", "bitstringLength": 10, "mutationType": "Not Real",
        })
        assert r.status_code == 400


class TestAlternateOperators:
    def test_non_default_crossover_and_mutation_work(self):
        payload = {
            "problem": "onemax",
            "bitstringLength": 16,
            "populationSize": 20,
            "generations": 15,
            "seed": 3,
            "crossoverType": "Two Point",
            "mutationType": "Swap",
            "mutationRate": 0.1,
        }
        r = client.post("/bitga/run", json=payload)
        assert r.status_code == 200
        assert len(r.json()["bestSolution"]) == 16