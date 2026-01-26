from maths.root_finding.bisection import Bisection
from modes.math_root_finding_visualizer import run_math_root_finding_visualizer

def run_math_root_finding_mode(screen):
    f = lambda x: x**3 - x - 2
    algo = Bisection(f, a=1, b=2)

    run_math_root_finding_visualizer(
        screen,
        algo=algo,
        f=f,
        x_range=(0, 3)
    )
