from dataclasses import dataclass

VALID_COMMANDS = {"left", "right", "stop"}


@dataclass(frozen=True)
class Command:
    name: str
    confidence: float

    def __post_init__(self) -> None:
        if self.name not in VALID_COMMANDS:
            raise ValueError(f"Unknown command: {self.name}")
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("Confidence must be between 0 and 1")


class SafetyGate:
    def __init__(self, threshold: float = 0.75) -> None:
        if not 0.0 <= threshold <= 1.0:
            raise ValueError("Threshold must be between 0 and 1")
        self.threshold = threshold

    def approve(self, command: Command) -> bool:
        return command.confidence >= self.threshold


@dataclass
class Robot:
    position: int = 0
    stopped: bool = False

    def apply(self, command: Command) -> None:
        if command.name == "left":
            self.position -= 1
            self.stopped = False
        elif command.name == "right":
            self.position += 1
            self.stopped = False
        else:
            self.stopped = True


def execute(command: Command, robot: Robot, gate: SafetyGate | None = None) -> bool:
    """Apply a command and return whether it was executed."""
    if gate is not None and not gate.approve(command):
        return False
    robot.apply(command)
    return True
