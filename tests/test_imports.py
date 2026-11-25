"""Smoke test: the package layout imports from a clean environment."""


def test_src_packages_import():
    import src.data  # noqa: F401
    import src.evaluation  # noqa: F401
    import src.models  # noqa: F401
    import src.training  # noqa: F401
    import src.utils  # noqa: F401
