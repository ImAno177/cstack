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

## Agent workflow, interfaces, and verification

- [ReAct](https://arxiv.org/abs/2210.03629), Yao et al., ICLR 2023. Interleaving reasoning with external actions improves grounding and exception handling. Transfer: every important decision in a skill should point to an observation, command, or artifact instead of relying on an ungrounded plan.
- [SWE-bench](https://arxiv.org/abs/2310.06770), Jimenez et al., 2023. Real repository tasks require cross-file understanding, execution, long context, and multi-step coordination. Transfer: evaluate cstack against whole-repository outcomes, not isolated function examples or prose quality.
- [SWE-agent](https://arxiv.org/abs/2405.15793), Yang et al., 2024. Agent-computer interface design materially changes software-agent performance. Transfer: keep commands, paths, output limits, and handoff schemas explicit; a skill is part of the agent interface, not only a prompt.
- [Lost in the Middle](https://arxiv.org/abs/2307.03172), Liu et al., TACL 2024. Retrieval quality degrades when relevant information is buried in long context. Transfer: front-load invariants and the next action, use compact checkpoints, and retrieve task-family slices rather than indiscriminate history.
- [AgentBench](https://arxiv.org/abs/2308.03688), Liu et al., 2023. Agent failures cluster around long-horizon reasoning, decision-making, and instruction following. Transfer: measure trajectories, retries, partial completion, and instruction adherence in addition to final success.
- [Let's Verify Step by Step](https://arxiv.org/abs/2305.20050), Lightman et al., 2023. Process supervision can outperform outcome-only supervision on difficult reasoning tasks. Transfer: verify meaningful intermediate units and preserve their evidence, while still requiring an end-state check.
- [AutoGen](https://arxiv.org/abs/2308.08155), Wu et al., 2023. Multi-agent conversations are useful when interaction roles and protocols are explicit. Transfer: assign bounded roles, ownership, schemas, and termination conditions; do not fan out merely because more agents are available.
- [Operation-Visible Agent Architecture](https://aclanthology.org/2026.emnlp-industry.179/), ACL Industry Track 2026. The system keeps tool operation resolution visible in the main reasoning loop while allowing efficient parallel calls. Transfer: parallelize independent work, but return compact operation outcomes to the coordinator so correctness and recovery remain inspectable.
- [PASTE](https://arxiv.org/abs/2603.18897), 2026. Speculative tool invocation predicts recurring future calls to reduce observed latency. Transfer: treat speculation as an experiment with cancellation and stale-result accounting, not as a default, because incorrect predictions can add calls and obscure failures.

## Skill authoring and retrieval

- [A Survey on Agent Skills](https://research.google/pubs/a-survey-on-agent-skills-externalized-procedural-knowledge-in-language-models/), Badhe et al., 2026. Frames skills as externalized procedural knowledge with a lifecycle from authoring and routing through execution, repair, evaluation, and governance. Transfer: audit each skill across those lifecycle stages instead of treating `SKILL.md` as a prompt-only artifact.
- [SkillsBench](https://arxiv.org/abs/2602.12670), Li et al., 2026. Curated skills improve pass rates on average but not uniformly; self-generated skills do not reliably help, and focused packages outperform comprehensive documentation. Transfer: keep skills narrow, test them against a no-skill baseline, and do not promote a model-generated skill without external evaluation.
- [SkillReducer](https://arxiv.org/abs/2603.29919), Gao et al., 2026. Reports that non-actionable bodies and oversized references waste context, while compression plus progressive disclosure can preserve quality. Transfer: keep routing metadata short, move detail to references, and measure retention after any reduction.
- [How Well Do Agentic Skills Work in the Wild](https://arxiv.org/abs/2604.04323), 2026. Finds skill gains degrade when the agent must retrieve from a large noisy collection, while query-specific refinement recovers performance when the initial match is relevant. Transfer: evaluate router precision and distractor resistance, not only hand-picked direct invocation.
- [What Keeps Agent Skills from Being Reusable?](https://arxiv.org/abs/2608.08453), Zhang et al., 2026. Finds widespread defects in routing metadata, actionable body structure, and resource organization. Transfer: lint metadata, paths, provenance, host assumptions, and progressive disclosure as release gates.
- [Harnessing LLM Agents with Skill Programs](https://aclanthology.org/2026.emnlp-main.2086/), Liu et al., EMNLP 2026. Shows that validated executable interventions can act at failure-prone states instead of remaining passive prose. Transfer: encode repeated, verifiable corrections as scripts, validators, or narrowly triggered rules when text alone is insufficient.
- [XSkill](https://proceedings.mlr.press/v306/jiang26aq.html), Jiang et al., ICML 2026. Separates concise action-level experiences from structured task-level skills and uses critique across rollouts. Transfer: keep episode-specific observations separate from durable skills; promote only consolidated, transferable procedures.

## Design conclusion

For this plugin, continual learning means conservative, versioned agent-level skill evolution: source, scope, conflict check, replay, transfer measurement, approval, rollback, and retirement. Model-level claims require a training pipeline and parameter-level evaluation; a hook or text file cannot make that claim.
