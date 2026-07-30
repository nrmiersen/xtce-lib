"""Temporary template for building models."""

from typing import Any

from xtce_lib.exceptions import DowngradePolicy


class TemplateClass:
    """Template class."""

    _v1_1_type = None
    _v1_2_type = None
    _v1_3_type = None

    @classmethod
    def _from_v1_1_kwargs(cls, obj: type) -> dict[str, Any]:
        kwargs = super()._from_v1_1_kwargs(obj)
        kwargs["name"] = obj.name
        return kwargs

    @classmethod
    def _from_v1_2_kwargs(cls, obj: type) -> dict[str, Any]:
        kwargs = super()._from_v1_2_kwargs(obj)
        kwargs["name"] = obj.name
        return kwargs

    @classmethod
    def _from_v1_3_kwargs(cls, obj: type) -> dict[str, Any]:
        kwargs = super()._from_v1_3_kwargs(obj)
        kwargs["name"] = obj.name
        return kwargs

    def _to_v1_1_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_1_kwargs(policy)
        kwargs["name"] = self.name
        return kwargs

    def _to_v1_2_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_2_kwargs(policy)
        kwargs["name"] = self.name
        return kwargs

    def _to_v1_3_kwargs(self, policy: DowngradePolicy) -> dict[str, Any]:
        kwargs = super()._to_v1_3_kwargs(policy)
        kwargs["name"] = self.name
        return kwargs
