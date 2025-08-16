# Simulation of Parcel Delivery Time

A Monte Carlo simulation exploring how weather events, labor strikes, and network congestion affect parcel delivery time for a hub-to-node route. The work supports the WER module (Spring 2025, FHNW/HSI).

## What’s inside
- `simulation_delivery.ipynb` — main notebook with the model, analysis, and figures.
- `utils/` — helper data and scripts (e.g., strike data, weather parsing).
- `weather_data/` — raw reference datasets used to estimate event probabilities.
- `docs/` — exported HTML report from the notebook.

## Quick start
1) Create/activate a virtual environment (optional but recommended).
2) Install dependencies:
	- pip install -r requirements.txt
3) Open and run the notebook:
	- simulation_delivery.ipynb

## Notes
- Probabilities and delays combine public sources and reasonable assumptions; details are documented inline in the notebook.
- Figures and statistics are reproducible by re-running the notebook cells.