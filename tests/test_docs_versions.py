"""Tests for the XTCE version badges in the API reference."""

import shutil
import subprocess
import sys
from abc import ABC
from enum import Enum
from pathlib import Path

import pytest
from lxml import html

from xtce_lib import xtce

griffe = pytest.importorskip("griffe")
jinja2 = pytest.importorskip("jinja2")

ROOT = Path(__file__).resolve().parents[1]
VERSIONS = ("1.1", "1.2", "1.3")


def test_model_version_badges_match_conversion_targets() -> None:
    """Render badges from static Griffe data and compare them with model targets."""
    package = griffe.load("xtce_lib", search_paths=[str(ROOT / "src")])
    model_module = package["xtce"]
    environment = jinja2.Environment(
        loader=jinja2.ChoiceLoader(
            [
                jinja2.FileSystemLoader(
                    ROOT / "overrides/mkdocstrings/python/material"
                ),
                jinja2.DictLoader(
                    {
                        "_base/class.html.jinja": "{% block labels scoped %}{% endblock %}"
                    }
                ),
            ]
        ),
        autoescape=True,
    )
    template = environment.get_template("class.html.jinja")

    for name in xtce.__all__:
        model = getattr(xtce, name)
        if not isinstance(model, type) or not issubclass(model, xtce.XtceBaseModel):
            continue

        griffe_class = model_module[name]
        rendered = template.render(
            **{"class": griffe_class, "all_members": griffe_class.all_members}
        )
        fragment = html.fragment_fromstring(rendered, create_parent=True)
        badges = fragment.xpath('.//span[contains(@class, "xtce-version-badge ")]')
        labels = [
            badge.xpath('./span[@class="xtce-version-label"]/text()')[0]
            for badge in badges
        ]
        assert labels == list(VERSIONS), name
        for version, badge in zip(VERSIONS, badges, strict=True):
            supported = (
                getattr(model, f"_v{version.replace('.', '_')}_type") is not None
            )
            status = "supported" if supported else "unsupported"
            assert f"xtce-version-badge--{status}" in badge.get("class", ""), name
            assert badge.get("tabindex") == "0"
            assert badge.xpath('.//autoref[@identifier="xtce-version-compatibility"]')
            if not supported:
                assert "raises XtceUnsupportedError" in badge.text_content()


