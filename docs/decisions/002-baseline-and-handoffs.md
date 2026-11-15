# 002: Preserve baseline results and repository handoffs

Date: 2026-11-15. Status: accepted for collaboration. Work item: COLLAB-001.

## Context and decision

Yifan and Wenhan will work from separate accounts with different agents. Preserve the existing v1–v4 outputs as the shared research baseline. Engineering checks must not overwrite them.

Use one current STATUS.md, a work register, dated handoffs, numbered decisions, and dated validation records. Use relative links and explicit evidence paths. Keep the original Chinese handoff as a historical baseline and document later developments separately.

Before new estimation, isolate all outputs and record the new run's sample, instruments, environment, parameters, and comparison baseline. A successful engineering test does not validate the economics.

## Consequences

Fresh agents can continue from repository files without access to the other account's chats. Sharing still requires Git commits/pushes or another explicit transfer. The old handoff paths remain as redirects to preserve existing references.
