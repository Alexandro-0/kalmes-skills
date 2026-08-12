# Windows installation

Use Docker Desktop on supported Windows 10 or Windows 11. Docker Desktop is not supported on Windows Server; use a supported Linux host instead of improvising a Windows Server deployment.

Use Docker's current official instructions as the authority: <https://docs.docker.com/desktop/setup/install/windows-install/>. For WSL requirements and behavior, use <https://docs.docker.com/desktop/features/wsl/>.

## Preflight

1. Confirm native Windows, edition/build, architecture, virtualization capability, available memory/disk, and administrative access.
2. Run `wsl --status` and `wsl --version`. Docker currently requires WSL 2.1.5 or newer for the WSL backend; prefer the latest available WSL release. Run `wsl --update` when necessary.
3. Check `docker version`, `docker compose version`, and `docker info`. If all succeed and the daemon reports Linux containers, keep the existing installation.
4. Detect other Docker or container runtimes. Do not uninstall them or delete their data without explicit authorization.

## Install Docker Desktop

Prefer the official Docker Desktop installer or the verified `Docker.DockerDesktop` package from the configured Windows Package Manager source. Inspect the package identity before installation:

```powershell
winget show --exact --id Docker.DockerDesktop
winget install --exact --id Docker.DockerDesktop
```

Let the user review and accept any source or package agreement prompts; do not add automatic agreement flags. If `winget` is unavailable or the identity cannot be verified, download Docker Desktop only from the official Docker page and follow its current command-line or interactive instructions. Do not use an unofficial mirror.

Allow the user to approve elevation, Docker's terms, and any required Windows feature changes. A restart may be required after enabling WSL or virtualization. After installation, launch Docker Desktop visibly so the user can finish first-run setup. Select the WSL 2 engine and Linux containers. Kalmes does not use Windows containers.

Docker Desktop licensing depends on organization and usage. Do not accept subscription terms on the user's behalf; surface the terms and let the user decide.

## Validate Docker

Wait for Docker Desktop to report that the engine is running, then verify from native PowerShell or Command Prompt:

```powershell
docker version
docker compose version
docker info --format '{{.OSType}}'
```

Require the final command to report `linux`. Do not continue while Docker Desktop is starting or when the CLI only reports its client section.

## Run Kalmes V2

Keep the extracted release on a normal local Windows path and run from its root in an attached terminal:

```powershell
cmd.exe /d /c call install_v2.bat
```

Do not execute the Linux script from WSL for a native Windows installation. The Windows V2 installer uses a folder picker, saves user settings in `HKCU:\Environment`, loads the packaged images, and starts the deployment through Docker Desktop.

If Windows Firewall prompts for network access, approve only the network profiles required by the intended deployment. Do not expose Kalmes on Public networks by default.
