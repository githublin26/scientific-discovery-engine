# Protocol v0.1
Freeze method before reading reference values: rank ascending formation energy; ties by material ID.
Input features are explicitly allowlisted. Predictions are serialized and hashed before reference reveal.
Target: published Decomposition Energy Per Atom All, eV/atom, with a declared 0.001 eV/atom screening tolerance.
This tolerance is a project screening choice, not a universal synthesis criterion.
Report precision@min(3,n), class prevalence, and single-class flag. There is no predictive acceptance threshold yet.
Software acceptance: parsing, deterministic ranking, leakage guards, traceable hashes, tests.
Scientific acceptance: deferred until an independent mixed-class grouped benchmark and stronger/random baselines exist.
The local evaluator can access reference labels; isolation is procedural, not adversarial.
No inference about bandgap, semiconductor suitability or synthesis feasibility is warranted.

