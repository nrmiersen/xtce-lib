# Commands and Arguments

Command definitions, argument types and transmission constraints. See [Command Verification](verification.md) for verifiers. Import these names from `xtce_lib.xtce`.

::: xtce_lib.xtce
    options:
      show_root_heading: false
      show_root_toc_entry: false
      members:
        - MetaCommand
        - BaseMetaCommand
        - BlockMetaCommand
        - MetaCommandRef
        - MetaCommandStep
        - Argument
        - ArgumentAssignment
        - IntegerArgument
        - FloatArgument
        - StringArgument
        - BinaryArgument
        - BooleanArgument
        - EnumeratedArgument
        - ArrayArgument
        - AggregateArgument
        - AbsoluteTimeArgument
        - RelativeTimeArgument
        - TransmissionConstraint
        - Significance
        - ContextSignificance
        - Interlock
        - ParameterToSet
        - ParameterToSuspendAlarmsOn