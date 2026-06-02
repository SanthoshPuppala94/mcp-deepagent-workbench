# Deep Agent Patterns

A deep agent decomposes a task, selects tools, executes tool calls, observes
results, synthesizes a response, and writes useful memory. LangGraph is a good
fit because each phase can be a node with explicit state transitions.

Production deep agents should be observable, testable, and constrained. Tool
selection should be explainable, memory writes should be intentional, and risky
actions should require approval or policy checks.

