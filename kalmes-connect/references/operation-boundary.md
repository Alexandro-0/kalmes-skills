# Kalmes application operation boundary

## Required path

For live application work, use the relevant Kalmes skill and its documented API contracts with the required authentication, authorization and activity labels. This includes source reads and writes, execution, FAP definitions, records, settings, jobs, logs, plugin packs, verification and rollback. Documented browser workflows, page checks and masked secret-entry interfaces remain valid where the relevant skill specifies them.

This boundary applies even when the agent already has a session, the deployment is local or non-production, or host administrator access is available. Permission to complete a plugin task does not authorize a different execution channel.

## Prohibited bypasses

- Do not use Docker or Compose CLI, Docker Engine API/SDK, container shells, SSH or equivalent host access to perform application work. This includes `docker exec`, `docker compose exec`, `docker cp`, container logs/inspection as a substitute for application diagnostics, and container restart/recreation as an application repair.
- Do not read or modify deployed Extra Code, configuration, secrets or data through container filesystems, bind mounts, named volumes or host deployment directories. A locally mounted runtime directory is not a source checkout for this purpose.
- Do not connect directly to MongoDB or another backing database, invoke server Python functions from a shell, or use database/file utilities to replace an application API.
- Do not upload or execute helper Extra Code that acts as a shell, Docker proxy, arbitrary file/database editor or other escape hatch around the required API. Ordinary feature code using the documented Kalmes runtime contracts remains allowed.
- Do not ask another agent, internal queue, script or tool to perform a prohibited bypass. Carry this boundary into delegated task instructions.

## When an API cannot complete the task

Follow the relevant skill's bounded authentication, request-correction and retry rules. Missing credentials, denied access, license failure, absent endpoints, unsupported capabilities, timeouts and server errors never authorize infrastructure fallback. Report the blocked operation, observed response and missing capability or access without exposing secrets. Continue only independent work that remains within scope. Do not fabricate successful verification or replay an uncertain mutation.

If a necessary operation has no supported interface, leave that operation blocked and describe the required product capability or separate infrastructure work. Do not silently reinterpret a plugin request as installation or maintenance authorization.

## Local work and installation

Authorized source-checkout edits, isolated local tests, analysis of API-exported data and inspection of supplied plugin archives remain allowed. They must not reach into a running deployment's files or database. Use the documented APIs to deploy and verify a live plugin.

The local activity collector may observe its paired checkout and use its documented upload API; it grants no application or infrastructure access. Maintaining skill source files also does not authorize runtime changes.

`kalmes-install-v2` permits Docker installation, official release deployment and bounded container/readiness diagnosis only within an explicitly requested installation or reinstall. That exception cannot be borrowed to perform plugin operations. Separately requested infrastructure maintenance is a distinct scope, not a fallback supplied by these application skills.
