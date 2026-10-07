# Scientific-agent landscape: narrow primary-source sidecar

**Access date for every source: 2026-10-07.** Scope: FutureHouse platform/Robin and Google DeepMind Co-Scientist, public descriptions only. No project-code inspection or competitor execution. “Described” below means a first-party claim, not independently verified performance.

## Compact comparison

| Capability | FutureHouse platform / Robin | Google DeepMind Co-Scientist |
|---|---|---|
| Hypothesis generation | Robin generates hypotheses, plans experiments, analyzes results, and proposes follow-up hypotheses; the updated announcement describes an integrated biological-discovery workflow. [Robin][R] | Generation proposes literature/data-grounded hypotheses; Evolution refines and combines them. [DeepMind][D] |
| Tool orchestration | Platform agents access specialist databases and chemistry tools; Robin orchestrates Crow, Falcon, and Finch for literature and data-analysis tasks. [Platform][F], [Robin][R] | A supervisor coordinates specialized agents in parallel; web search, ChEMBL, and UniProt supply knowledge. AlphaFold tool use is described as testing in selected collaborations, not universal availability. [DeepMind][D] |
| Literature search | Crow answers scholarly questions, Falcon performs deeper reviews, and Owl investigates whether work has been done before; full-text analysis and source-quality evaluation are described. [Platform][F] | Searches and reasons over literature, cites it, and uses external tools where applicable to ground recommendations. [Authors' paper][P] |
| Provenance / evidence linking | Platform describes visible reasoning and source consideration; Robin publishes code and example trajectories. These provide evidence-inspection hooks, not proof of complete reproducibility. [Platform][F], [Robin][R] | Recommendations cite relevant literature; reviews assess evidence and scrutinize assumptions. This establishes source linking, not a verified end-to-end provenance guarantee. [Authors' paper][P] |
| Feedback loops | Robin feeds experimental data analysis into subsequent experimental choices and candidate hypotheses. Humans performed the physical experiments in the described study. [Robin][R] | Reflection, ranking tournaments, evolution, and meta-review provide iterative feedback; scientists can steer goals and proposals through natural-language feedback. [DeepMind][D], [Authors' paper][P] |

## Interpretation and limits

**Inference:** hypothesis generation, orchestration, literature retrieval, evidence linking, and iterative feedback are shared capability categories in these sources. Their mere inclusion in another system is therefore not a unique differentiator. This does not establish identical implementations, maturity, coverage, correctness, or cost.

Evidence linking should not be conflated with complete provenance: this review does not establish comparable guarantees for immutable snapshots, hashes, units, execution lineage, or replay. Unestablished guarantees remain **unknown**, not competitor deficiencies.

Current-access caveat: the historical FutureHouse platform URL now redirects to Edison; the 2025 launch description is not a verified current feature inventory. Google's help page describes Hypothesis Generation access as interest-form limited, with no guaranteed admission. [Platform entry][E], [Google help][H]

**Source-described capabilities are not head-to-head measurements and cannot prove relative advantage.** Vendor benchmarks or selected biological examples do not establish superiority for semiconductor weak-signal detection or this project's materials baseline. Potential differentiation would require a matched, independently evaluated task with specified data, baselines, false-alarm/recall metrics, provenance requirements, and resource budgets. No such comparison was conducted here. No claim is made that either competitor lacks any capability.

## Direct primary-source URLs

- [FutureHouse platform launch (2025-05-01)][F]
- [FutureHouse Robin announcement (updated 2026-05-19)][R]
- [Google DeepMind Co-Scientist overview][D]
- [Co-Scientist authors' Nature paper][P]
- [Google Hypothesis Generation help][H]
- [FutureHouse platform entry; redirects to Edison][E]

[F]: https://www.futurehouse.org/news/launching-futurehouse-platform-ai-agents
[R]: https://www.futurehouse.org/research/demonstrating-end-to-end-scientific-discovery-with-robin-a-multi-agent-system
[D]: https://deepmind.google/blog/co-scientist-a-multi-agent-ai-partner-to-accelerate-research/
[P]: https://www.nature.com/articles/s41586-026-10644-y
[H]: https://support.google.com/hypothesis-generation/answer/17106281?hl=en
[E]: https://platform.futurehouse.org/
