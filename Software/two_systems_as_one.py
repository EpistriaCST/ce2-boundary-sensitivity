"""
Emergence by boundary expansion: what CE 2.0 reports when an independent
system is appended to the declared microsystem.

Uses Jansma & Hoel's own toolkit (pymergence):
  git clone https://github.com/EI-research-group/pymergence
  run this file from the folder that contains the clone.

Part 1  The toy case: A (2 states, each stays put) and B (2 states, pure noise),
        never interacting, declared as one 4-state chain S = A x B.
Part 2  The general identity behind it: for independent A and B and any
        factorized intervention distribution,
            CP(A x B) = [log|A| CP(A) + log|B| CP(B)] / log(|A||B|)
        and the partition that coarse-grains away B is dynamically consistent
        and recovers CP(A). The emergence reported for A x B is therefore
            (log|B| / log(|A||B|)) * (CP(A) - CP(B)),
        which the analyst can raise toward CP(A) - CP(B) by enlarging B.
Part 3  Contrast with CE 1.0: effective information adds, EI(A x B) = EI(A) + EI(B).
Part 4  The full-lattice emergent hierarchy of A x B (A alone has none).
Part 5  Every maximal micro->macro path to the A-projection for |B| = 4.
Part 6  A drives B without feedback: the same emergence is reported.
Runtime: roughly two minutes.
"""
import sys, numpy as np
sys.path.insert(0, "pymergence")
from pymergence.core import (StochasticMatrix, CoarseGraining,
                             calc_CP_along_CGs, refinement_graph, delta_CP_ancestors)

def cp(T, p=None):
    return StochasticMatrix(T).effectiveness(intervention_distribution=p)  # determinism + specificity - 1

# ---------- Part 1: the toy case ----------
A = np.eye(2)
B = np.full((2, 2), 0.5)
S = StochasticMatrix(np.kron(A, B))          # states: 0=(a0,b0) 1=(a0,b1) 2=(a1,b0) 3=(a1,b1)

print("PART 1  A alone: CP =", round(cp(A), 3), "(no emergence possible)   B alone: CP =", round(cp(B), 3))
print("        A x B declared as one system: microscale CP =", round(cp(np.kron(A, B)), 3))

path = [((0,), (1,), (2,), (3,)), ((0,), (1,), (2, 3)), ((0, 1), (2, 3))]
vals = [S.coarse_grain(CoarseGraining(p)).effectiveness() for p in path]
print("        single micro->macro path (Patterns method):")
for p, v, prev in zip(path, vals, [None] + vals[:-1]):
    gain = "" if prev is None else f"  gain {v - prev:.3f}"
    print(f"          {p}: CP {v:.3f}{gain}")
print(f"          total causal emergence along the path: {vals[-1] - vals[0]:.3f}")
print("        (0,1)(2,3) is exactly 'the state of A'; dynamically consistent:",
      S.is_consistent_with(CoarseGraining(((0, 1), (2, 3)))))

cps, cgs = calc_CP_along_CGs(S)
lattice = refinement_graph(cgs)
by_node = {n: cps[str(CoarseGraining(d["partition"]))] for n, d in lattice.nodes(data=True)}
dcp = delta_CP_ancestors(lattice, by_node, allAncestors=True)
print("        full-lattice emergent hierarchy (Engineering Emergence method; not additive across branches):")
for part, v in sorted(dcp.items(), key=lambda x: -x[1]):
    if v > 1e-9 and CoarseGraining(part).n_blocks < 4:
        print(f"          {part}: dCP {v:.3f}")

# ---------- Part 2: the general identity ----------
rng = np.random.default_rng(0)
worst = 0.0
for _ in range(300):
    na, nb = rng.integers(2, 5, 2)
    Ar, Br = rng.dirichlet([0.5] * na, size=na), rng.dirichlet([0.5] * nb, size=nb)
    pa, pb = rng.dirichlet([1] * na), rng.dirichlet([1] * nb)      # arbitrary product intervention dists
    La, Lb = np.log2(na), np.log2(nb)
    lhs = cp(np.kron(Ar, Br), np.kron(pa, pb))
    rhs = (La * cp(Ar, pa) + Lb * cp(Br, pb)) / (La + Lb)
    worst = max(worst, abs(lhs - rhs))
print("\nPART 2  weighted-average identity, 300 random independent pairs, random product P(C):")
print(f"        largest deviation {worst:.1e} (floating-point zero)")
print("        dialing the reported emergence by enlarging the appended noise system:")
for nb in [2, 4, 8, 16, 64]:
    j = cp(np.kron(np.eye(2), np.full((nb, nb), 1 / nb)))
    print(f"          |B| = {nb:>2}: CP(A x B) = {j:.3f}   emergence reported = {1 - j:.3f}")

