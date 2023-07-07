"""Abbreviated the annotations generated by sphinx-autodoc.

It's not necessary to generate the full path of type hints, because they are rendered as
clickable links.

See also https://github.com/sphinx-doc/sphinx/issues/5868.
"""
# pyright: reportMissingImports=false

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from sphinx.addnodes import pending_xref
    from sphinx.environment import BuildEnvironment


__TARGET_SUBSTITUTIONS = {
    "a set-like object providing a view on D's items": "typing.ItemsView",
    "a set-like object providing a view on D's keys": "typing.KeysView",
    "an object providing a view on D's values": "typing.ValuesView",
    "typing_extensions.Protocol": "typing.Protocol",
}
__REF_TYPE_SUBSTITUTIONS = {
    "None": "obj",
}


def _new_type_to_xref(
    target: str,
    env: "BuildEnvironment" = None,  # type: ignore[assignment]
    suppress_prefix: bool = False,
) -> "pending_xref":
    if env:
        kwargs = {
            "py:module": env.ref_context.get("py:module"),
            "py:class": env.ref_context.get("py:class"),
        }
    else:
        kwargs = {}

    target = __TARGET_SUBSTITUTIONS.get(target, target)
    reftype = __REF_TYPE_SUBSTITUTIONS.get(target, "class")
    if suppress_prefix:
        short_text = target.split(".")[-1]
    else:
        short_text = target

    from docutils.nodes import Text
    from sphinx.addnodes import pending_xref

    return pending_xref(
        "",
        Text(short_text),
        refdomain="py",
        reftype=reftype,
        reftarget=target,
        **kwargs,
    )


def relink_references() -> None:
    import sphinx.domains.python

    sphinx.domains.python.type_to_xref = _new_type_to_xref  # type: ignore[assignment]
