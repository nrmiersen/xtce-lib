class TestClass:
    @classmethod
    def _from_v1_1(cls: type[Self], dimension: xtce_1_1.DimensionType) -> Self:
        version = XtceVersion.V1_1

    @classmethod
    def _from_v1_2(cls: type[Self], dimension: xtce_1_2.DimensionType) -> Self:
        version = XtceVersion.V1_2

    @classmethod
    def _from_v1_3(cls: type[Self], dimension: xtce_1_3.DimensionType) -> Self:
        version = XtceVersion.V1_3

    @classmethod
    def from_xsdata(cls: type[Self], raw_obj: Any, version: XtceVersion) -> Self:
        """Factory method to create a Dimension from an xsdata-generated Dimension
        object of any version.
        """
        match version:
            case XtceVersion.V1_1:
                return cls._from_v1_1(raw_obj)
            case XtceVersion.V1_2:
                return cls._from_v1_2(raw_obj)
            case XtceVersion.V1_3:
                return cls._from_v1_3(raw_obj)
            case _:
                assert_never(version)

    def _to_v1_1(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_1.DimensionType:
        version = XtceVersion.V1_1

    def _to_v1_2(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_2.DimensionType:
        version = XtceVersion.V1_2

    def _to_v1_3(
        self, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_3.DimensionType:
        version = XtceVersion.V1_3

    def to_xsdata(
        self, version: XtceVersion, policy: DowngradePolicy = DowngradePolicy.STRICT
    ) -> xtce_1_2.DimensionType | xtce_1_3.DimensionType:
        """Convert this Dimension to an xsdata-generated Dimension object of the
        specified version.
        """
        match version:
            case XtceVersion.V1_1:
                return self._to_v1_1(policy)
            case XtceVersion.V1_2:
                return self._to_v1_2(policy)
            case XtceVersion.V1_3:
                return self._to_v1_3(policy)
            case _:
                assert_never(version)
