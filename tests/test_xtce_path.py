"""Comprehensive unit tests for XtcePath."""

import os

import pytest
from pydantic import BaseModel, ValidationError

from xtce_lib import XtcePath
from xtce_lib.common.xtce_path import PathNode


def _parts_as_raw(path: XtcePath) -> tuple[str, ...]:
    """Return the raw string form of each path component."""
    return tuple(str(part) for part in path.parts)


def _node(
    raw: str, base: str, indices: tuple[int, ...] = (), member: PathNode | None = None
) -> PathNode:
    """Build a PathNode fixture with the given shape."""
    return PathNode(raw=raw, base=base, indices=indices, member=member)


class TestPathNode:
    """Unit tests for the PathNode class."""

    @pytest.mark.parametrize(
        "raw_segment, expected",
        [
            ("BUS", _node("BUS", "BUS")),
            ("BUS[0]", _node("BUS[0]", "BUS", (0,))),
            ("BUS[0][12]", _node("BUS[0][12]", "BUS", (0, 12))),
            (
                "BUS[0].FIELD[2].VALUE",
                _node(
                    "BUS[0].FIELD[2].VALUE",
                    "BUS",
                    (0,),
                    _node(
                        "FIELD[2].VALUE",
                        "FIELD",
                        (2,),
                        _node("VALUE", "VALUE"),
                    ),
                ),
            ),
            (".", _node(".", ".")),
            ("..", _node("..", "..")),
            ("BUS[abc]", _node("BUS[abc]", "BUS[abc]")),
            ("BUS.", _node("BUS.", "BUS.")),
        ],
    )
    def test_from_string_parses_supported_forms(
        self,
        raw_segment: str,
        expected: PathNode,
    ) -> None:
        """PathNode should parse plain, indexed, aggregate, and fallback forms."""
        node = PathNode.from_string(raw_segment)

        assert node == expected
        assert str(node) == raw_segment

    def test_properties_for_leaf_and_array_nodes(self) -> None:
        """PathNode flags should distinguish plain nodes from array nodes."""
        plain = PathNode.from_string("BUS")
        array_node = PathNode.from_string("BUS[1][2]")

        assert plain.is_array is False
        assert plain.is_aggregate is False
        assert plain.contains_array is False
        assert plain.contains_aggregate is False

        assert array_node.is_array is True
        assert array_node.is_aggregate is False
        assert array_node.contains_array is True
        assert array_node.contains_aggregate is False

    def test_properties_for_nested_aggregate_nodes(self) -> None:
        """PathNode should report nested aggregate state across member chains."""
        node = PathNode.from_string("BUS[0].FIELD[2].VALUE")

        assert node.is_array is True
        assert node.is_aggregate is True
        assert node.contains_array is True
        assert node.contains_aggregate is True
        assert node.member is not None
        assert node.member.base == "FIELD"
        assert node.member.indices == (2,)
        assert node.member.member == PathNode.from_string("VALUE")

    def test_nested_members_remain_recursive(self) -> None:
        """Nested aggregate members should keep recursing through member chains."""
        node = PathNode.from_string("BUS.FIELD.SUBFIELD")

        assert node.member is not None
        assert node.member.member is not None
        assert node.member.member.base == "SUBFIELD"
        assert node.member.contains_aggregate is True
        assert node.member.contains_array is False

    def test_invalid_segments_fall_back_to_raw_values(self) -> None:
        """Invalid segment shapes should round-trip as raw PathNode values."""
        node = PathNode.from_string("BUS[1].")

        assert node == PathNode(raw="BUS[1].", base="BUS[1].")
        assert node.is_array is False
        assert node.is_aggregate is False


