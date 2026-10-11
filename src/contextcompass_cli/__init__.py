"""Context Compass - durable, file-backed execution state for coding agents.

This module is the INSTALLER and CLI. It is deliberately NOT named
`contextcompass`, even though that is the distribution name, because the payload
directory in this repository is `src/contextcompass/` and two things claiming one
import name resolve differently depending on how Python was invoked. Keeping the
module name distinct means no collision is possible.

Three names are in play here and they are not interchangeable:

    contextcompass         the DISTRIBUTION on PyPI, and the repository
    contextcompass_cli     this MODULE - what `import` sees
    context_compass        the DIRECTORY, both in `src/` and in a consuming repo

The last one keeps its underscore. 119 shipped documents cite paths like
`context_compass/tools/...` - 546 mentions - plus a config filename and two
tool filenames carrying the same name. Renaming it is a migration, not a
rename, and it buys nothing now that this module is named distinctly.

`src/` mirrors the install deliberately: what you see there is what lands in a
repository, with no translation step. The one thing that must NOT match either
is this module's name, because a module sharing a name with a directory in the
user's repo resolves differently depending on how Python was invoked.

The payload ships inside this module as `_package/`.
"""

from __future__ import annotations

import pathlib

# Single source of truth for the version. `MANIFEST.md` inside the payload
# records the same number, and a test asserts they agree - a version maintained
# in two places is a version that will disagree, which is the whole reason the
# manifest is derived rather than declared.
__version__ = "2.17.0"

# What `init` creates in the user's repository. Distinct from both the source
# directory and the module name; see the docstring above.
INSTALL_DIRNAME = "context_compass"

# Where the payload lives in THIS repository's source tree. Deliberately the
# same as INSTALL_DIRNAME: what you see in `src/` is what lands in a repo, with
# no translation step to hold in your head.
SOURCE_DIRNAME = "context_compass"

_HERE = pathlib.Path(__file__).resolve().parent


def _find_payload() -> pathlib.Path:
    """Where the shipped package files live, installed or in a source checkout.

    In a wheel the build maps `src/contextcompass/` to `_package/` beside this
    module. In a source tree that directory does not exist and the payload is
    the sibling `src/contextcompass/`. Without this fallback the CLI works only
    after a build, so every source-run and every test would exercise a different
    code path from the one users get.

    The older layout put the payload at `src/context_compass/`. That is still
    accepted, because a checkout mid-rename should not fail obscurely.
    """
    installed = _HERE / "_package"
    if (installed / "AGENTS.MD").is_file():
        return installed
    for sibling in (SOURCE_DIRNAME, INSTALL_DIRNAME):
        checkout = _HERE.parent / sibling
        if (checkout / "AGENTS.MD").is_file():
            return checkout
    return installed          # report the installed path in the error message


PAYLOAD = _find_payload()

__all__ = ["__version__", "PAYLOAD", "INSTALL_DIRNAME", "SOURCE_DIRNAME"]
