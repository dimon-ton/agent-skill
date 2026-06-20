#!/usr/bin/env bash
set -euo pipefail

display="${VNC_DISPLAY:-:1}"
geometry="${VNC_GEOMETRY:-1440x900}"
depth="${VNC_DEPTH:-24}"

if [[ ! "$display" =~ ^:[0-9]+$ ]]; then
  echo "VNC_DISPLAY must look like :1" >&2
  exit 2
fi

display_number="${display#:}"
port=$((5900 + display_number))
vnc_dir="${HOME}/.vnc"
xstartup="${vnc_dir}/xstartup"

usage() {
  cat <<'EOF'
Usage: vm-gui-vnc.sh install|configure|start|stop|status|launch [command...]

Environment:
  VNC_DISPLAY   Display number, default :1
  VNC_GEOMETRY  Desktop size, default 1440x900
  VNC_DEPTH     Color depth, default 24
EOF
}

require_command() {
  if ! command -v "$1" >/dev/null 2>&1; then
    echo "Missing required command: $1" >&2
    exit 1
  fi
}

install_packages() {
  if [[ ! -r /etc/os-release ]]; then
    echo "Cannot identify the operating system." >&2
    exit 1
  fi

  # shellcheck disable=SC1091
  . /etc/os-release
  case "${ID:-}" in
    debian|ubuntu) ;;
    *)
      echo "Automatic installation supports Debian and Ubuntu only." >&2
      exit 1
      ;;
  esac

  require_command sudo
  sudo apt-get update
  sudo DEBIAN_FRONTEND=noninteractive apt-get install -y \
    xfce4 xfce4-goodies tigervnc-standalone-server dbus-x11
}

configure_xstartup() {
  mkdir -p "$vnc_dir"
  chmod 700 "$vnc_dir"

  if [[ -e "$xstartup" ]]; then
    echo "$xstartup already exists; leaving it unchanged."
    return
  fi

  cat >"$xstartup" <<'EOF'
#!/bin/sh
unset SESSION_MANAGER
unset DBUS_SESSION_BUS_ADDRESS
exec dbus-launch --exit-with-session startxfce4
EOF
  chmod 700 "$xstartup"
  echo "Created $xstartup"
}

start_server() {
  require_command vncserver
  require_command startxfce4

  if vncserver -list 2>/dev/null | awk 'NR > 2 {print $1}' | grep -Fxq "$display"; then
    echo "VNC display $display is already running."
    return
  fi

  if [[ ! -f "${vnc_dir}/passwd" ]]; then
    echo "No VNC password found. Run: vncpasswd" >&2
    exit 1
  fi

  configure_xstartup
  vncserver -localhost yes "$display" -geometry "$geometry" -depth "$depth"
  echo "VNC display $display is listening on localhost port $port."
}

stop_server() {
  require_command vncserver
  vncserver -kill "$display"
}

show_status() {
  require_command vncserver
  vncserver -list
  echo
  echo "Expected secure listener for $display: localhost:$port"
  ss -ltn 2>/dev/null | awk -v port=":$port" '$4 ~ port "$" {print}' || true
}

launch_app() {
  if (($# == 0)); then
    echo "Provide an application command after 'launch'." >&2
    exit 2
  fi

  if ! vncserver -list 2>/dev/null | awk 'NR > 2 {print $1}' | grep -Fxq "$display"; then
    echo "VNC display $display is not running." >&2
    exit 1
  fi

  log_name="$(basename "$1" | tr -c '[:alnum:]._- ' '_' | tr -d ' ')"
  log_file="/tmp/${log_name:-gui-app}-vnc-${display_number}.log"
  DISPLAY="$display" nohup "$@" >"$log_file" 2>&1 &
  echo "Started $* on $display (PID $!, log: $log_file)"
}

case "${1:-}" in
  install)
    install_packages
    ;;
  configure)
    configure_xstartup
    ;;
  start)
    start_server
    ;;
  stop)
    stop_server
    ;;
  status)
    show_status
    ;;
  launch)
    shift
    launch_app "$@"
    ;;
  *)
    usage
    exit 2
    ;;
esac
