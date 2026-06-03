"""OpenPokedex desktop launcher.

Starts the Flask app on a random free localhost port in a background thread,
then opens a native pywebview window pointing at it. The window uses the
OS-native webview component (Edge WebView2 on Windows), so this is a real
desktop app — not a browser tab.
"""
import os
import socket
import sys
import threading
import time
from urllib.request import urlopen
from urllib.error import URLError

import webview

import paths
from app import app


def _pick_free_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def _start_flask(port):
    # Bind to loopback only — this app never accepts remote connections.
    app.run(host="127.0.0.1", port=port, debug=False, use_reloader=False, threaded=True)


def _wait_for_flask(port, timeout=10.0):
    deadline = time.monotonic() + timeout
    url = f"http://127.0.0.1:{port}/"
    while time.monotonic() < deadline:
        try:
            with urlopen(url, timeout=0.5) as r:
                if r.status < 500:
                    return True
        except (URLError, ConnectionError, OSError):
            time.sleep(0.1)
    return False


def _icon_path():
    candidate = paths.bundled_resource_path("static/icon.png")
    return candidate if os.path.exists(candidate) else None


def main():
    port = _pick_free_port()
    flask_thread = threading.Thread(target=_start_flask, args=(port,), daemon=True)
    flask_thread.start()

    if not _wait_for_flask(port):
        sys.stderr.write("OpenPokedex: Flask backend failed to start.\n")
        sys.exit(1)

    window_kwargs = dict(
        title="OpenPokedex",
        url=f"http://127.0.0.1:{port}/",
        width=1280,
        height=800,
        min_size=(900, 600),
        resizable=True,
        maximized=True,
    )

    webview.create_window(**window_kwargs)
    webview.start()


if __name__ == "__main__":
    main()
