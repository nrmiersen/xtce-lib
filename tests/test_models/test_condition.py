"""Test condition models."""

from __future__ import annotations

import datetime

import pytest
from pydantic import ValidationError

from xtce_lib import (
    DowngradePolicy,
    XtceDowngradeError,
    XtcePath,
    XtceUnsupportedError,
    XtceVersion,
    xtce,
)
from xtce_lib.generated import xtce_1_2

VERSIONS = [XtceVersion.V1_1, XtceVersion.V1_2, XtceVersion.V1_3]
SUPPORTED_CONDITION_VERSIONS = [XtceVersion.V1_2, XtceVersion.V1_3]


def _make_parameter_instance_ref() -> xtce.ParameterInstanceRef:
    return xtce.ParameterInstanceRef(
        ref=XtcePath("/TestSystem/ParameterA"),
        instance=-1,
        use_calibrated_value=False,
    )


def _make_argument_instance_ref() -> xtce.ArgumentInstanceRef:
    return xtce.ArgumentInstanceRef(ref="ArgumentA", use_calibrated_value=False)


def _make_comparison(value: object) -> xtce.Comparison:
    return xtce.Comparison(
        ref=XtcePath("/TestSystem/ParameterA"),
        instance=1,
        use_calibrated_value=True,
        comparison_operator=xtce.ComparisonOperator.GT,
        value=value,  # type: ignore[arg-type]
    )


def _make_argument_comparison(value: object) -> xtce.ArgumentComparison:
    return xtce.ArgumentComparison(
        instance_ref=_make_parameter_instance_ref(),
        comparison_operator=xtce.ComparisonOperator.NEQ,
        value=value,  # type: ignore[arg-type]
    )


class TestComparison:
    """Test Comparison model."""

    @pytest.mark.parametrize(
        "value",
        [
            12,
            3.5,
            "armed",
            True,
            b"\xab\x12",
            datetime.timedelta(days=1, seconds=5),
            datetime.datetime(2024, 1, 2, 3, 4, 5),
        ],
    )
    @pytest.mark.parametrize("version", VERSIONS)
    def test_round_trip_through_xsdata_preserves_value(
        self,
        version: XtceVersion,
        value: object,
    ) -> None:
        """Round-trip Comparison values through every supported version."""
        original = _make_comparison(value)

        round_tripped = xtce.Comparison.from_xsdata(
            original.to_xsdata(version),
            version,
        )

        assert round_tripped == original


class TestArgumentComparison:
    """Test ArgumentComparison model."""

    @pytest.mark.parametrize("version", [XtceVersion.V1_2, XtceVersion.V1_3])
    def test_round_trip_with_parameter_instance_ref(
        self,
        version: XtceVersion,
    ) -> None:
        """Round-trip ArgumentComparison with a parameter instance reference."""
        original = xtce.ArgumentComparison(
            instance_ref=_make_parameter_instance_ref(),
            comparison_operator=xtce.ComparisonOperator.LTE,
            value=datetime.timedelta(seconds=15),
        )

        round_tripped = xtce.ArgumentComparison.from_xsdata(
            original.to_xsdata(version),
            version,
        )

        assert round_tripped == original

    @pytest.mark.parametrize("version", [XtceVersion.V1_2, XtceVersion.V1_3])
    def test_round_trip_with_argument_instance_ref(
        self,
        version: XtceVersion,
    ) -> None:
        """Round-trip ArgumentComparison with an argument instance reference."""
        original = xtce.ArgumentComparison(
            instance_ref=_make_argument_instance_ref(),
            comparison_operator=xtce.ComparisonOperator.GTE,
            value=b"\xab\x12",
        )

        round_tripped = xtce.ArgumentComparison.from_xsdata(
            original.to_xsdata(version),
            version,
        )

        assert round_tripped == original

    def test_v1_1_is_unsupported(self) -> None:
        """Verify ArgumentComparison rejects XTCE v1.1."""
        with pytest.raises(XtceUnsupportedError):
            xtce.ArgumentComparison.from_xsdata(
                xtce_1_2.ArgumentComparisonType(
                    choice=xtce_1_2.ParameterInstanceRefType(
                        parameter_ref="/TestSystem/ParameterA",
                        instance=0,
                        use_calibrated_value=True,
                    ),
                    comparison_operator=xtce_1_2.ComparisonOperatorsType.EQUALS_SIGN_EQUALS_SIGN,
                    value="1",
                ),
                XtceVersion.V1_1,
            )

        with pytest.raises(XtceUnsupportedError):
            xtce.ArgumentComparison(
                instance_ref=_make_parameter_instance_ref(),
                value=1,
            ).to_xsdata(XtceVersion.V1_1)


