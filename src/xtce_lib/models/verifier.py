"""Verifier models."""

from pydantic import Field
from xsdata.models.datatype import XmlDuration

from ._base import XtceBaseModel
from .codec import DynamicValue
from .command import ArgumentAssignment
from .common import OptionalNameDescriptionBase
from .enum import TimeWindowIsRelativeTo
from .processing import BooleanExpression, Comparison, InputAlgorithm
from .reference import ContainerRef, ParameterRef


class ChangeValue(XtceBaseModel):
    # TODO why does this even exist
    value: float = Field(...)


class ParameterValueChange(XtceBaseModel):
    parameter_ref: ParameterRef = Field(...)
    change: ChangeValue = Field(...)


class CheckWindow(XtceBaseModel):
    time_to_start_checking: XmlDuration | None = Field(default=None)
    time_to_stop_checking: XmlDuration | None = Field(default=None)
    time_window_is_relative_to: TimeWindowIsRelativeTo = Field(
        default=TimeWindowIsRelativeTo.TIME_LAST_VERIFIER_PASSED
    )


class CheckWindowAlgorithms(XtceBaseModel):
    start_check: InputAlgorithm = Field(...)
    stop_time: InputAlgorithm = Field(...)  # TODO is this the right name?


class CommandVerifier(OptionalNameDescriptionBase):
    verifier: (
        Comparison
        | list[Comparison]
        | ContainerRef
        | ParameterValueChange
        | InputAlgorithm
        | BooleanExpression
        | None
    ) = Field(default=None)
    check_window_or_check_window_algorithms: (
        CheckWindow | CheckWindowAlgorithms | None
    ) = Field(default=None)
    argument_restrictions: list[ArgumentAssignment] = Field(
        default_factory=list, min_length=1
    )


# TODO probably get rid of these redundant classes, need to see what's in xsd


class TransferredToRangeVerifier(CommandVerifier):
    # Nothing
    pass


class SentFromRangeVerifier(CommandVerifier):
    # Nothing
    pass


class ReceivedVerifier(CommandVerifier):
    # Nothing
    pass


class AcceptedVerifier(CommandVerifier):
    # Nothing
    pass


class QueuedVerifier(CommandVerifier):
    # Nothing
    pass


class ExecutionVerifier(CommandVerifier):
    percent_complete: float | DynamicValue | None = Field(default=None, ge=0, le=100)


class CompleteVerifier(CommandVerifier):
    return_parm_ref: ParameterRef | None = Field(default=None)


class FailedVerifier(CommandVerifier):
    return_parm_ref: ParameterRef | None = Field(default=None)


# TODO maybe make parent class for Complete and Failed


class VerifierSet(XtceBaseModel):
    transferred_to_range_verifier: TransferredToRangeVerifier | None = Field(
        default=None
    )
    sent_from_range_verifier: SentFromRangeVerifier | None = Field(default=None)
    received_verifier: ReceivedVerifier | None = Field(default=None)
    accepted_verifier: AcceptedVerifier | None = Field(default=None)
    queued_verifier: QueuedVerifier | None = Field(default=None)
    execution_verifier: list[ExecutionVerifier] = Field(default_factory=list)
    complete_verifier: list[CompleteVerifier] = Field(default_factory=list)
    failed_verifier: FailedVerifier | None = Field(default=None)
