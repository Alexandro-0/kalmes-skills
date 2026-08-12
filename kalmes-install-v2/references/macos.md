# macOS installation

Use Docker Desktop for Mac and the dedicated Kalmes `mac_install_v2.sh` script. Use Docker's current official instructions as the authority: <https://docs.docker.com/desktop/setup/install/mac-install/>.

## Preflight

1. Run `sw_vers` and `uname -m`. Distinguish Apple silicon (`arm64`) from Intel (`x86_64`) and require a macOS release currently supported by Docker Desktop.
2. Check available memory/disk and confirm the user can approve privileged helper installation.
3. Check `docker version`, `docker compose version`, and `docker info`. Keep a working existing Docker Desktop installation.
4. Verify `python3`, `find`, `sed`, and Bash 4 or newer. Apple's system `/bin/bash` may be version 3 and is not sufficient for the Kalmes macOS V2 script.

## Install Docker Desktop

Download the architecture-matched Docker Desktop DMG only through Docker's official macOS installation page. Verify the published checksum when available. Follow Docker's current interactive or command-line DMG installation procedure, then launch Docker Desktop visibly with:

```text
open -a Docker
```

Let the user approve Docker's terms and privileged helper prompts. Docker Desktop licensing depends on organization and usage; do not accept subscription terms for the user.

Wait for the engine, then require successful `docker version`, `docker compose version`, and `docker info` calls.

## Install script prerequisites

Install Bash 4+ and Python 3 through an already trusted package manager. With Homebrew already present:

```text
brew install bash python
"$(brew --prefix)/bin/bash" --version
python3 --version
```

If no trusted package manager exists, explain that Kalmes needs Bash 4+ and ask before adding one. Do not silently run a remote package-manager bootstrap script.

## Run Kalmes V2

Resolve and verify the non-system Bash path, then run from the extracted package root in an attached terminal:

```text
BASH_BIN="$(brew --prefix)/bin/bash"
"$BASH_BIN" ./mac_install_v2.sh
```

Use `mac_install_v2.sh`, not the Linux `install_v2.sh`. Keep Docker Desktop running throughout image loading and startup. Allow the user to handle macOS elevation and MQTT secret prompts locally.
