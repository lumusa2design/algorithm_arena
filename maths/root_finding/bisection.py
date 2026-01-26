class Bisection:
    name = "Bisection"

    def __init__(self, f, a, b, tol=1e-4, max_iter=50):
        self.f = f
        self.a = a
        self.b = b
        self.tol = tol
        self.max_iter = max_iter

    def run(self):
        a, b = self.a, self.b
        fa, fb = self.f(a), self.f(b)

        if fa * fb > 0:
            raise ValueError("f(a) y f(b) deben tener signos opuestos")

        for k in range(1, self.max_iter + 1):
            m = (a + b) / 2
            fm = self.f(m)

            yield {
                "iter": k,
                "a": a, "b": b, "m": m,
                "fa": fa, "fb": fb, "fm": fm
            }

            if abs(fm) < self.tol or abs(b - a) < self.tol:
                yield {"done": True, "root": m}
                return

            if fa * fm < 0:
                b, fb = m, fm
            else:
                a, fa = m, fm