class TestComparisonCheck:
    """Test ComparisonCheck model."""

    @pytest.mark.parametrize(
        "right",
        [
            42,
            "locked",
            datetime.timedelta(minutes=3),
            datetime.datetime(2024, 5, 6, 7, 8, 9),
        ],
    )
    @pytest.mark.parametrize("version", VERSIONS)
    def test_round_trip_with_literal_right_side(
        self,
        version: XtceVersion,
        right: object,
    ) -> None:
        """Round-trip ComparisonCheck with literal right-hand values."""
        original = xtce.ComparisonCheck(
            left=_make_parameter_instance_ref(),
            comparison_operator=xtce.ComparisonOperator.EQ,
            right=right,  # type: ignore[arg-type]
        )

        round_tripped = xtce.ComparisonCheck.from_xsdata(
            original.to_xsdata(version),
            version,
        )

        assert round_tripped == original

    @pytest.mark.parametrize("version", VERSIONS)
    def test_round_trip_with_parameter_right_side(
        self,
        version: XtceVersion,
    ) -> None:
        """Round-trip ComparisonCheck with a parameter right-hand value."""
        original = xtce.ComparisonCheck(
            left=_make_parameter_instance_ref(),
            comparison_operator=xtce.ComparisonOperator.NEQ,
            right=xtce.ParameterInstanceRef(
                ref=XtcePath("/TestSystem/ParameterB"),
                instance=2,
                use_calibrated_value=True,
            ),
        )

        round_tripped = xtce.ComparisonCheck.from_xsdata(
            original.to_xsdata(version),
            version,
        )

        assert round_tripped == original


class TestArgumentComparisonCheck:
    """Test ArgumentComparisonCheck model."""

    @pytest.mark.parametrize(
        "right",
        [
            7,
            True,
            datetime.timedelta(seconds=20),
            datetime.datetime(2024, 3, 4, 5, 6, 7),
        ],
    )
    @pytest.mark.parametrize("version", SUPPORTED_CONDITION_VERSIONS)
    def test_round_trip_with_literal_right_side(
        self,
        version: XtceVersion,
        right: object,
    ) -> None:
        """Round-trip ArgumentComparisonCheck with literal values."""
        original = xtce.ArgumentComparisonCheck(
            left=_make_argument_instance_ref(),
            comparison_operator=xtce.ComparisonOperator.GT,
            right=right,  # type: ignore[arg-type]
        )

        round_tripped = xtce.ArgumentComparisonCheck.from_xsdata(
            original.to_xsdata(version),
            version,
        )

        assert round_tripped == original

    @pytest.mark.parametrize("version", SUPPORTED_CONDITION_VERSIONS)
    @pytest.mark.parametrize(
        "right",
        [
            xtce.ParameterInstanceRef(
                ref=XtcePath("/TestSystem/ParameterB"),
                instance=0,
                use_calibrated_value=True,
            ),
            xtce.ArgumentInstanceRef(ref="ArgumentB", use_calibrated_value=True),
        ],
    )
    def test_round_trip_with_instance_ref_right_side(
        self,
        version: XtceVersion,
        right: xtce.ParameterInstanceRef | xtce.ArgumentInstanceRef,
    ) -> None:
        """Round-trip ArgumentComparisonCheck with instance-reference values."""
        original = xtce.ArgumentComparisonCheck(
            left=_make_argument_instance_ref(),
            comparison_operator=xtce.ComparisonOperator.LTE,
            right=right,
        )

        round_tripped = xtce.ArgumentComparisonCheck.from_xsdata(
            original.to_xsdata(version),
            version,
        )

        assert round_tripped == original

    def test_v1_1_is_unsupported(self) -> None:
        """Verify ArgumentComparisonCheck rejects XTCE v1.1."""
        with pytest.raises(XtceUnsupportedError):
            xtce.ArgumentComparisonCheck.from_xsdata(
                xtce_1_2.ArgumentComparisonCheckType(
                    choice=[xtce_1_2.ArgumentInstanceRefType(argument_ref="Arg1")],
                    comparison_operator=xtce_1_2.ComparisonOperatorsType.EQUALS_SIGN_EQUALS_SIGN,
                    value="1",
                ),
                XtceVersion.V1_1,
            )

        with pytest.raises(XtceUnsupportedError):
            xtce.ArgumentComparisonCheck(
                left=_make_argument_instance_ref(),
                right=1,
                comparison_operator=xtce.ComparisonOperator.EQ,
            ).to_xsdata(XtceVersion.V1_1)


