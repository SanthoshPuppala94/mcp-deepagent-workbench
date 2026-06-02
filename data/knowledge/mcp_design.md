# MCP Design Notes

Model Context Protocol servers should expose narrow, well-documented tools with
explicit input schemas. Production MCP tools should apply least privilege, audit
tool calls, validate arguments, and separate resources from executable actions.

Good MCP resources are stable knowledge surfaces such as runbooks, architecture
notes, policies, and API references. Tools should perform bounded operations such
as search, risk assessment, or agent workflow execution.

