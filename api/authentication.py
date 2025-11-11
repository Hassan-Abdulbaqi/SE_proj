"""
Unsafe authentication utilities for local development only.

These helpers remove CSRF enforcement so the frontend can perform state-changing
requests without requesting a token first. Never ship this module to production.
"""

from rest_framework.authentication import SessionAuthentication


class DevSessionAuthentication(SessionAuthentication):
    """Session authentication without CSRF checks – development only."""

    def enforce_csrf(self, request):
        """Override the default CSRF enforcement hook to disable it."""
        return