class TestConditionGroups:
    """Test grouped condition expressions."""

    def test_anded_conditions_round_trip(self) -> None:
        """Round-trip AndedConditions through every supported version."""
        original = xtce.AndedConditions(
            conditions=[
                xtce.ComparisonCheck(
                    left=_make_parameter_instance_ref(),
                    comparison_operator=xtce.ComparisonOperator.GT,
                    right=1,
                ),
                xtce.ComparisonCheck(
                    left=xtce.ParameterInstanceRef(
                        ref=XtcePath("/TestSystem/ParameterB"),
                        instance=0,
                        use_calibrated_value=True,
                    ),
                    comparison_operator=xtce.ComparisonOperator.LT,
                    right=2,
                ),
            ]
        )

        for version in VERSIONS:
            round_tripped = xtce.AndedConditions.from_xsdata(
                original.to_xsdata(version),
                version,
            )

            assert round_tripped == original

    def test_ored_conditions_round_trip(self) -> None:
        """Round-trip OredConditions through every supported version."""
        original = xtce.OredConditions(
            conditions=[
                xtce.ComparisonCheck(
                    left=_make_parameter_instance_ref(),
                    comparison_operator=xtce.ComparisonOperator.EQ,
                    right=1,
                ),
                xtce.AndedConditions(
                    conditions=[
                        xtce.ComparisonCheck(
                            left=xtce.ParameterInstanceRef(
                                ref=XtcePath("/TestSystem/ParameterB"),
                                instance=0,
                                use_calibrated_value=True,
                            ),
                            comparison_operator=xtce.ComparisonOperator.GTE,
                            right=2,
                        ),
                        xtce.ComparisonCheck(
                            left=xtce.ParameterInstanceRef(
                                ref=XtcePath("/TestSystem/ParameterC"),
                                instance=0,
                                use_calibrated_value=True,
                            ),
                            comparison_operator=xtce.ComparisonOperator.LTE,
                            right=3,
                        ),
                    ]
                ),
            ]
        )

        for version in VERSIONS:
            round_tripped = xtce.OredConditions.from_xsdata(
                original.to_xsdata(version),
                version,
            )

            assert round_tripped == original

    def test_argument_anded_conditions_round_trip(self) -> None:
        """Round-trip ArgumentAndedConditions through supported versions."""
        original = xtce.ArgumentAndedConditions(
            conditions=[
                xtce.ArgumentComparisonCheck(
                    left=_make_argument_instance_ref(),
                    comparison_operator=xtce.ComparisonOperator.GT,
                    right=1,
                ),
                xtce.ArgumentComparisonCheck(
                    left=xtce.ArgumentInstanceRef(ref="ArgumentB"),
                    comparison_operator=xtce.ComparisonOperator.LT,
                    right=2,
                ),
            ]
        )

        for version in SUPPORTED_CONDITION_VERSIONS:
            round_tripped = xtce.ArgumentAndedConditions.from_xsdata(
                original.to_xsdata(version),
                version,
            )

            assert round_tripped == original

    def test_argument_ored_conditions_round_trip(self) -> None:
        """Round-trip ArgumentOredConditions through supported versions."""
        original = xtce.ArgumentOredConditions(
            conditions=[
                xtce.ArgumentComparisonCheck(
                    left=_make_argument_instance_ref(),
                    comparison_operator=xtce.ComparisonOperator.EQ,
                    right=1,
                ),
                xtce.ArgumentAndedConditions(
                    conditions=[
                        xtce.ArgumentComparisonCheck(
                            left=xtce.ArgumentInstanceRef(ref="ArgumentB"),
                            comparison_operator=xtce.ComparisonOperator.GTE,
                            right=2,
                        ),
                        xtce.ArgumentComparisonCheck(
                            left=xtce.ArgumentInstanceRef(ref="ArgumentC"),
                            comparison_operator=xtce.ComparisonOperator.LTE,
                            right=3,
                        ),
                    ]
                ),
            ]
        )

        for version in SUPPORTED_CONDITION_VERSIONS:
            round_tripped = xtce.ArgumentOredConditions.from_xsdata(
                original.to_xsdata(version),
                version,
            )

            assert round_tripped == original


