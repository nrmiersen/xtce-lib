"""Common validation utilities."""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Generic, TypeVar

from .xtce_path import XtcePath


class BaseValidationError(ABC):
    """Abstract base class for all validation errors."""

    @abstractmethod
    def format(self) -> str:
        """Return a formatted string representation of the error."""
        pass


@dataclass(frozen=True)
class XtceSchemaError(BaseValidationError):
    """An XTCE schema validation error."""

    line: int
    message: str

    def format(self) -> str:
        """Return a formatted string representation of the error."""
        return f"Line {self.line}: {self.message}"


@dataclass(frozen=True)
class XtceSemanticError(BaseValidationError):
    """An XTCE semantic validation error."""

    scope: XtcePath
    message: str

    def format(self) -> str:
        """Return a formatted string representation of the error."""
        return f"[{self.scope}] {self.message}"


ErrorType = TypeVar("ErrorType", bound=BaseValidationError)


@dataclass
class ValidationReport(Generic[ErrorType]):
    """A generic report for XTCE validation."""

    title: str
    errors: list[ErrorType] = field(default_factory=list)

    @property
    def is_valid(self) -> bool:
        """True if the validation pass found no errors."""
        return len(self.errors) == 0

    def add_error(self, error: ErrorType) -> None:
        """Append an error to the report."""
        self.errors.append(error)

    def summary(self) -> str:
        """Generate a console-friendly report."""
        if self.is_valid:
            return f"{self.title}: PASSED"

        lines = [f"{self.title}: FAILED with {len(self.errors)} errors"]
        for err in self.errors:
            lines.append(f"  {err.format()}")

        return "\n".join(lines)
