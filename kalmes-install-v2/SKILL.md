---
name: kalmes-install-v2
description: Install Docker and deploy Kalmes V2 from an official Kalmes V2 release package on Windows, macOS, or Linux, then validate the running system. Use when a user asks Codex or another agent to install, set up, deploy, or reinstall Kalmes on a computer, including installing Docker Desktop on Windows or macOS, installing Docker Engine and Compose on Linux, selecting the correct V2 installer script, handling prerequisites, and troubleshooting initial startup. This skill supports Kalmes V2 only and must never run V1 or deprecated installer scripts.
---

# Install Kalmes V2

Install the software on the user's current computer unless the user names another host. Perform safe, discoverable steps autonomously, but leave license acceptance, elevation prompts, reboots, and secret entry to the user.

## Establish the target

1. Detect the host OS, version, CPU architecture, available package manager, privilege level, free disk space, and whether the current shell is native, WSL, a container, or a remote session. Do not mistake WSL for the Windows host. Confirm that the supplied release supports the detected CPU architecture before loading its images.
2. Locate the official Kalmes V2 release package supplied by the user or vendor. If no package path or official download URL is available, ask for it; do not invent a Kalmes download URL or build a release from source.
3. Inspect the package before changing the host. Read [references/installer-contract.md](references/installer-contract.md) and confirm that the correct V2 script and its adjacent payload are present in one isolated extraction directory.
4. Determine whether this is a new installation. If a Kalmes deployment, matching containers, named Docker volumes, or a saved deployment path already exists, stop before running the installer and explain that continuing can overwrite files and force-recreate containers. Require explicit reinstall/update authorization and a backup plan.
5. Collect the non-secret installation choices: system name, advertised host/IP, base HTTPS port, MQTT port, time zone, and whether MQTT authentication is required. Let the user enter MQTT credentials directly into the interactive installer; never ask them to paste a password into chat or expose it in logs.

## Install and validate Docker

Skip installation only when both Docker Engine and the Compose plugin already work. `docker --version` alone is insufficient; require a successful engine query and `docker compose version`.

- On Windows, read [references/windows.md](references/windows.md). Install Docker Desktop, use the WSL 2 backend and Linux containers, and run Kalmes from native Windows with `install_v2.bat`.
- On macOS, read [references/macos.md](references/macos.md). Install the architecture-matched Docker Desktop and Bash 4 or newer, then run `mac_install_v2.sh`.
- On Linux, read [references/linux.md](references/linux.md). Install Docker Engine and the Docker Compose plugin from Docker's official repository for the detected distribution, then run `install_v2.sh`.

Do not remove an existing Docker installation, containers, images, volumes, networks, WSL distributions, or conflicting packages without explicit authorization. If a reboot or logout is required, record the completed state and give the exact resume step.

Before continuing, verify that the daemon is reachable, Compose is available as `docker compose`, and Docker is using Linux containers. Do not substitute the legacy `docker-compose` command.

## Run the V2 installer

1. Check that the selected ports are free and that the base port is at least 3. Kalmes consumes the base port and the two preceding ports; the MQTT port must be distinct from all three.
2. Run the installer from the isolated extracted package directory in an attached interactive terminal. Do not run it detached, redirect its input, or copy the script away from its sibling payload.
3. Use exactly one platform script:

   - Windows: `cmd.exe /d /c call install_v2.bat`
   - Linux: `chmod +x ./install_v2.sh` followed by `./install_v2.sh`
   - macOS: invoke `./mac_install_v2.sh` with a verified Bash 4+ executable

4. Answer non-secret prompts using the agreed values. Pause for the user to enter privileged credentials or MQTT secrets directly. Do not run `install_v1_deprecated.bat`, `install_v1_deprecated.sh`, `install.sh`, or any other V1/legacy installer even if V2 fails.
5. Preserve the full failure context when a command fails. Diagnose Docker, ports, permissions, package integrity, or container logs before retrying; never repeatedly rerun the whole installer as a generic repair.

## Verify the deployment

Follow [references/installer-contract.md](references/installer-contract.md) to discover the actual deployment directory and installer-reported URL. Then:

1. Confirm both generated Compose files exist in the deployment directory.
2. Run `docker compose ... ps -a` for the backend and frontend Compose files and require the expected services to remain running.
3. Inspect recent logs for exited, restarting, or unhealthy services. Do not print environment variables or secrets.
4. Request the installer-reported HTTPS URL and `/<system-name>/api/ping`. Accept a locally bundled self-signed certificate only for this narrow local readiness check; keep normal TLS verification for remote or production hosts.
5. Confirm the ping returns HTTP 200 and does not report `ready: false`. Treat `service_initializing` as temporary and poll for a bounded period before collecting logs.

## Completion

Report the host OS and architecture, Docker and Compose versions, Docker installation method, exact V2 script used, deployment directory, system URL, selected non-secret ports and time zone, container/readiness results, and any reboot, certificate, firewall, backup, or credential action still required. Never include MQTT passwords or other secrets.
