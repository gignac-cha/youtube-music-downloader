"""Middleware package."""

from presentation.middleware.security import SecurityHeadersMiddleware

__all__ = ["SecurityHeadersMiddleware"]
