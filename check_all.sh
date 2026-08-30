#!/usr/bin/env bash
# AUTH:DEVNEUROSIM:7A3F9E2B | check_all.sh
# NeuroSim Master Test & Compliance Runner

echo "============================================="
echo "   NeuroSim Test & Compliance Suite Runner"
echo "============================================="
echo ""

# 1. Run Unit & Integration Tests
echo "[1/2] Running all unit and integration tests..."
PYTHONPATH=NeuroSim.Engine/src python -m unittest discover -s NeuroSim.Problems/TestSuites -p "test_backend.py" -v
TEST_EXIT=$?

if [ $TEST_EXIT -ne 0 ]; then
    echo ""
    echo "❌ ERROR: One or more test cases failed! Please fix the errors above."
    exit $TEST_EXIT
fi

echo "✓ All tests passed successfully!"
echo ""

# 2. Run Compliance Checker
echo "[2/2] Running project compliance checks..."
bash scripts/compliance.sh
COMP_EXIT=$?

if [ $COMP_EXIT -ne 0 ]; then
    echo ""
    echo "❌ ERROR: Compliance check failed!"
    exit $COMP_EXIT
fi

echo ""
echo "============================================="
echo " 🎉 SUCCESS: All tests passed and compliance is PERFECT!"
echo "============================================="
