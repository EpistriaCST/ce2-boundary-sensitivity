# Causal Emergence 2.0 Is Not Invariant Under Adjoining an Independent System

**Supplementary code and output**

Charles S. Thomas · Epistria, LLC · ORCID [0009-0007-6330-1053](https://orcid.org/0009-0007-6330-1053)

## What this record contains

| File | Contents |
| - | - |
| `Causal Emergence 2.0 Is Not Invariant Under Adjoining an Independent System.pdf` | The technical note |
| `two\_systems\_as\_one.py` | Script that reproduces principle numerical results reported in the note |
| `two\_systems\_as\_one\_output.txt` | The script's full output, as produced for the note |
| `README.md` | This file |


## The result in brief

Take a system A that shows no causal emergence: two states, each of which stays put. Append a system B that never interacts with A: pure noise. Treat the pair as one system, A ⊗ B. Causal Emergence 2.0 (Hoel 2026; Jansma & Hoel 2025) then reports causal emergence for the pair.

The emergence it reports sits at the scale that ignores B, which is exactly A. A did not change, and nothing connects A to B. The emergence score rises as B is made larger:

| Size of B | CE reported for A ⊗ B |
| - | - |
| 2 states | 0.500 |
| 4 states | 0.667 |
| 16 states | 0.800 |
| 64 states | 0.857 |


The full-lattice "emergent hierarchy" is produced the same way. With four states of noise, A ⊗ B has 196 emergent scales, all of which coarse-grain B. A alone has none.

The general form: for independent systems, CE 2.0's causal primitives (CP) for the pair are the average of the two systems' CPs, weighted by the logarithm of each system's number of states. CE 1.0's effective information simply adds across the two instead, and does not show the effect. The note gives the proofs.

## What the script computes

| Part | Computation |
| - | - |
| 1 | The worked example: the micro-to-macro path, its gains, the consistency check, and the full-lattice hierarchy for B with 2 states |
| 2 | The weighted-average identity, checked on 300 random independent pairs with random intervention distributions, and the table above |
| 3 | The CE 1.0 contrast: effective information adds across independent systems, and no emergence is reported |
| 4 | The emergent hierarchy for B with 2 and 4 states, including a check that no emergent scale mixes different states of A |
| 5 | All 6,480 maximal paths to the A-scale for B with 4 states: total CE and the range of emergent complexity |
| 6 | A drives B without feedback: the same emergence is reported whether B is independent or tracks A |


## How to run it

The script uses the causal emergence toolkit published by the CE 2.0 authors, pymergence (Jansma & Hoel 2025), at the commit used for the note.

Requirements: Python 3 with the packages `numpy`, `networkx` and `matplotlib`.

```
pip install numpy networkx matplotlib  
git clone https://github.com/EI-research-group/pymergence  
cd pymergence  
git checkout 6e5cb45  
cd ..  
python two\_systems\_as\_one.py
```

Run the last command from the folder that contains both `two\_systems\_as\_one.py` and the `pymergence` folder. The run takes about two minutes. Its output should match `two\_systems\_as\_one\_output.txt` line for line.

This procedure was checked in a clean environment (Python 3.11, numpy 2.4, networkx 3.6, matplotlib 3.10). The output was identical to the file in this record.


## Citation

Thomas, C. S. (2026). *Causal Emergence 2.0 Is Not Invariant Under Adjoining an Independent System* (Technical note). Zenodo. [https://doi.org/10.5281/zenodo.22699520](https://doi.org/10.5281/zenodo.22699520) 

## References

- Hoel, E. (2026). Quantifying emergent complexity. *Patterns*, 7, 101472. [https://doi.org/10.1016/j.patter.2025.101472](https://doi.org/10.1016/j.patter.2025.101472)

- Hoel, E. (2025). Causal Emergence 2.0: Quantifying emergent complexity. ArXiv. https://doi.org/10.48550/arXiv.2503.13395

- Jansma, A., & Hoel, E. (2025). Engineering emergence. arXiv:2510.02649.

- Jansma, A., & Hoel, E. (2025). PyMergence: A Python toolkit for causal emergence 2.0. Zenodo. [https://doi.org/10.5281/zenodo.17210078](https://doi.org/10.5281/zenodo.17210078) 

## License

```
The technical note is licensed CC BY-NC 4.0. The reproduction script is licensed under the MIT License. Copyright (c) 2026 C.S. Thomas

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
```


