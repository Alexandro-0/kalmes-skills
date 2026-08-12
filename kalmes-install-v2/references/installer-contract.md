# Kalmes V2 installer contract

Use this reference to preflight, run, and verify an official Kalmes V2 release package. The release payload, not this skill repository, is the installation source.

## Package preflight

Extract the release into a new, isolated directory. The V2 scripts copy package directories into the deployment directory, so unrelated sibling directories must not be present.

Require the platform script and its adjacent payload:

- Windows: `install_v2.bat`
- Linux: `install_v2.sh`
- macOS: `mac_install_v2.sh`
- Backend and frontend production-image directories containing their Compose templates, run scripts, and image archives
- `nginx-template.conf`

List the archive before extraction when the format permits it, reject path traversal or absolute archive members, and compare a vendor-provided checksum or signature when available. Do not treat a filename alone as proof of authenticity. Never download and execute a remote installer in a single pipeline.

Reject a package that has only `install_v1_deprecated.bat`, `install_v1_deprecated.sh`, `install.sh`, or another legacy installer. Do not fall back to V1.

Estimate the expanded payload size and Docker image load size, then confirm adequate free space. Do not invent a fixed minimum when the package itself provides the measurable requirement.

## Installation inputs

Agree on these values before launching the interactive script:

| Input | Default | Validation and effect |
| --- | --- | --- |
| System name | `kalmes` | Lowercase letters, numbers, `_`, and `-`; first character must be alphanumeric. It controls container/service names, deployment folder, environment keys, and URL path. |
| Host/IP | `localhost` | Use a client-reachable hostname or IP for remote access; do not expose an unreviewed public interface. |
| Base HTTPS port | `17202` | Integer 3-65535. Kalmes also uses base-1 and base-2, so the default reserves 17200-17202. |
| MQTT port | `16000` | Integer 1-65535 and different from the three Kalmes ports. |
| Time zone | `Asia/Taipei` | Use a valid IANA-style value without spaces. |
| MQTT authentication | disabled | For a network-reachable deployment, prefer authentication. Let the user enter the deployment account and password in the installer terminal. |

Check all four ports for active listeners before installation. Also review host firewall and network exposure. Docker-published ports can interact with or bypass some host firewall paths, especially on Linux; apply access rules deliberately rather than assuming the firewall blocks them.

## Installer behavior

The scripts are interactive and perform more than file copying. They persist installation settings, create or reuse a deployment directory, patch Compose and Nginx configuration, configure MQTT, load Docker image archives, create the shared Docker network, and start backend and frontend services with `--force-recreate`.

Saved settings are stored in:

- Windows: current user's `HKCU:\Environment`, using keys derived from the system name, including `<system>_deploy_path`, `<system>_MES_IP`, `<system>_MES_PORT`, `<system>_MQTT_PORT`, and `<system>_TIME_ZONE`.
- Linux and macOS: `${KALMES_DEPLOY_ENV_FILE:-$HOME/.kalmes_deploy_env}`. A hyphen in the system name becomes an underscore in shell environment-key prefixes.

The normal deployment directory is selected under a parent directory on Windows and defaults to `$HOME/<system-name>_deploy` on Linux/macOS. Use the installer's final output or saved deployment-path value as authoritative.

Running the script against an existing deployment can replace files and force-recreate services. Before an authorized reinstall or update, record `docker compose ps`, back up the deployment directory and application data according to the user's recovery requirements, and confirm that the backup can be located. Do not assume copying the deployment directory alone backs up named Docker volumes.

## Execution

Run from the package root and keep the terminal attached:

```text
Windows: cmd.exe /d /c call install_v2.bat
Linux:   chmod +x ./install_v2.sh && ./install_v2.sh
macOS:   "<bash-4+-path>" ./mac_install_v2.sh
```

Do not place secrets in command arguments or pre-seed them through visible environment variables. Allow interactive elevation and secret prompts to be handled locally by the user.

## Verification

Use the deployment directory reported by the installer. It should contain:

- `docker-compose.backend.prod.yml`
- `docker-compose.frontend.prod.yml`
- `nginx.conf`

Run Compose status separately for both files. On Linux, use the same privilege model as the package run scripts, which currently invoke `sudo docker`. Confirm that services remain running and inspect bounded recent logs for failures.

Use the final URL printed by the installer. With defaults it is:

```text
https://localhost:17202/kalmes
```

The readiness endpoint is the corresponding `api/ping`, normally:

```text
https://localhost:17202/kalmes/api/ping
```

For the bundled local self-signed certificate, a one-time local `curl --insecure` readiness request is acceptable if the exception is clearly stated. Do not use an insecure TLS exception for remote or production verification. Require HTTP 200 and a response that does not set `ready` to false.

If startup fails, capture Compose status and the last 200 log lines for the failing service. Check daemon availability, port conflicts, architecture mismatch, incomplete image archives, permissions, and MQTT settings before considering a rerun.
