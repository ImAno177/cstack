# Continual learning research notes

These notes separate model-level continual learning from external agent memory and versioned skill evolution. They are design evidence, not a claim that this plugin implements the algorithms.

## Stability, plasticity, and replay

- [Learning without Forgetting](https://arxiv.org/abs/1606.09282), Li and Hoiem, 2016. Distillation preserves old outputs while learning new data. Transfer: compare behavior before and after an update. Limit: agreement on new inputs does not prove complete old-task retention.
- [Overcoming catastrophic forgetting in neural networks](https://doi.org/10.1073/pnas.1611835114), Kirkpatrick et al., PNAS 2017. EWC protects parameters important to earlier tasks. Transfer: declare protected behavior and penalize damaging changes. Limit: skill files expose neither parameters nor Fisher information.
- [Gradient Episodic Memory](https://papers.nips.cc/paper/7225-gradient-episodic-memory-for-continual-learning), Lopez-Paz and Ranzato, NeurIPS 2017. GEM constrains updates using episodic memories and formalizes backward and forward transfer. Transfer: replay representative prior tasks after each material change.
- [Experience Replay for Continual Learning](https://proceedings.neurips.cc/paper_files/paper/2019/hash/fa7cdfad1a5aaf8370ebeda47a1ff1c3-Abstract.html), Rolnick et al., NeurIPS 2019. Replay preserves prior behavior in streams without clean task boundaries. Transfer: select replay by task family and failure mode. Limit: storage, privacy, and irrelevant context still matter.

## Language-model continual adaptation

- [Continual Learning for Large Language Models: A Survey](https://arxiv.org/abs/2402.01364), Wu et al., 2024. Separates continual pretraining, instruction tuning, and alignment, and distinguishes these from retrieval, editing, and prompting. Use it to classify the problem before selecting a method.
- [CITB: A Benchmark for Continual Instruction Tuning](https://aclanthology.org/2023.findings-emnlp.633/), Zhang et al., Findings of EMNLP 2023. Makes task order and sequential evaluation explicit. Transfer: version a fixed task stream before claiming improvement.
- [Orthogonal Subspace Learning for Language Model Continual Learning](https://arxiv.org/abs/2310.14152), Wang et al., 2023. Isolates task updates in low-rank subspaces. Transfer: prefer modular, narrow skill updates over repeated edits to a shared core. Limit: it still requires parameter training.
- [Rehearsal-Free Modular and Compositional Continual Learning for Language Models](https://arxiv.org/abs/2404.00790), Wang et al., 2024. Uses modules and composition to reduce rehearsal. Transfer: compose scoped skills. Limit: routing and module management add failure modes.
- [InsCL](https://aclanthology.org/2024.naacl-long.37/), Wang et al., NAACL 2024. Uses instruction-aware replay. Transfer: retrieve by task similarity and quality, not recency alone. Limit: benchmark gains do not generalize automatically.

## Agent memory and skill evolution

- [Reflexion](https://arxiv.org/abs/2303.11366), Shinn et al., 2023. Stores verbal feedback instead of changing weights. Transfer: keep feedback as a candidate, but require external outcome evidence because self-reflection can amplify errors.
- [MemoryBank](https://arxiv.org/abs/2305.10250), Zhong et al., 2023. Adds reinforcement and forgetting policies to long-term memory. Transfer: define retention and retirement; importance heuristics do not replace provenance or correctness.
- [Lifelong Learning of LLM-based Agents: A Roadmap](https://arxiv.org/abs/2501.07278), Zheng et al., 2025. Separates perception, memory, and action modules. Transfer: evaluate the whole loop rather than equating a memory store with learning.
- [LifelongAgentBench](https://arxiv.org/abs/2505.11942), Zheng et al., 2025. Tests interdependent tasks and finds indiscriminate replay can be limited by irrelevant context. Transfer: measure reuse under a fixed context budget.
- [A-MEM](https://arxiv.org/abs/2502.12110), Xu et al., 2025. Structures and links evolving memories. Transfer: make links and updates reviewable. Risk: graph drift can spread one wrong memory.
- [SkillLearnBench](https://arxiv.org/abs/2604.20087), Zhong et al., 2026. Evaluates skill quality, trajectories, and outcomes across real-world tasks. It reports inconsistent gains across tasks and models, stronger results on reusable workflows, and recursive drift from self-feedback alone. Transfer: require external feedback, repeated evaluation, and task-level reporting.
- [ContinualSkillBench](https://arxiv.org/abs/2608.03874), Guan et al., 2026. Finds in-context adaptation can match explicit skill maintenance on average, while explicit skills help selected reusable-procedure tasks. Transfer: prove that a promoted skill adds durable, transferable value beyond simply retaining prior context.

## Design conclusion

For this plugin, continual learning means conservative, versioned agent-level skill evolution: source, scope, conflict check, replay, transfer measurement, approval, rollback, and retirement. Model-level claims require a training pipeline and parameter-level evaluation; a hook or text file cannot make that claim.