# ---------- Part 3: contrast with CE 1.0 (effective information) ----------
ei = lambda T: StochasticMatrix(T).effective_information()
worst = 0.0
for _ in range(300):
    na, nb = rng.integers(2, 5, 2)
    Ar, Br = rng.dirichlet([0.5] * na, size=na), rng.dirichlet([0.5] * nb, size=nb)
    worst = max(worst, abs(ei(np.kron(Ar, Br)) - ei(Ar) - ei(Br)))
print("\nPART 3  CE 1.0 contrast: EI(A x B) = EI(A) + EI(B); largest deviation over 300 pairs", f"{worst:.1e}")
for nb in [2, 4]:
    Sb = StochasticMatrix(np.kron(np.eye(2), np.full((nb, nb), 1 / nb)))
    best = max(Sb.coarse_grain(c).effective_information() for c in Sb.all_coarse_grainings())
    print(f"        |B| = {nb}: EI at joint microscale {Sb.effective_information():.3f}, "
          f"max EI over all partitions {best:.3f}  -> CE 1.0 reports no emergence")

# ---------- Part 4: the emergent hierarchy is manufactured too ----------
print("\nPART 4  emergent hierarchy (full lattice) of A x B; A alone has none")
for nb in [2, 4]:
    Sb = StochasticMatrix(np.kron(np.eye(2), np.full((nb, nb), 1 / nb)))
    c4, g4 = calc_CP_along_CGs(Sb)
    lat4 = refinement_graph(g4)
    bn4 = {n: c4[str(CoarseGraining(d["partition"]))] for n, d in lat4.nodes(data=True)}
    d4 = delta_CP_ancestors(lat4, bn4, allAncestors=True)
    em = [p for p, v in d4.items() if v > 0.01 and len(p) < 2 * nb]
    levels = sorted({len(p) for p in em})
    print(f"        |B| = {nb}: {len(em)} scales with dCP > 0.01, spanning levels (number of blocks) {levels}")
    mixed = [p for p in em if any(len({s // nb for s in blk}) > 1 for blk in p)]
    print(f"                 scales whose blocks mix different states of A: {len(mixed)}")

# ---------- Part 5: every maximal path to pi_A for |B| = 4 ----------
import itertools
S4 = StochasticMatrix(np.kron(np.eye(2), np.full((4, 4), 0.25)))
memo = {}
def cp_part(part):
    key = tuple(sorted(tuple(sorted(b)) for b in part))
    if key not in memo:
        memo[key] = S4.coarse_grain(CoarseGraining(key)).effectiveness()
    return memo[key]
target = {frozenset({0, 1, 2, 3}), frozenset({4, 5, 6, 7})}
ecs, totals = [], set()
def walk(part, path):
    if set(part) == target:
        v = [cp_part(p) for p in path]
        g = np.diff(v); g = g[g > 1e-12]; q = g / g.sum()
        ecs.append(-(q * np.log2(q)).sum()); totals.add(round(v[-1] - v[0], 6)); return
    for i, j in itertools.combinations(range(len(part)), 2):
        if (min(part[i]) < 4) == (min(part[j]) < 4):          # a path to pi_A merges only within a state of A
            walk([b for k, b in enumerate(part) if k not in (i, j)] + [part[i] | part[j]],
                 path + [[b for k, b in enumerate(part) if k not in (i, j)] + [part[i] | part[j]]])
start = [frozenset({s}) for s in range(8)]
walk(start, [start])
print(f"\nPART 5  |B| = 4: {len(ecs)} maximal paths end at pi_A; total CE on every path {sorted(totals)}; "
      f"emergent complexity {min(ecs):.2f} to {max(ecs):.2f} bits")

# ---------- Part 6: A drives B (no feedback) ----------
print("\nPART 6  A autonomous, B copies A's state with probability q (else a coin flip):")
for q in [0.0, 0.5, 0.9]:
    T = np.zeros((4, 4))
    for a, b, a2, b2 in itertools.product(range(2), repeat=4):
        T[2 * a + b, 2 * a2 + b2] = (a2 == a) * (q * (b2 == a) + (1 - q) * 0.5)
    Sq = StochasticMatrix(T); cgA = CoarseGraining(((0, 1), (2, 3)))
    print(f"        q = {q}: joint CP {cp(T):.3f}, CP(pi_A) {Sq.coarse_grain(cgA).effectiveness():.3f}, "
          f"consistent {Sq.is_consistent_with(cgA)}")
