# UCLA_Capstone_Project

Large language models (LLMs) have demonstrated strong performance
on mathematical reasoning benchmarks such as GSM8K. However, their
robustness to small perturbations in problem formulation remains under-
explored. In this work, I propose a systematic evaluation framework that
measures the robustness of reasoning models under controlled variations
of math word problems. Starting from 100 base problems sampled from
the GSM8K dataset, I generate five types of semantic and structural vari-
ations, including semantic rephrasing, irrelevant numerical distractors,
symbolic or operand swaps, scale or unit changes, and implicit reason-
ing requirements. I evaluate several modern LLMs using both Chain-of-
Thought (CoT) and Self-Consistency (SC) inference strategies. My exper-
iments reveal that while strong models maintain high baseline accuracy,
performance degradation occurs under certain perturbations, particularly
symbolic transformations and scale modifications. Self-consistency de-
coding improves robustness across most models. These findings highlight
important limitations in mathematical reasoning robustness and provide
insights into how reasoning models respond to adversarial variations in
problem statements.