class TestXtcePath:
    """Unit tests for the XtcePath class."""

    def test_init_normalizes_slashes_and_parts(self) -> None:
        """Initialization should normalize extra separators and preserve parts."""
        path = XtcePath("//ConkSat-1///BUS/")

        assert _parts_as_raw(path) == ("ConkSat-1", "BUS")
        assert str(path) == "/ConkSat-1/BUS"

    def test_init_preserves_relative_paths(self) -> None:
        """Initialization should preserve whether the input path is relative."""
        path = XtcePath("ConkSat-1/BUS")

        assert _parts_as_raw(path) == ("ConkSat-1", "BUS")
        assert path.is_absolute() is False
        assert str(path) == "ConkSat-1/BUS"

    def test_init_with_self(self) -> None:
        """Initialization with an XtcePath should return the same path."""
        original = XtcePath("/ConkSat-1/BUS")
        copy = XtcePath(original)

        assert copy is not original
        assert copy == original
        assert copy.is_absolute() is True

    def test_joinpath_appends_child_segment(self) -> None:
        """Joinpath should append a child path segment."""
        base = XtcePath("/ConkSat-1/BUS")

        result = base.joinpath("COMMAND_ARGUMENT_Type")

        assert result == "/ConkSat-1/BUS/COMMAND_ARGUMENT_Type"

    def test_relative_to_reports_expected_suffix(self) -> None:
        """relative_to should return the remaining suffix when base matches."""
        base = XtcePath("/ConkSat-1/BUS")
        child = XtcePath("/ConkSat-1/BUS/COMMAND_ARGUMENT_Type")

        assert child.relative_to(base) == XtcePath("COMMAND_ARGUMENT_Type")
        assert child.relative_to(base).is_absolute() is False

    def test_name_returns_leaf_segment(self) -> None:
        """Name should return the last path segment."""
        assert XtcePath("/ConkSat-1/BUS/EPS").name == "EPS"

    def test_leaf_returns_final_pathnode(self) -> None:
        """Leaf should return the final PathNode component."""
        path = XtcePath("/ConkSat-1/BUS[0].TEMP")

        assert path.leaf == PathNode.from_string("BUS[0].TEMP")

    def test_leaf_returns_none_for_root_path(self) -> None:
        """Leaf should return None for root paths with no components."""
        assert XtcePath("/").leaf is None

    def test_root_path_properties(self) -> None:
        """Root path should expose expected root semantics."""
        root = XtcePath("/")

        assert root.parts == ()
        assert root.name == ""
        assert root.parent == XtcePath("/")
        assert root.parents == ()
        assert root.is_root is True
        assert root.is_absolute() is True

    def test_relative_empty_path_properties(self) -> None:
        """An empty relative path should behave like the current directory."""
        path = XtcePath(".")

        assert path.parts == (PathNode(raw=".", base="."),)
        assert path.parent == XtcePath(".")
        assert path.is_absolute() is False

    def test_parent_and_parents_for_nested_path(self) -> None:
        """Parent and parents should return immediate and ancestor paths."""
        path = XtcePath("/A/B/C")

        assert path.parent == XtcePath("/A/B")
        assert path.parents == (XtcePath("/A/B"), XtcePath("/A"), XtcePath("/"))

    def test_parent_and_parents_for_relative_path(self) -> None:
        """Relative paths should preserve relative ancestors and current directory."""
        path = XtcePath("A/B/C")

        assert path.parent == XtcePath("A/B")
        assert path.parents == (XtcePath("A/B"), XtcePath("A"), XtcePath("."))

    def test_is_root_for_single_component_path(self) -> None:
        """Single-component paths should be considered root-level."""
        assert XtcePath("/A").is_root is True

    def test_joinpath_accepts_mixed_segment_types(self) -> None:
        """Joinpath should accept both strings and XtcePath instances."""
        base = XtcePath("/A")

        result = base.joinpath("B", XtcePath("/C/D"))

        assert result == XtcePath("/C/D")

    def test_joinpath_keeps_relative_when_all_segments_are_relative(self) -> None:
        """Joinpath should keep a path relative when no absolute segment is introduced."""
        base = XtcePath("A")

        result = base.joinpath("B", XtcePath("C/D"))

        assert result == XtcePath("A/B/C/D")
        assert result.is_absolute() is False

    def test_div_operator_delegates_to_joinpath(self) -> None:
        """The division operator should compose paths like joinpath."""
        base = XtcePath("/A/B")

        assert base / "C" == XtcePath("/A/B/C")

    def test_with_name_replaces_only_leaf(self) -> None:
        """with_name should replace only the final segment."""
        path = XtcePath("/A/B/C")

        assert path.with_name("D") == XtcePath("/A/B/D")

    def test_with_name_preserves_relative_paths(self) -> None:
        """with_name should preserve relative path semantics."""
        path = XtcePath("A/B/C")

        assert path.with_name("D") == XtcePath("A/B/D")

    def test_with_name_raises_for_root_path(self) -> None:
        """with_name should fail for root paths that have no leaf segment."""
        with pytest.raises(ValueError, match="XtcePath has no name"):
            XtcePath("/").with_name("X")

    def test_with_name_raises_for_invalid_segment(self) -> None:
        """with_name should reject invalid replacement segments."""
        with pytest.raises(ValueError, match="single non-empty"):
            XtcePath("/A/B").with_name("C/D")

    def test_relative_to_raises_for_non_subpath(self) -> None:
        """relative_to should raise when base is not a true prefix."""
        with pytest.raises(ValueError, match="not in the subpath"):
            XtcePath("/A/B").relative_to("/X")

    def test_relative_to_raises_for_mixed_absolute_and_relative_paths(self) -> None:
        """relative_to should reject comparisons across absolute and relative paths."""
        with pytest.raises(ValueError, match="not in the subpath"):
            XtcePath("/A/B").relative_to("A")

    def test_is_relative_to_for_matching_and_non_matching_bases(self) -> None:
        """is_relative_to should return true only for prefix matches."""
        path = XtcePath("/A/B/C")

        assert path.is_relative_to("/A/B") is True
        assert path.is_relative_to("/Z") is False
        assert path.is_relative_to("A/B") is False

    def test_is_absolute_reports_path_style(self) -> None:
        """is_absolute should distinguish absolute and relative XTCE paths."""
        assert XtcePath("/A/B").is_absolute() is True
        assert XtcePath("A/B").is_absolute() is False

    def test_equality_supports_strings_and_paths(self) -> None:
        """Equality should support comparing XtcePath with strings and paths."""
        path = XtcePath("/A/B")

        assert path == XtcePath("/A/B")
        assert path == "/A/B"
        assert path != "A/B"
        assert (path == 42) is False

    def test_hash_is_stable_for_equal_paths(self) -> None:
        """Equal paths should produce the same hash value."""
        assert hash(XtcePath("/A/B")) == hash(XtcePath("/A/B"))

    def test_repr_and_fspath_are_informative(self) -> None:
        """Repr and os.fspath should return expected string forms."""
        path = XtcePath("/A/B")

        assert repr(path) == "XtcePath('/A/B')"
        assert os.fspath(path) == "/A/B"

    def test_pydantic_coerces_string_input(self) -> None:
        """Pydantic should coerce supported inputs into XtcePath."""

        class PathModel(BaseModel):
            path: XtcePath

        from_str = PathModel(path="/A/B")  # type: ignore

        assert isinstance(from_str.path, XtcePath)
        assert from_str.path == XtcePath("/A/B")

    def test_pydantic_accepts_dot_segments_in_qualified_paths(self) -> None:
        """Pydantic should accept './' and '../' path navigation segments."""

        class PathModel(BaseModel):
            path: XtcePath

        dot_path = PathModel(path="./A/B")  # type: ignore
        dotdot_path = PathModel(path="../A/B")  # type: ignore

        assert dot_path.path == XtcePath("./A/B")
        assert dotdot_path.path == XtcePath("../A/B")

    def test_pydantic_rejects_invalid_input_type(self) -> None:
        """Pydantic should reject unsupported input types for XtcePath."""

        class PathModel(BaseModel):
            path: XtcePath

        with pytest.raises(ValidationError):
            PathModel(path=123)  # type: ignore

    @pytest.mark.parametrize(
        "invalid_value",
        [
            "A/B/",
            "A:B",
            "A[0]/B",
            ".",
            "..",
        ],
    )
    def test_pydantic_rejects_invalid_name_reference_strings(
        self, invalid_value: str
    ) -> None:
        """Pydantic should reject strings that violate XTCE name-reference pattern."""

        class PathModel(BaseModel):
            path: XtcePath

        with pytest.raises(ValidationError, match="valid XTCE name reference path"):
            PathModel(path=invalid_value)  # type: ignore

    def test_pydantic_serialization_and_json_schema(self) -> None:
        """Pydantic should serialize XtcePath as a string and expose string schema."""

        class PathModel(BaseModel):
            path: XtcePath

        model = PathModel(path=XtcePath("/A/B"))

        assert model.model_dump() == {"path": "/A/B"}
        assert model.model_json_schema()["properties"]["path"]["type"] == "string"

    def test_normalize_removes_dot_segments(self) -> None:
        """Normalize should remove '.' segments from paths."""
        path = XtcePath("/A/./B")

        assert path.normalize() == XtcePath("/A/B")

    def test_normalize_collapses_parent_references(self) -> None:
        """Normalize should collapse '..' segments with previous components."""
        path = XtcePath("/A/B/../C")

        assert path.normalize() == XtcePath("/A/C")

    def test_normalize_handles_multiple_parent_references(self) -> None:
        """Normalize should handle multiple consecutive '..' segments."""
        path = XtcePath("/A/B/C/../../D")

        assert path.normalize() == XtcePath("/A/D")

    def test_normalize_parent_references_at_absolute_root(self) -> None:
        """Normalize should not traverse above the root for absolute paths."""
        path = XtcePath("/../A")

        assert path.normalize() == XtcePath("/A")

    def test_normalize_multiple_parents_at_absolute_root(self) -> None:
        """Normalize should handle multiple '..' at the root of absolute paths."""
        path = XtcePath("/../../A/B")

        assert path.normalize() == XtcePath("/A/B")

    def test_normalize_preserves_relative_paths_with_leading_parent_refs(self) -> None:
        """Normalize should preserve leading '..' in relative paths."""
        path = XtcePath("../A/B")

        assert path.normalize() == XtcePath("../A/B")

    def test_normalize_collapses_in_relative_paths(self) -> None:
        """Normalize should collapse '..' in relative paths when possible."""
        path = XtcePath("A/B/../C")

        assert path.normalize() == XtcePath("A/C")

    def test_normalize_mixed_dot_and_parent_references(self) -> None:
        """Normalize should handle mixed '.' and '..' segments."""
        path = XtcePath("/A/./B/../C/./D")

        assert path.normalize() == XtcePath("/A/C/D")

    def test_normalize_returns_equivalent_for_normalized_path(self) -> None:
        """Normalize should return equivalent path for already-normalized paths."""
        path = XtcePath("/A/B/C")

        assert path.normalize() == path

    def test_normalize_dot_directory_to_dot(self) -> None:
        """Normalize of '.' should return '.' ."""
        path = XtcePath(".")

        assert path.normalize() == XtcePath(".")

    def test_normalize_parent_directory_to_parent(self) -> None:
        """Normalize of '..' should return '..'."""
        path = XtcePath("..")

        assert path.normalize() == XtcePath("..")

    def test_normalize_root_to_root(self) -> None:
        """Normalize of '/' should return '/'."""
        path = XtcePath("/")

        assert path.normalize() == XtcePath("/")

    def test_normalize_complex_relative_with_mixed_segments(self) -> None:
        """Normalize should handle complex relative paths with mixed segments."""
        path = XtcePath("A/./B/../C/../../D/../E")

        assert path.normalize() == XtcePath("../E")
