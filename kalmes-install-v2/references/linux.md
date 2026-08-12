# Linux installation

Install Docker Engine and the Docker Compose plugin from Docker's official repository for the detected distribution. Use Docker's platform index as the authority and open the matching current distribution page: <https://docs.docker.com/engine/install/>. Use the Compose plugin instructions at <https://docs.docker.com/compose/install/linux/>.

## Preflight

1. Read `/etc/os-release`; record distribution, version, and codename. Run `uname -m` and confirm that both Docker and the Kalmes image archives support the architecture.
2. Confirm `systemd` or the distribution's service manager, `sudo`/root access, free disk space, and outbound access required to install packages.
3. Check `sudo docker version`, `sudo docker compose version`, and `sudo docker info`. Keep an already working official installation.
4. Detect conflicting packages and runtimes. Docker's distribution instructions may tell you to remove packages such as `docker.io`, `podman-docker`, `containerd`, or `runc`; removal can disrupt workloads, so show the conflict and obtain explicit authorization before removing anything.
5. Inspect current containers, volumes, networks, firewall rules, and Docker data root. Never uninstall Docker or erase `/var/lib/docker` as part of a normal Kalmes install.

## Install Docker Engine

Follow the current official repository procedure for the exact supported distribution and version. Install Docker Engine, CLI, containerd, Buildx, and the Docker Compose plugin. Do not guess repository codenames for derivative or unsupported distributions.

For non-production development only, Docker's convenience script may be used with explicit user agreement. Download it to a file, inspect it, and run its `--dry-run` mode before execution. Never pipe it directly from the network into a shell, and do not use it for production installation or upgrades.

Enable and start Docker with the distribution's service manager when the official instructions require it. The Kalmes Linux run scripts currently use `sudo docker`, so adding the user to the `docker` group is unnecessary. Do not grant docker-group access silently because it is root-equivalent.

Install the Kalmes script prerequisites through the distribution package manager: Bash 4+, Python 3, `find`, and `sed`.

## Validate Docker

Require successful server-side output from:

```text
sudo docker version
sudo docker compose version
sudo docker info
```

Also confirm that the Docker service is enabled/running as intended and review firewall exposure before publishing Kalmes ports. Docker-published ports can bypass expected `ufw` or `firewalld` paths; follow Docker's current firewall guidance for the host.

## Run Kalmes V2

Run from the isolated extracted package root in an attached terminal:

```text
chmod +x ./install_v2.sh
./install_v2.sh
```

Do not run the script as `sudo`; it intentionally stores per-user settings below the invoking user's home and calls `sudo docker` only where needed. Let the user enter the sudo password and any MQTT secret directly in the terminal.
