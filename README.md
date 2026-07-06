# Microgrid-Simulator

A modular chronological 7-day chronological microgrid simulation modeling
shared rooftop solar arrays, centralized commercial battery storage,
dynamic apartment loads, and utility grid interaction.

The simulator incorporates stochastic weather, dust accumulation,
scheduled maintenance, battery energy management, and an interactive
visualization engine for analyzing system performance.

------------------------------------------------------------------------

# Detailed Component Architecture

The software is organized into modular components separating
configuration, environmental models, physical equations, simulation
logic, and visualization.

## 1. `sim_config.py` --- System Configuration

Centralized source of truth for all simulation parameters.

### Solar Parameters

-   Panel Rating: `100.0 kW`
-   Panel Efficiency: `0.82`

### Battery Parameters

-   Capacity: `200.0 kWh`
-   Charge Efficiency: `95%`
-   Discharge Efficiency: `95%`
-   Maximum Charge Rate
-   Maximum Discharge Rate
-   Minimum State of Charge: `40%`

### Load Parameters

-   Base apartment demand
-   Afternoon Gaussian demand peak
-   Evening Gaussian demand peak

### Grid Parameters

-   Grid buy tariff (₹/kWh)
-   Grid sell tariff (₹/kWh)

------------------------------------------------------------------------

## 2. `weather.py` --- Stochastic Weather Engine

-   Markov-chain weather transitions
-   Dust accumulation
-   Rain cleaning events
-   Scheduled manual cleaning
-   Transient cloud events

------------------------------------------------------------------------

## 3. `models.py` --- Physical & Mathematical Models

### Solar Generation Model

``` text
Actual Power =
Panel Rating
× Panel Efficiency
× sin(π(t − Sunrise)/(Sunset − Sunrise))
× (1 − Soiling Loss)
× (1 − Cloud Loss)
```

### Apartment Load Model

``` text
Load(t) =
Base Load
+ Afternoon Peak × exp(-(t − μ₁)² / (2σ₁²))
+ Evening Peak × exp(-(t − μ₂)² / (2σ₂²))
```

### Battery Controller

-   Capacity limits
-   Charge/discharge rate limits
-   Minimum SoC reserve
-   Round-trip efficiency losses

------------------------------------------------------------------------

## 4. `simulation.py`

Handles hourly weather updates, solar generation, load calculation,
battery dispatch, grid interaction and energy accounting.

------------------------------------------------------------------------

## 5. `main.py`

Runs the simulation and launches the interactive visualization.

------------------------------------------------------------------------

# Systems Engineering Metrics

## Capacity Ratio

``` text
Capacity Ratio (%) =
(Total Actual Solar Generation
 / Total Clear-Sky Solar Generation)
× 100
```

## Self-Sufficiency Index

``` text
SSI (%) =
((Total Load − Total Grid Import)
/ Total Load)
× 100
```

------------------------------------------------------------------------

# Manual Cleaning Protocol

``` text
Dust > 25%
      │
      ▼
Schedule cleaning
      │
      ▼
6:00–8:00 AM
Solar OFFLINE
      │
      ▼
Dust reset to 0%
```

------------------------------------------------------------------------

# Project Structure

``` text
Microgrid-Simulator/
├── sim_config.py
├── weather.py
├── models.py
├── simulation.py
├── main.py
├── requirements.txt
└── README.md
```

# Installation

``` bash
pip install -r requirements.txt
```

# Running

``` bash
python main.py
```

# Interactive Visualization

Use the keyboard:

-   ← Previous graph
-   → Next graph

Visualizations: 1. Highest Solar Production Day 2. Lowest Solar
Production Day 3. Daily Mean Solar Generation 4. Weekly Battery State of
Charge 5. Utility Grid Interaction

# Features

-   7-day chronological simulation
-   Markov-chain weather
-   Dynamic cloud events
-   Dust accumulation and cleaning
-   Gaussian apartment load model
-   Battery energy storage
-   Grid import/export
-   Interactive visualization
-   Modular architecture
