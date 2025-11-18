"""Retry service for handling transient failures."""

import asyncio
import logging
from collections.abc import Callable
from typing import TypeVar

T = TypeVar("T")

logger = logging.getLogger(__name__)


class RetryService:
    """Service for retrying operations with exponential backoff."""

    def __init__(
        self, max_retries: int = 3, base_delay: float = 1.0, max_delay: float = 60.0
    ) -> None:
        """Initialize retry service.

        Args:
            max_retries: Maximum number of retry attempts
            base_delay: Base delay between retries in seconds
            max_delay: Maximum delay between retries in seconds
        """
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.max_delay = max_delay

    async def retry_async(
        self,
        func: Callable[[], T],
        operation_name: str,
        *,
        retryable_exceptions: tuple = (Exception,),
    ) -> T:
        """Retry an async operation with exponential backoff.

        Args:
            func: Async function to retry
            operation_name: Name of the operation for logging
            retryable_exceptions: Tuple of exception types to retry on

        Returns:
            Result from the function

        Raises:
            The last exception if all retries fail
        """
        last_exception = None

        for attempt in range(self.max_retries + 1):
            try:
                result = await func()
                if attempt > 0:
                    logger.info(
                        f"{operation_name} succeeded after {attempt} retries"
                    )
                return result

            except retryable_exceptions as e:
                last_exception = e

                if attempt < self.max_retries:
                    # Calculate delay with exponential backoff
                    delay = min(self.base_delay * (2**attempt), self.max_delay)

                    logger.warning(
                        f"{operation_name} failed (attempt {attempt + 1}/{self.max_retries + 1}): {e}. "
                        f"Retrying in {delay:.1f}s..."
                    )

                    await asyncio.sleep(delay)
                else:
                    logger.error(
                        f"{operation_name} failed after {self.max_retries + 1} attempts: {e}"
                    )

        # All retries exhausted
        raise last_exception
