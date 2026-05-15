"""Comprehensive unit tests for XtcePath."""

import os

import pytest

from xtce_lib import XtcePath


def test_init_normalizes_slashes_and_parts() -> None:
    """Initialization should normalize extra separators and preserve parts."""
    path = XtcePath("//ConkSat-1///BUS/")

    assert path.parts == ("ConkSat-1", "BUS")
    assert str(path) == "/ConkSat-1/BUS"


def test_init_preserves_relative_paths() -> None:
    """Initialization should preserve whether the input path is relative."""
    path = XtcePath("ConkSat-1/BUS")

    assert path.parts == ("ConkSat-1", "BUS")
    assert path.is_absolute() is False
    assert str(path) == "ConkSat-1/BUS"


def test_init_with_self() -> None:
    """Initialization with an XtcePath should return the same path."""
    original = XtcePath("/ConkSat-1/BUS")
    copy = XtcePath(original)

    assert copy is not original
    assert copy == original
    assert copy.is_absolute() is True


def test_joinpath_appends_child_segment() -> None:
    """Joinpath should append a child path segment."""
    base = XtcePath("/ConkSat-1/BUS")

    result = base.joinpath("COMMAND_ARGUMENT_Type")

    assert result.as_posix() == "/ConkSat-1/BUS/COMMAND_ARGUMENT_Type"


def test_relative_to_reports_expected_suffix() -> None:
    """relative_to should return the remaining suffix when base matches."""
    base = XtcePath("/ConkSat-1/BUS")
    child = XtcePath("/ConkSat-1/BUS/COMMAND_ARGUMENT_Type")

    assert child.relative_to(base) == XtcePath("COMMAND_ARGUMENT_Type")
    assert child.relative_to(base).is_absolute() is False


def test_name_returns_leaf_segment() -> None:
    """Name should return the last path segment."""
    assert XtcePath("/ConkSat-1/BUS/EPS").name == "EPS"


def test_root_path_properties() -> None:
    """Root path should expose expected root semantics."""
    root = XtcePath("/")

    assert root.parts == ()
    assert root.name == ""
    assert root.parent == XtcePath("/")
    assert root.parents == ()
    assert root.is_root is True
    assert root.is_absolute() is True


def test_relative_empty_path_properties() -> None:
    """An empty relative path should behave like the current directory."""
    path = XtcePath(".")

    assert path.parts == (".",)
    assert path.parent == XtcePath(".")
    assert path.is_absolute() is False


def test_parent_and_parents_for_nested_path() -> None:
    """Parent and parents should return immediate and ancestor paths."""
    path = XtcePath("/A/B/C")

    assert path.parent == XtcePath("/A/B")
    assert path.parents == (XtcePath("/A/B"), XtcePath("/A"), XtcePath("/"))


def test_parent_and_parents_for_relative_path() -> None:
    """Relative paths should preserve relative ancestors and current directory."""
    path = XtcePath("A/B/C")

    assert path.parent == XtcePath("A/B")
    assert path.parents == (XtcePath("A/B"), XtcePath("A"), XtcePath("."))


def test_is_root_for_single_component_path() -> None:
    """Single-component paths should be considered root-level."""
    assert XtcePath("/A").is_root is True


def test_joinpath_accepts_mixed_segment_types() -> None:
    """Joinpath should accept both strings and XtcePath instances."""
    base = XtcePath("/A")

    result = base.joinpath("B", XtcePath("/C/D"))

    assert result == XtcePath("/C/D")


def test_joinpath_keeps_relative_when_all_segments_are_relative() -> None:
    """Joinpath should keep a path relative when no absolute segment is introduced."""
    base = XtcePath("A")

    result = base.joinpath("B", XtcePath("C/D"))

    assert result == XtcePath("A/B/C/D")
    assert result.is_absolute() is False


def test_div_operator_delegates_to_joinpath() -> None:
    """The division operator should compose paths like joinpath."""
    base = XtcePath("/A/B")

    assert base / "C" == XtcePath("/A/B/C")


def test_with_name_replaces_only_leaf() -> None:
    """with_name should replace only the final segment."""
    path = XtcePath("/A/B/C")

    assert path.with_name("D") == XtcePath("/A/B/D")


def test_with_name_preserves_relative_paths() -> None:
    """with_name should preserve relative path semantics."""
    path = XtcePath("A/B/C")

    assert path.with_name("D") == XtcePath("A/B/D")


def test_with_name_raises_for_root_path() -> None:
    """with_name should fail for root paths that have no leaf segment."""
    with pytest.raises(ValueError, match="XtcePath has no name"):
        XtcePath("/").with_name("X")


def test_with_name_raises_for_invalid_segment() -> None:
    """with_name should reject invalid replacement segments."""
    with pytest.raises(ValueError, match="single non-empty"):
        XtcePath("/A/B").with_name("C/D")


def test_relative_to_raises_for_non_subpath() -> None:
    """relative_to should raise when base is not a true prefix."""
    with pytest.raises(ValueError, match="not in the subpath"):
        XtcePath("/A/B").relative_to("/X")


def test_relative_to_raises_for_mixed_absolute_and_relative_paths() -> None:
    """relative_to should reject comparisons across absolute and relative paths."""
    with pytest.raises(ValueError, match="not in the subpath"):
        XtcePath("/A/B").relative_to("A")


def test_is_relative_to_for_matching_and_non_matching_bases() -> None:
    """is_relative_to should return true only for prefix matches."""
    path = XtcePath("/A/B/C")

    assert path.is_relative_to("/A/B") is True
    assert path.is_relative_to("/Z") is False
    assert path.is_relative_to("A/B") is False


def test_is_absolute_reports_path_style() -> None:
    """is_absolute should distinguish absolute and relative XTCE paths."""
    assert XtcePath("/A/B").is_absolute() is True
    assert XtcePath("A/B").is_absolute() is False


def test_equality_supports_strings_and_paths() -> None:
    """Equality should support comparing XtcePath with strings and paths."""
    path = XtcePath("/A/B")

    assert path == XtcePath("/A/B")
    assert path == "/A/B"
    assert path != "A/B"
    assert (path == 42) is False


def test_hash_is_stable_for_equal_paths() -> None:
    """Equal paths should produce the same hash value."""
    assert hash(XtcePath("/A/B")) == hash(XtcePath("/A/B"))


def test_repr_and_fspath_are_informative() -> None:
    """Repr and os.fspath should return expected string forms."""
    path = XtcePath("/A/B")

    assert repr(path) == "XtcePath('/A/B')"
    assert os.fspath(path) == "/A/B"
