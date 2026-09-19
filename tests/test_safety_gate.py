import pytest

from neurosafe.safety_gate import Command, Robot, SafetyGate, execute


def test_gate_rejects_low_confidence_command():
    robot = Robot()
    executed = execute(Command("right", 0.74), robot, SafetyGate(0.75))
    assert not executed
    assert robot.position == 0


def test_gate_allows_threshold_confidence():
    robot = Robot()
    executed = execute(Command("right", 0.75), robot, SafetyGate(0.75))
    assert executed
    assert robot.position == 1


def test_stop_is_executed_when_approved():
    robot = Robot(position=2)
    execute(Command("stop", 0.90), robot, SafetyGate(0.75))
    assert robot.stopped
    assert robot.position == 2


def test_invalid_inputs_are_rejected():
    with pytest.raises(ValueError):
        Command("forward", 0.9)
    with pytest.raises(ValueError):
        Command("left", 1.1)
