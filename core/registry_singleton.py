"""
Registry Singleton - FIXED VERSION
Ensures all components share the same registry instance with proper synchronization
"""

import threading
import os
import fcntl
import time
import json
from pathlib import Path
from typing import Optional


class RegistrySingleton:
    """Thread-safe singleton pattern for registry management."""

    _instance = None
    _lock = threading.RLock()  # Reentrant lock
    _registry = None
    _file_locks = {}
    _last_reload = 0
    _reload_interval = 0.5  # Minimum seconds between reloads

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(RegistrySingleton, cls).__new__(cls)
                    # Import here to avoid circular dependency
                    from core.registry import RegistryManager

                    cls._instance._registry = RegistryManager()
                    cls._instance._last_reload = time.time()
        return cls._instance

    def get_registry(self):
        """Get the shared registry instance with automatic reload if needed."""
        with self._lock:
            # Check if files have been modified since last load
            if self._should_reload():
                self._reload_registry()
            return self._registry

    def _should_reload(self) -> bool:
        """Check if registry files have been modified."""
        current_time = time.time()
        if current_time - self._last_reload < self._reload_interval:
            return False

        # Check file modification times
        from config import AGENTS_REGISTRY_PATH, TOOLS_REGISTRY_PATH

        for path in [AGENTS_REGISTRY_PATH, TOOLS_REGISTRY_PATH]:
            if os.path.exists(path):
                mtime = os.path.getmtime(path)
                if mtime > self._last_reload:
                    return True
        return False

    def _reload_registry(self):
        """Reload registry from disk with file locking."""
        from core.registry import RegistryManager

        # Create new registry instance that will load from files
        new_registry = RegistryManager()

        # Atomic swap
        self._registry = new_registry
        self._last_reload = time.time()
        print(f"DEBUG: Registry reloaded at {self._last_reload}")

    def force_reload(self):
        """Force reload the registry from disk."""
        with self._lock:
            self._reload_registry()

    def acquire_file_lock(self, filepath: str):
        """Acquire file lock for atomic operations."""
        if filepath not in self._file_locks:
            lock_path = f"{filepath}.lock"
            self._file_locks[filepath] = open(lock_path, "w")

        fcntl.flock(self._file_locks[filepath], fcntl.LOCK_EX)

    def release_file_lock(self, filepath: str):
        """Release file lock."""
        if filepath in self._file_locks:
            fcntl.flock(self._file_locks[filepath], fcntl.LOCK_UN)

    def atomic_update(self, filepath: str, data: dict):
        """Atomically update a JSON file."""
        with self._lock:
            self.acquire_file_lock(filepath)
            try:
                # Write to temporary file first
                temp_path = f"{filepath}.tmp"
                with open(temp_path, "w") as f:
                    json.dump(data, f, indent=2, default=str)

                # Atomic rename
                os.replace(temp_path, filepath)

                # Force sync to disk
                os.sync()
            finally:
                self.release_file_lock(filepath)


# Global function to get shared registry
_singleton = None
_singleton_lock = threading.Lock()


def get_shared_registry():
    """Get the shared registry instance - thread-safe."""
    global _singleton
    if _singleton is None:
        with _singleton_lock:
            if _singleton is None:
                _singleton = RegistrySingleton()
    return _singleton.get_registry()


def force_global_reload():
    """Force reload all registry instances."""
    global _singleton
    if _singleton:
        _singleton.force_reload()
