import csv
from pathlib import Path

import matplotlib.pyplot as plt

from .safety_gate import Command, Robot, SafetyGate, execute


SYNTHETIC_COMMANDS = [
    Command("right", 0.92),
    Command("left", 0.61),
    Command("right", 0.81),
    Command("left", 0.42),
    Command("stop", 0.58),
    Command("right", 0.77),
    Command("left", 0.69),
    Command("stop", 0.95),
]


def run_trial(commands: list[Command], gate: SafetyGate | None = None) -> tuple[list[dict], dict]:
    robot = Robot()
    rows = []
    rejected = 0
    for index, command in enumerate(commands, start=1):
        before = robot.position
        executed = execute(command, robot, gate)
        rejected += int(not executed)
        rows.append(
            {
                "step": index,
                "command": command.name,
                "confidence": command.confidence,
                "executed": executed,
                "position": robot.position,
                "movement": robot.position - before,
            }
        )
    metrics = {
        "executed_commands": sum(row["executed"] for row in rows),
        "movement_steps": sum(abs(row["movement"]) for row in rows),
        "rejected_commands": rejected,
    }
    return rows, metrics


def save_results(output_dir: Path, ungated_rows: list[dict], gated_rows: list[dict], metrics: dict) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    log_path = output_dir / "experiment_log.csv"
    with log_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["mode", *ungated_rows[0].keys()])
        writer.writeheader()
        for mode, rows in (("without_gate", ungated_rows), ("with_gate", gated_rows)):
            for row in rows:
                writer.writerow({"mode": mode, **row})

    labels = ["executed commands", "movement steps", "rejected commands"]
    without_gate = [metrics["without_gate"][key] for key in ("executed_commands", "movement_steps", "rejected_commands")]
    with_gate = [metrics["with_gate"][key] for key in ("executed_commands", "movement_steps", "rejected_commands")]
    positions_without = [row["position"] for row in ungated_rows]
    positions_with = [row["position"] for row in gated_rows]

    figure, axes = plt.subplots(1, 2, figsize=(9, 3.8))
    axes[0].bar(labels, without_gate, label="without gate")
    axes[0].bar(labels, with_gate, alpha=0.75, label="with gate")
    axes[0].set_ylabel("count")
    axes[0].tick_params(axis="x", rotation=25)
    axes[0].legend()
    axes[0].set_title("Behavior measures")
    axes[1].plot(range(1, len(positions_without) + 1), positions_without, marker="o", label="without gate")
    axes[1].plot(range(1, len(positions_with) + 1), positions_with, marker="o", label="with gate")
    axes[1].set_xlabel("command step")
    axes[1].set_ylabel("robot position")
    axes[1].set_title("Simulated position")
    axes[1].legend()
    figure.tight_layout()
    figure.savefig(output_dir / "command_comparison.png", dpi=140)
    plt.close(figure)


def main() -> None:
    output_dir = Path(__file__).parents[1] / "results"
    ungated_rows, ungated_metrics = run_trial(SYNTHETIC_COMMANDS)
    gated_rows, gated_metrics = run_trial(SYNTHETIC_COMMANDS, SafetyGate(0.75))
    metrics = {"without_gate": ungated_metrics, "with_gate": gated_metrics}
    save_results(output_dir, ungated_rows, gated_rows, metrics)
    print("Synthetic Safety Gate experiment")
    print(f"Without gate: {ungated_metrics}")
    print(f"With gate (threshold=0.75): {gated_metrics}")
    print(f"Results saved to {output_dir}")


if __name__ == "__main__":
    main()