class TestBooleanExpressionWrappers:
    """Test boolean-expression wrapper dispatch."""

    @pytest.mark.parametrize(
        "comparison",
        [
            xtce.ComparisonCheck(
                left=_make_parameter_instance_ref(),
                comparison_operator=xtce.ComparisonOperator.EQ,
                right=1,
            ),
            xtce.AndedConditions(
                conditions=[
                    xtce.ComparisonCheck(
                        left=_make_parameter_instance_ref(),
                        comparison_operator=xtce.ComparisonOperator.GT,
                        right=1,
                    ),
                    xtce.ComparisonCheck(
                        left=xtce.ParameterInstanceRef(
                            ref=XtcePath("/TestSystem/ParameterB"),
                            instance=0,
                            use_calibrated_value=True,
                        ),
                        comparison_operator=xtce.ComparisonOperator.LT,
                        right=2,
                    ),
                ]
            ),
            xtce.OredConditions(
                conditions=[
                    xtce.ComparisonCheck(
                        left=_make_parameter_instance_ref(),
                        comparison_operator=xtce.ComparisonOperator.EQ,
                        right=1,
                    ),
                    xtce.ComparisonCheck(
                        left=xtce.ParameterInstanceRef(
                            ref=XtcePath("/TestSystem/ParameterB"),
                            instance=0,
                            use_calibrated_value=True,
                        ),
                        comparison_operator=xtce.ComparisonOperator.NEQ,
                        right=2,
                    ),
                ]
            ),
        ],
    )
    def test_boolean_expression_round_trip(self, comparison: object) -> None:
        """Round-trip BooleanExpression wrapper variants."""
        original = xtce.BooleanExpression(comparison=comparison)  # type: ignore[arg-type]

        for version in VERSIONS:
            round_tripped = xtce.BooleanExpression.from_xsdata(
                original.to_xsdata(version),
                version,
            )

            assert round_tripped == original

    @pytest.mark.parametrize(
        "comparison",
        [
            xtce.ArgumentComparisonCheck(
                left=_make_argument_instance_ref(),
                comparison_operator=xtce.ComparisonOperator.EQ,
                right=1,
            ),
            xtce.ArgumentAndedConditions(
                conditions=[
                    xtce.ArgumentComparisonCheck(
                        left=_make_argument_instance_ref(),
                        comparison_operator=xtce.ComparisonOperator.GT,
                        right=1,
                    ),
                    xtce.ArgumentComparisonCheck(
                        left=xtce.ArgumentInstanceRef(ref="ArgumentB"),
                        comparison_operator=xtce.ComparisonOperator.LT,
                        right=2,
                    ),
                ]
            ),
            xtce.ArgumentOredConditions(
                conditions=[
                    xtce.ArgumentComparisonCheck(
                        left=_make_argument_instance_ref(),
                        comparison_operator=xtce.ComparisonOperator.EQ,
                        right=1,
                    ),
                    xtce.ArgumentComparisonCheck(
                        left=xtce.ArgumentInstanceRef(ref="ArgumentB"),
                        comparison_operator=xtce.ComparisonOperator.NEQ,
                        right=2,
                    ),
                ]
            ),
        ],
    )
    def test_argument_boolean_expression_round_trip(self, comparison: object) -> None:
        """Round-trip ArgumentBooleanExpression wrapper variants."""
        original = xtce.ArgumentBooleanExpression(comparison=comparison)  # type: ignore[arg-type]

        for version in SUPPORTED_CONDITION_VERSIONS:
            round_tripped = xtce.ArgumentBooleanExpression.from_xsdata(
                original.to_xsdata(version),
                version,
            )

            assert round_tripped == original


