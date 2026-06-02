# Agent Memory Design

Short-term memory belongs in graph state and should capture the current task,
plan, selected tools, observations, and answer. Long-term memory belongs in a
persistent store such as SQLite, Postgres, or a managed database.

Production memory needs clear boundaries: what is saved, why it is saved, how it
is retrieved, and how users can update or delete it. Sensitive data should be
minimized and protected.

