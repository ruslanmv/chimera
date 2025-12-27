"""
Chimera Desktop Launcher using Eel
Integrates React frontend with Python backend in a desktop application
"""

import eel
import uvicorn
import asyncio
import threading
import os
import sys
from pathlib import Path
import time
import httpx

# Add backend to path
backend_path = Path(__file__).parent.parent
sys.path.insert(0, str(backend_path))

from backend.main import app
from backend.core.manager import engine


class ChimeraLauncher:
    """Main launcher for Chimera desktop application"""

    def __init__(self, frontend_path="frontend/dist", backend_port=8000, frontend_port=8080):
        self.frontend_path = frontend_path
        self.backend_port = backend_port
        self.frontend_port = frontend_port
        self.backend_thread = None
        self.backend_started = False

    def start_backend_server(self):
        """Start FastAPI backend server in a separate thread"""
        def run_server():
            try:
                # Initialize engine
                engine.load_plugins()

                # Run uvicorn
                uvicorn.run(
                    app,
                    host="127.0.0.1",
                    port=self.backend_port,
                    log_level="info",
                    access_log=False
                )
            except Exception as e:
                print(f"❌ Backend server error: {e}")

        self.backend_thread = threading.Thread(target=run_server, daemon=True)
        self.backend_thread.start()
        print(f"✅ Backend server starting on http://127.0.0.1:{self.backend_port}")

    def wait_for_backend(self, timeout=30):
        """Wait for backend to be ready"""
        print("⏳ Waiting for backend to start...")
        start_time = time.time()

        while time.time() - start_time < timeout:
            try:
                response = httpx.get(f"http://127.0.0.1:{self.backend_port}/api/health", timeout=2)
                if response.status_code == 200:
                    self.backend_started = True
                    print(f"✅ Backend ready! ({response.json()})")
                    return True
            except (httpx.ConnectError, httpx.TimeoutException):
                time.sleep(0.5)
            except Exception as e:
                print(f"⚠️  Backend check error: {e}")
                time.sleep(0.5)

        print("❌ Backend failed to start within timeout")
        return False

    def build_frontend(self):
        """Build React frontend if needed"""
        dist_path = Path(self.frontend_path)

        if not dist_path.exists():
            print("📦 Building frontend...")
            os.chdir("frontend")
            os.system("npm run build")
            os.chdir("..")
            print("✅ Frontend built successfully")
        else:
            print(f"✅ Using existing frontend build at {self.frontend_path}")

    def launch(self, mode='chrome', size=(1400, 900)):
        """Launch the Chimera desktop application"""
        print("🚀 Starting Chimera Desktop Application...")
        print("=" * 60)

        # Start backend server
        self.start_backend_server()

        # Wait for backend to be ready
        if not self.wait_for_backend():
            print("❌ Cannot start application - backend not responding")
            return

        # Build frontend if needed
        self.build_frontend()

        # Initialize Eel with frontend folder
        try:
            eel.init(self.frontend_path)
        except Exception as e:
            print(f"❌ Failed to initialize Eel: {e}")
            print(f"Make sure {self.frontend_path} exists and contains index.html")
            return

        # Configure Eel options
        eel_options = {
            'mode': mode,
            'host': '127.0.0.1',
            'port': self.frontend_port,
            'size': size,
            'position': None,
            'disable_cache': False,
            'close_callback': self.on_close
        }

        print(f"🌐 Starting Eel frontend on http://127.0.0.1:{self.frontend_port}")
        print(f"🖥️  Browser mode: {mode}")
        print("=" * 60)
        print("\n✨ Chimera is now running!")
        print(f"   Frontend: http://127.0.0.1:{self.frontend_port}")
        print(f"   Backend:  http://127.0.0.1:{self.backend_port}")
        print(f"   API Docs: http://127.0.0.1:{self.backend_port}/docs")
        print("\nPress Ctrl+C to stop the application\n")

        try:
            # Start Eel (this blocks until window is closed)
            eel.start('index.html', **eel_options)
        except (SystemExit, KeyboardInterrupt):
            print("\n🛑 Shutting down Chimera...")
        except Exception as e:
            print(f"\n❌ Error running Eel: {e}")
            print(f"Falling back to web browser at http://127.0.0.1:{self.frontend_port}")
            print("Press Ctrl+C to stop")
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                print("\n🛑 Shutting down Chimera...")

    def on_close(self, page, sockets):
        """Callback when Eel window is closed"""
        print("\n🛑 Application window closed")
        print("Shutting down...")


def main():
    """Main entry point for Chimera launcher"""
    import argparse

    parser = argparse.ArgumentParser(description="Chimera Desktop Application Launcher")
    parser.add_argument('--mode', default='chrome', choices=['chrome', 'electron', 'edge', 'firefox', 'default'],
                       help='Browser mode for Eel (default: chrome)')
    parser.add_argument('--backend-port', type=int, default=8000,
                       help='Backend server port (default: 8000)')
    parser.add_argument('--frontend-port', type=int, default=8080,
                       help='Frontend server port (default: 8080)')
    parser.add_argument('--width', type=int, default=1400,
                       help='Window width (default: 1400)')
    parser.add_argument('--height', type=int, default=900,
                       help='Window height (default: 900)')
    parser.add_argument('--dev', action='store_true',
                       help='Use development frontend (frontend/src)')

    args = parser.parse_args()

    # Determine frontend path
    frontend_path = "frontend/src" if args.dev else "frontend/dist"

    # Create and launch
    launcher = ChimeraLauncher(
        frontend_path=frontend_path,
        backend_port=args.backend_port,
        frontend_port=args.frontend_port
    )

    launcher.launch(
        mode=args.mode,
        size=(args.width, args.height)
    )


if __name__ == "__main__":
    main()
