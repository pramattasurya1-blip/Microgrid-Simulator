# Microgrid-Simulator

A high-fidelity, 7-day chronological microgrid simulation modeling shared rooftop solar arrays, centralized commercial battery storage, dynamic loads, and utility grid interdependency.

The simulator incorporates realistic environmental constraints, stochastic dust accumulation, automated maintenance scheduling, and an interactive multi-plot visualization engine for analyzing system performance.

---

# Detailed Component Architecture

The software is refactored into a modular package layout, separating configuration constants, stochastic environmental models, electrical performance equations, simulation logic, and visualization.

## 1. `sim_config.py` — System Configuration

Centralized source of truth for all simulation parameters.

### Solar Parameters
- Panel Rating: `100.0 kW`
- Panel Efficiency: `0.82`

### Battery Parameters
- Capacity: `200.0 kWh`
- Charge Efficiency: `95%`
- Discharge Efficiency: `95%`
- Maximum Charge Rate
- Maximum Discharge Rate
- Minimum State of Charge (40%)

### Load Parameters
- Base apartment demand
- Afternoon Gaussian demand peak
- Evening Gaussian demand peak

### Grid Parameters
- Grid buy tariff (₹/kWh)
- Grid sell tariff (₹/kWh)

---

## 2. `weather.py` — Stochastic Weather Engine

Simulates environmental effects throughout the seven-day simulation.

### Features

- Markov-chain weather transitions
- Dust accumulation
- Rain cleaning events
- Manual cleaning scheduling
- Transient cloud events

---

## 3. `models.py` — Physical & Mathematical Models

Contains the mathematical models governing the microgrid.

### Solar Generation Model

The solar array follows a half-sine irradiance profile:

\[
P_{actual}=P_{rating}\eta
\sin\left(
\frac{\pi(t-t_{sunrise})}
{t_{sunset}-t_{sunrise}}
\right)
(1-L_{dust})
(1-L_{cloud})
\]

---

### Apartment Load Model

Community demand is represented using two Gaussian peaks:

\[
Load(t)=Base
+
A_1e^{-\frac{(t-\mu_1)^2}{2\sigma_1^2}}
+
A_2e^{-\frac{(t-\mu_2)^2}{2\sigma_2^2}}
\]

representing:

- Afternoon cooking / cooling peak
- Evening residential activity peak

---

### Battery Controller

The battery controller enforces

- Capacity limits
- Charge-rate limits
- Discharge-rate limits
- Minimum State-of-Charge reserve
- Round-trip efficiency losses

---

## 4. `simulation.py` — Chronological Simulation Engine

Coordinates the hourly simulation.

Responsibilities include:

- Weather updates
- Dust accumulation
- Rain cleaning
- Solar generation
- Load calculation
- Battery charging/discharging
- Grid import/export
- Daily statistics
- Weekly energy accounting

---

## 5. `main.py` — Runtime Controller

Responsible for

- Launching the simulation
- Printing performance statistics
- Initializing the interactive visualization interface

---

# Systems Engineering Metrics

The simulator computes several operational metrics beyond raw electrical measurements.

---

## Capacity Ratio

Compares actual solar production against an ideal clear-sky reference.

\[
Capacity\ Ratio=
\frac{\sum P_{actual}}
{\int P_{clear}\,dt}
\times100
\]

The ratio decreases because of

- Cloud cover
- Dust accumulation
- Scheduled maintenance downtime

---

## Self-Sufficiency Index (SSI)

Measures how much of the apartment load is supplied without purchasing electricity from the utility.

\[
SSI=
\frac{
Load_{total}-GridImport_{total}
}
{
Load_{total}
}
\times100
\]

### Interpretation

| SSI | Status |
|------|--------|
| >60% | High self-sufficiency |
| 35–60% | Moderate |
| <35% | Heavy grid dependence |

---

# Manual Cleaning Protocol

```
Day X
│
├── Dust accumulates
│
├── Dust > 25% ?
│
└── Yes
      │
      ▼
Schedule maintenance

Day X+1

06:00  Solar OFFLINE
07:00  Cleaning continues
08:00  Solar resumes
        Dust reset to 0%
```

Whenever dust exceeds **25%**, a maintenance event is scheduled.

During maintenance:

- Solar production is forced to **0 kW**
- Duration: **6:00 AM – 8:00 AM**
- Battery and utility grid supply the apartment load
- Dust accumulation resets after cleaning

---

# Project Structure

```
Microgrid-Simulator/
│
├── sim_config.py
├── weather.py
├── models.py
├── simulation.py
├── main.py
├── requirements.txt
└── README.md
```

---

# Installation

Clone the repository and install the dependencies.

```bash
pip install -r requirements.txt
```

---

# Running the Simulator

```bash
python main.py
```

---

# Interactive Visualization

After the simulation finishes, an interactive Matplotlib window opens.

Click inside the graph window and use:

- **← Left Arrow** — Previous graph
- **→ Right Arrow** — Next graph

---

## Available Visualizations

### 1. Highest Solar Production Day

Displays

- Solar generation
- Apartment load
- Battery State of Charge

---

### 2. Lowest Solar Production Day

Displays the worst-performing day caused by poor weather or maintenance.

---

### 3. Daily Mean Solar Generation

Shows the average solar output for each simulated day.

---

### 4. Weekly Battery State of Charge

Displays battery energy throughout the entire simulation.

---

### 5. Utility Grid Interaction

Shows

- Grid Import
- Grid Export

allowing visualization of the microgrid's dependence on the external utility network.

---

# Features

- 7-day chronological simulation
- Markov-chain weather model
- Dynamic cloud events
- Dust accumulation
- Rain cleaning
- Scheduled manual cleaning
- Gaussian apartment load model
- Battery energy storage system
- Grid import/export management
- Interactive visualization interface
- Modular project architecture
