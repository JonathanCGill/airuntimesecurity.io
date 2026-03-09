"""Audit sinks — pluggable destinations for security events.

Ship events to your SIEM, log aggregator, or any other backend
by implementing the AuditSink interface.
"""

from __future__ import annotations

import json
import logging
from abc import ABC, abstractmethod
from typing import Any, Callable

from airs.telemetry.events import AISecurityEvent

logger = logging.getLogger(__name__)


class AuditSink(ABC):
    """Base class for audit event destinations."""

    @abstractmethod
    def handle(self, event: AISecurityEvent) -> None:
        """Process a security event.  Must not raise."""
        ...


class LogAuditSink(AuditSink):
    """Writes structured JSON events to a Python logger.

    Usage:
        from airs.telemetry import LogAuditSink, register_sink
        register_sink(LogAuditSink())
    """

    def __init__(
        self,
        logger_name: str = "airs.audit",
        level: int = logging.INFO,
    ) -> None:
        self._logger = logging.getLogger(logger_name)
        self._level = level

    def handle(self, event: AISecurityEvent) -> None:
        self._logger.log(self._level, event.to_json())


class CallbackAuditSink(AuditSink):
    """Sends events to a callable — useful for testing and custom pipelines.

    Usage:
        events = []
        register_sink(CallbackAuditSink(events.append))
    """

    def __init__(self, callback: Callable[[AISecurityEvent], None]) -> None:
        self._callback = callback

    def handle(self, event: AISecurityEvent) -> None:
        self._callback(event)


class BufferAuditSink(AuditSink):
    """Collects events in memory.  Useful for testing and batch export.

    Usage:
        sink = BufferAuditSink()
        register_sink(sink)
        # ... run pipeline ...
        for event in sink.events:
            print(event.to_json())
    """

    def __init__(self, max_size: int = 10_000) -> None:
        self.events: list[AISecurityEvent] = []
        self._max_size = max_size

    def handle(self, event: AISecurityEvent) -> None:
        if len(self.events) < self._max_size:
            self.events.append(event)

    def clear(self) -> None:
        self.events.clear()
