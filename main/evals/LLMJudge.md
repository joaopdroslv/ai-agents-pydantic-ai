# What is LLMJudge?

**LLMJudge is an evaluator** provided by the pydantic-evals library.
It allows you to **automatically evaluate the output of an LLM** (Large Language Model)
based on qualitative, subjective, or open-ended criteria.

Rather than relying on strict rules or exact matching, **LLMJudge leverages
another LLM as the judge to assess whether a given output meets a certain rubric**
(set of evaluation instructions or goals).

# How does it work under the hood?

### It constructs a prompt like:

`“Given the input and output below, does the output satisfy the rubric: ‘[your rubric here]’?”`

Sends this prompt to a judge model (e.g., gpt-4, claude-3, etc.).
Interprets the judge's response to decide whether the case passes.

This makes it a powerful tool for evaluating tasks like:
- Instruction following
- Ethical alignment
- Style and tone matching
- Content filtering
- Creative writing or summarization