def test_api_member_details_include_types_without_summary_tables(
    tmp_path: Path,
) -> None:
    """Build the reference and check detailed model members and class navigation."""
    pytest.importorskip("zensical")
    for name in ("docs", "overrides", "src"):
        shutil.copytree(ROOT / name, tmp_path / name)
    (tmp_path / "zensical.toml").write_text((ROOT / "zensical.toml").read_text())
    subprocess.run(
        [sys.executable, "-m", "zensical", "build"],
        cwd=tmp_path,
        check=True,
    )

    page = html.parse(str(tmp_path / "site/api/xtce/commands/index.html"))
    model = page.xpath('//*[@id="xtce_lib.xtce.IntegerArgument"]/parent::div')[0]
    summaries = model.xpath('.//span[@class="doc-section-title"]/text()')
    assert "Methods:" not in summaries
    assert "Attributes:" not in summaries
    assert not page.xpath('//table//a[normalize-space()="IntegerArgument"]')

    children = model.xpath(
        './div[contains(@class, "doc-contents")]/div[@class="doc doc-children"]'
        '/div[contains(@class, "doc-object")]'
    )
    attribute_positions = [
        index
        for index, child in enumerate(children)
        if "doc-attribute" in child.get("class", "")
    ]
    method_positions = [
        index
        for index, child in enumerate(children)
        if "doc-function" in child.get("class", "")
    ]
    assert attribute_positions and method_positions
    assert max(attribute_positions) < min(method_positions)

    for name, expected in (
        ("size_in_bits", "Literal[-1] | int = 32"),
        ("signed", "bool = True"),
        ("valid_ranges", "ValidIntegerRanges | None = None"),
        ("from_xsdata", "version: XtceVersion) -> Self"),
    ):
        member = model.xpath(f'.//*[@id="xtce_lib.xtce.IntegerArgument.{name}"]/..')[0]
        signature = member.xpath('./div[contains(@class, "doc-signature")]')[0]
        assert expected in signature.text_content()
        assert member.xpath('./div[contains(@class, "doc-contents")]//p')

    size_field = model.xpath(
        './/*[@id="xtce_lib.xtce.IntegerArgument.size_in_bits"]/..'
    )[0]
    assert "Constraint (int): >= 1" in " ".join(size_field.text_content().split())
    assert (
        "xtce-version-badge--supported"
        in model.getchildren()[0].xpath(
            './/span[contains(@class, "xtce-version-badge")]/@class'
        )[0]
    )

    ref_field = page.xpath(
        '//*[@id="xtce_lib.xtce.MetaCommandStep.meta_command_ref"]/..'
    )[0]
    ref_text = " ".join(ref_field.text_content().split())
    assert "Required" in ref_text
    assert "Examples: 'TODO'" in ref_text
    assert "Schema metadata" in ref_text
    assert (
        "Field("
        not in ref_field.xpath('./div[contains(@class, "doc-signature")]')[
            0
        ].text_content()
    )

    assignments = page.xpath(
        '//*[@id="xtce_lib.xtce.MetaCommandStep.argument_assignments"]/..'
    )[0]
    assert "Default factory: list" in " ".join(assignments.text_content().split())

    dimensions = page.xpath('//*[@id="xtce_lib.xtce.ArrayArgument.dimensions"]/..')[0]
    dimensions_text = " ".join(dimensions.text_content().split())
    assert "Minimum length: 1" in dimensions_text
    assert "Factory defaults may not be validated" in dimensions_text

    data_types = html.parse(str(tmp_path / "site/api/xtce/data-types/index.html"))
    symbol = data_types.xpath('//*[@id="xtce_lib.xtce.Unit.symbol"]/..')[0]
    assert "Examples: 'm/s^2', 'V', 'byte'" in " ".join(symbol.text_content().split())

    encodings = html.parse(str(tmp_path / "site/api/xtce/encodings/index.html"))
    leading_size = encodings.xpath(
        '//*[@id="xtce_lib.xtce.LeadingSize.size_in_bits"]/..'
    )[0]
    assert "Minimum: 1" in " ".join(leading_size.text_content().split())

    enum_page_path = tmp_path / "site/api/xtce/enums/index.html"
    enum_page = html.parse(str(enum_page_path))
    enum_names = {
        name
        for name in xtce.__all__
        if isinstance(getattr(xtce, name), type)
        and issubclass(getattr(xtce, name), Enum)
    }
    enum_ids = {f"xtce_lib.xtce.{name}" for name in enum_names}
    headings = enum_page.xpath('//h2[@class="doc doc-heading"]/@id')
    assert set(headings) == enum_ids
    assert len(headings) == len(enum_ids)
    assert enum_page.xpath('//*[@id="xtce_lib.xtce.ConsequenceLevel.NORMAL"]')
    assert not enum_page.xpath(
        '//span[@class="doc-section-title" and text()="Attributes:"]'
    )
    basis = enum_page.xpath('//*[@id="xtce_lib.xtce.Basis"]/..')[0]
    per_second = basis.xpath('.//*[@id="xtce_lib.xtce.Basis.PER_SECOND"]/..')[0]
    assert "The rate is measured per second." in per_second.text_content()
    system_type = enum_page.xpath('//*[@id="xtce_lib.xtce.SystemType"]/..')[0]
    asset = system_type.xpath('.//*[@id="xtce_lib.xtce.SystemType.ASSET"]/..')[0]
    assert "An form of asset monitored" in asset.text_content()

    base_ids = {
        f"xtce_lib.xtce.{name}"
        for name in xtce.__all__
        if isinstance(getattr(xtce, name), type)
        and ABC in getattr(xtce, name).__bases__
    }
    for api_page_path in (tmp_path / "site/api/xtce").rglob("index.html"):
        api_page = html.parse(str(api_page_path))
        headings = api_page.xpath('//h2[@class="doc doc-heading"]/@id')
        assert not base_ids.intersection(headings)
        if api_page_path == enum_page_path:
            continue
        assert not enum_ids.intersection(headings)

    assert page.xpath('//a[@href="../enums/#xtce_lib.xtce.ConsequenceLevel"]')
    assert encodings.xpath('//a[@href="../enums/#xtce_lib.xtce.IntegerEncoding"]')
    assert page.xpath('//*[@id="xtce_lib.xtce.IntegerArgument"]')
    argument_data = html.parse(str(tmp_path / "site/api/xtce/argument-data/index.html"))
    assert not argument_data.xpath('//*[@id="xtce_lib.xtce.ArgumentIntegerData"]')
    assert argument_data.xpath('//*[@id="xtce_lib.xtce.ArgumentBinaryData"]')
    assert not data_types.xpath('//*[@id="xtce_lib.xtce.IntegerData"]')
    parameters = html.parse(str(tmp_path / "site/api/xtce/parameters/index.html"))
    assert parameters.xpath('//*[@id="xtce_lib.xtce.IntegerParameter.size_in_bits"]')
