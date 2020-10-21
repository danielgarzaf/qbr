#!/usr/bin/env bash
echo "Running cube scan..."
./qbr.py
echo "Cube state set!"
./setCubeState.py
sleep 1
echo "Solving cube..."
./setCubeMoves.py