"""
Rate limiting configuration for the application.

This module provides a global rate limiter instance that can be used
to limit request rates on API endpoints. Rate limiting is based on
client IP addresses.

For detailed documentation, see the module's README.md file.
"""

from slowapi import Limiter
from slowapi.util import get_remote_address

# Global rate limiter instance
# Uses client IP address as the key for rate limiting
limiter = Limiter(key_func=get_remote_address)