class TestMatchCriteria:
    """Test match-criteria wrappers."""

    def test_match_criteria_round_trip_for_list_boolean_and_input_algorithm(
        self,
    ) -> None:
        """Round-trip MatchCriteria list, boolean, and algorithm cases."""
        list_criteria = xtce.MatchCriteria(
            criteria=[
                _make_comparison(1),
                xtce.Comparison(
                    ref=XtcePath("/TestSystem/ParameterB"),
                    instance=0,
                    use_calibrated_value=True,
                    comparison_operator=xtce.ComparisonOperator.NEQ,
                    value=datetime.timedelta(seconds=2),
                ),
            ]
        )
        boolean_criteria = xtce.MatchCriteria(
            criteria=xtce.BooleanExpression(
                comparison=xtce.ComparisonCheck(
                    left=_make_parameter_instance_ref(),
                    comparison_operator=xtce.ComparisonOperator.GT,
                    right=2,
                )
            )
        )
        input_algorithm_criteria = xtce.MatchCriteria(
            criteria=xtce.InputAlgorithm(
                name="InputAlgo",
                aliases=[xtce.Alias(namespace="Test", alias="InputAlgo")],
                ancillary_data=[xtce.AncillaryData(name="meta", value="1")],
                inputs=[
                    xtce.InputParameterInstanceRef(
                        ref=XtcePath("/TestSystem/ParameterA"),
                        input_name="InputA",
                    )
                ],
            )
        )

        for version in VERSIONS:
            for original in [list_criteria, boolean_criteria]:
                round_tripped = xtce.MatchCriteria.from_xsdata(
                    original.to_xsdata(version),
                    version,
                )

                assert round_tripped == original

        for version in SUPPORTED_CONDITION_VERSIONS:
            round_tripped = xtce.MatchCriteria.from_xsdata(
                input_algorithm_criteria.to_xsdata(version),
                version,
            )

            assert round_tripped == input_algorithm_criteria

    def test_context_match_round_trip(self) -> None:
        """Round-trip ContextMatch through supported versions."""
        original = xtce.ContextMatch(
            criteria=[
                xtce.Comparison(
                    ref=XtcePath("/TestSystem/ParameterA"),
                    instance=0,
                    use_calibrated_value=True,
                    comparison_operator=xtce.ComparisonOperator.EQ,
                    value=1,
                ),
                xtce.Comparison(
                    ref=XtcePath("/TestSystem/ParameterB"),
                    instance=0,
                    use_calibrated_value=False,
                    comparison_operator=xtce.ComparisonOperator.GTE,
                    value=2,
                ),
            ]
        )

        for version in VERSIONS:
            round_tripped = xtce.ContextMatch.from_xsdata(
                original.to_xsdata(version),
                version,
            )

            assert round_tripped == original

    def test_discrete_lookup_round_trip(self) -> None:
        """Round-trip DiscreteLookup through supported versions."""
        original = xtce.DiscreteLookup(
            criteria=xtce.Comparison(
                ref=XtcePath("/TestSystem/ParameterA"),
                instance=0,
                use_calibrated_value=True,
                comparison_operator=xtce.ComparisonOperator.EQ,
                value=1,
            ),
            value=7,
        )

        for version in SUPPORTED_CONDITION_VERSIONS:
            round_tripped = xtce.DiscreteLookup.from_xsdata(
                original.to_xsdata(version),
                version,
            )

            assert round_tripped == original

    def test_discrete_lookup_list_enforces_default_value_on_v1_2(self) -> None:
        """Verify v1.2 drops DiscreteLookupList defaults under IGNORE."""
        original = xtce.DiscreteLookupList(
            lookups=[
                xtce.DiscreteLookup(
                    criteria=xtce.Comparison(
                        ref=XtcePath("/TestSystem/ParameterA"),
                        instance=0,
                        use_calibrated_value=True,
                        comparison_operator=xtce.ComparisonOperator.EQ,
                        value=1,
                    ),
                    value=5,
                )
            ],
            default_value=9,
        )

        with pytest.raises(XtceDowngradeError):
            original.to_xsdata(XtceVersion.V1_2, DowngradePolicy.STRICT)

        raw_obj = original.to_xsdata(XtceVersion.V1_2, DowngradePolicy.IGNORE)

        assert isinstance(raw_obj, xtce_1_2.DiscreteLookupListType)
        assert [lookup.value for lookup in raw_obj.discrete_lookup] == [5]

    def test_discrete_lookup_list_round_trip_v1_3(self) -> None:
        """Round-trip DiscreteLookupList through XTCE v1.3."""
        original = xtce.DiscreteLookupList(
            lookups=[
                xtce.DiscreteLookup(
                    criteria=xtce.Comparison(
                        ref=XtcePath("/TestSystem/ParameterA"),
                        instance=0,
                        use_calibrated_value=True,
                        comparison_operator=xtce.ComparisonOperator.EQ,
                        value=1,
                    ),
                    value=5,
                )
            ],
            default_value=9,
        )

        round_tripped = xtce.DiscreteLookupList.from_xsdata(
            original.to_xsdata(XtceVersion.V1_3),
            XtceVersion.V1_3,
        )

        assert round_tripped == original

    def test_argument_match_criteria_round_trip(self) -> None:
        """Round-trip ArgumentMatchCriteria list, boolean, and algorithm cases."""
        list_criteria = xtce.ArgumentMatchCriteria(
            criteria=[
                _make_argument_comparison(1),
                xtce.ArgumentComparison(
                    instance_ref=_make_argument_instance_ref(),
                    comparison_operator=xtce.ComparisonOperator.GTE,
                    value=datetime.datetime(2024, 1, 2, 3, 4, 5),
                ),
            ]
        )
        boolean_criteria = xtce.ArgumentMatchCriteria(
            criteria=xtce.ArgumentBooleanExpression(
                comparison=xtce.ArgumentComparisonCheck(
                    left=_make_argument_instance_ref(),
                    comparison_operator=xtce.ComparisonOperator.GT,
                    right=2,
                )
            )
        )
        input_algorithm_criteria = xtce.ArgumentMatchCriteria(
            criteria=xtce.ArgumentInputAlgorithm(
                name="ArgumentInputAlgo",
                aliases=[xtce.Alias(namespace="Test", alias="ArgumentInputAlgo")],
                ancillary_data=[xtce.AncillaryData(name="meta", value="1")],
                inputs=[
                    xtce.InputParameterInstanceRef(
                        ref=XtcePath("/TestSystem/ParameterA"),
                        input_name="InputA",
                    ),
                    _make_argument_instance_ref(),
                ],
            )
        )

        for version in SUPPORTED_CONDITION_VERSIONS:
            for original in [list_criteria, boolean_criteria, input_algorithm_criteria]:
                round_tripped = xtce.ArgumentMatchCriteria.from_xsdata(
                    original.to_xsdata(version),
                    version,
                )

                assert round_tripped == original

    def test_argument_discrete_lookup_round_trip(self) -> None:
        """Round-trip ArgumentDiscreteLookup through supported versions."""
        original = xtce.ArgumentDiscreteLookup(
            criteria=xtce.ArgumentComparison(
                instance_ref=_make_argument_instance_ref(),
                comparison_operator=xtce.ComparisonOperator.EQ,
                value=1,
            ),
            value=7,
        )

        for version in SUPPORTED_CONDITION_VERSIONS:
            round_tripped = xtce.ArgumentDiscreteLookup.from_xsdata(
                original.to_xsdata(version),
                version,
            )

            assert round_tripped == original

    def test_argument_discrete_lookup_list_enforces_default_value_on_v1_2(self) -> None:
        """Verify v1.2 drops ArgumentDiscreteLookupList defaults under IGNORE."""
        original = xtce.ArgumentDiscreteLookupList(
            lookups=[
                xtce.ArgumentDiscreteLookup(
                    criteria=xtce.ArgumentComparison(
                        instance_ref=_make_argument_instance_ref(),
                        comparison_operator=xtce.ComparisonOperator.EQ,
                        value=1,
                    ),
                    value=5,
                )
            ],
            default_value=9,
        )

        with pytest.raises(XtceDowngradeError):
            original.to_xsdata(XtceVersion.V1_2, DowngradePolicy.STRICT)

        raw_obj = original.to_xsdata(XtceVersion.V1_2, DowngradePolicy.IGNORE)

        assert isinstance(raw_obj, xtce_1_2.ArgumentDiscreteLookupListType)
        assert [lookup.value for lookup in raw_obj.discrete_lookup] == [5]


class TestValidationCardinality:
    """Test explicit empty-list validation for grouped conditions."""

    @pytest.mark.parametrize(
        "model_cls",
        [
            xtce.AndedConditions,
            xtce.OredConditions,
            xtce.ArgumentAndedConditions,
            xtce.ArgumentOredConditions,
        ],
    )
    def test_empty_condition_lists_are_rejected(self, model_cls: type[object]) -> None:
        """Reject explicitly empty grouped-condition lists."""
        with pytest.raises(ValidationError):
            model_cls(conditions=[])  # type: ignore[call-arg]
