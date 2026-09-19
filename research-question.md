# Research Question

## Main question

How does a confidence threshold affect command execution and unsafe movement when a simulated assistive robot receives synthetic left, right, and stop commands?

## Hypothesis

A gate that requires confidence of at least 0.75 will reject some low-confidence commands. This should reduce false movement, while also increasing rejected commands.

## Measures

- `executed_commands`: commands that change the robot position or explicitly stop it.
- `movement_steps`: total absolute position change.
- `false_movement_events`: low-confidence non-stop commands that would move the robot without the gate.
- `rejected_commands`: commands blocked by the gate.

## Boundaries

The data are synthetic. Results do not establish EEG decoding quality, clinical benefit, or physical robot safety.
