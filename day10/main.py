from pathlib import Path
from typing import List, Tuple, Optional, Set, Callable

cycles = {
    "noop": 1,
    "addx": 2
}

apply = {
    "noop": lambda x, reg: reg,
    "addx": lambda x, reg: x + reg
}


def run_commands(commands: List[Tuple[str, Optional[int]]], called_every_cycle: Callable[[int, int], None]):
    x = 1
    cycle = 1
    for op, arg in commands:
        for _ in range(cycles[op]):
            called_every_cycle(x, cycle)
            cycle += 1
        x = apply[op](arg, x)


class InterestingSignalStrengthBuilder:
    def __init__(self):
        self.interesting_cycles = {20, 60, 100, 140, 180, 220}
        self.interesting_signal_strengths = []

    def capture_signal_strength_if_interesting(self, x, cycle):
        if cycle in self.interesting_cycles:
            self.interesting_signal_strengths.append(x * cycle)


class CRTRenderBuilder:
    def __init__(self):
        self.render = ""

    def render_cycle(self, x, cycle):
        if cycle != 1 and cycle % 40 == 1:
            self.render += "\n"
        if abs((cycle - 1) % 40 - x) <= 1:
            self.render += "#"
        else:
            self.render += "."


def main():
    input_str = Path("input.txt").read_text()
    commands = [(cmd[0], int(cmd[1]) if len(cmd) == 2 else None) for cmd in
                [cmd.split() for cmd in input_str.splitlines()]]

    interesting_signal_strength_builder = InterestingSignalStrengthBuilder()
    run_commands(commands, interesting_signal_strength_builder.capture_signal_strength_if_interesting)
    print(f"Sum of interesting signal strengths is {sum(interesting_signal_strength_builder.interesting_signal_strengths)}")

    crt_render_builder = CRTRenderBuilder()
    run_commands(commands, crt_render_builder.render_cycle)
    print(crt_render_builder.render)


if __name__ == "__main__":
    main()
