---
name: vm-gui-vnc
description: Set up and operate a lightweight graphical desktop on a headless Debian or Ubuntu VM with XFCE and TigerVNC, connect to it securely through an SSH tunnel, and launch GUI applications on the VNC display. Use when an agent needs a visible browser or desktop application in a remote VM, the user asks to access a VM GUI through VNC, or a graphical workflow cannot be completed with headless tools alone.
---

# VM GUI over VNC

Create a persistent XFCE desktop on a headless VM and expose it only through an SSH-forwarded VNC connection. Keep VNC bound to localhost; never open port 5900+ directly to the internet.

## Workflow

1. Inspect the host before changing it:

   ```bash
   . /etc/os-release && printf '%s %s\n' "$ID" "$VERSION_ID"
   command -v vncserver || true
   command -v startxfce4 || true
   vncserver -list 2>/dev/null || true
   ```

2. On Debian or Ubuntu, use the bundled helper:

   ```bash
   bash scripts/vm-gui-vnc.sh install
   bash scripts/vm-gui-vnc.sh configure
   ```

   Run `install` only with user authorization to install system packages. The command installs XFCE, TigerVNC, and `dbus-x11`.

3. Set the VNC password interactively as the user who will own the desktop:

   ```bash
   vncpasswd
   ```

   Never put the password in a command, log, script, repository, or chat response.

4. Start display `:1`, which maps to TCP port `5901`:

   ```bash
   bash scripts/vm-gui-vnc.sh start
   ```

   Override defaults when needed:

   ```bash
   VNC_DISPLAY=:2 VNC_GEOMETRY=1600x900 bash scripts/vm-gui-vnc.sh start
   ```

5. Tell the user to create the tunnel from their local computer:

   ```bash
   ssh -N -L 5901:127.0.0.1:5901 USER@VM_HOST
   ```

   Then connect a VNC viewer to `127.0.0.1:5901`. For display `:N`, use port `5900 + N` on both sides.

6. Launch the requested GUI application in the desktop:

   ```bash
   bash scripts/vm-gui-vnc.sh launch google-chrome
   bash scripts/vm-gui-vnc.sh launch xfce4-terminal
   ```

   If launching manually, set `DISPLAY` explicitly:

   ```bash
   DISPLAY=:1 nohup APPLICATION >/tmp/application-vnc.log 2>&1 &
   ```

7. Verify the session:

   ```bash
   bash scripts/vm-gui-vnc.sh status
   ss -ltn | grep 5901
   ```

   Accept only a loopback listener such as `127.0.0.1:5901` or `[::1]:5901`.

## Operating rules

- Run the desktop and GUI applications as a normal user, not root.
- Start VNC with `-localhost yes`; use SSH forwarding for remote access.
- Reuse an existing healthy display instead of starting duplicate sessions.
- Preserve an existing `~/.vnc/xstartup` unless it is broken or the user asked to replace it.
- Do not install a public web VNC gateway unless the user explicitly requests it and TLS/authentication are designed first.
- Do not disable the VM firewall or expose VNC ports in cloud firewall rules.
- Stop the desktop with `bash scripts/vm-gui-vnc.sh stop` when persistence is unnecessary.

## Troubleshooting

- If XFCE exits immediately, inspect `~/.vnc/*:N.log` and confirm `dbus-x11` is installed.
- If an application reports that it cannot open a display, launch it with the same `DISPLAY=:N` used by VNC.
- If a viewer cannot connect, verify the SSH tunnel remains running and the local/remote ports match the display number.
- If authentication fails, rerun `vncpasswd`; do not weaken authentication.
- X keyboard, audio, power-manager, or DPMS warnings are often non-fatal on headless VMs. Treat session exit, missing executables, and connection failures as actionable.

## Helper script

Use `scripts/vm-gui-vnc.sh` for repeatable installation, configuration, lifecycle, and application-launch commands. Read it before adapting the workflow to a non-Debian distribution or a desktop other than XFCE.
