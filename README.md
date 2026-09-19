# NeuroSafe Foundations

## Safety Gate for Simulated Assistive Robot Commands

This educational project compares a simple simulated assistive robot with and without a confidence-based safety gate.

The inputs are **synthetic commands** (`left`, `right`, and `stop`) and **synthetic confidence scores**. They are not real EEG, a medical device, a validated decoder, or a proven physical robot safety system.

## Research question

How does a confidence threshold change command execution and unsafe movement in a small deterministic command stream?

See `research-question.md` and `experiment-log-template.md`.

## Setup

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

## Run

```powershell
python -m neurosafe.simulate
pytest
```

The run writes `results/experiment_log.csv` and `results/command_comparison.png`. Generated results are ignored by Git.

## Project map

- `neurosafe/safety_gate.py`: command validation, confidence gate, and robot state.
- `neurosafe/simulate.py`: reproducible synthetic experiment and metrics.
- `tests/`: focused safety and behavior tests.
- `results/`: local generated output, not source code.

## Limitations

This is a small simulation for learning. It does not model EEG acquisition, signal processing, human factors, real robot dynamics, emergency certification, or clinical safety.
