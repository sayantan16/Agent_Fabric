"""
Registry Singleton
Ensures all components share the same registry instance
"""

from core.registry import RegistryManager


class RegistrySingleton:
    """Singleton pattern for registry management."""

    _instance = None
    _registry = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(RegistrySingleton, cls).__new__(cls)
            cls._registry = RegistryManager()
        return cls._instance

    def get_registry(self) -> RegistryManager:
        """Get the shared registry instance."""
        return self._registry

    def reload_registry(self):
        """Force reload the registry from disk."""
        self._registry = RegistryManager()

    def force_reload(self):
        """Force reload the registry from disk for all instances."""
        self._registry = RegistryManager()


# Global function to get shared registry
def get_shared_registry() -> RegistryManager:
    """Get the shared registry instance."""
    return RegistrySingleton().get_registry()
