# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2025 Felix Fontein <felix@fontein.de>

# /// script
# dependencies = ["nox>=2025.02.09", "antsibull-nox"]
# ///

import sys

import nox

try:
    import antsibull_nox
    from antsibull_nox.cli import run as run_antsibull_nox
except ImportError:
    print("You need to install antsibull-nox in the same Python environment as nox.")
    sys.exit(1)


antsibull_nox.load_antsibull_nox_toml()


@nox.session(name="update-azp-config", python=False)
def update_azp_config(session: nox.Session) -> None:
    command = [
        "antsibull-nox",
        "update-azp-config",
        "--exclude-tags",
        "docker",
        "--min-ansible-core",
        "2.18",
    ]
    if antsibull_nox.IN_CI:
        command.append("--fail-on-change")
    session.debug(" ".join(command))
    result = run_antsibull_nox(command)
    if result != 0:
        session.error(f"Execution failed with status code {result}")


# Allow to run the noxfile with `python noxfile.py`, `pipx run noxfile.py`, or similar.
# Requires nox >= 2025.02.09
if __name__ == "__main__":
    nox.main()
