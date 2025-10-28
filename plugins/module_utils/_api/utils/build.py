# This code is part of the Ansible collection community.docker, but is an independent component.
# This particular file, and this file only, is based on the Docker SDK for Python (https://github.com/docker/docker-py/)
#
# Copyright (c) 2016-2022 Docker, Inc.
#
# It is licensed under the Apache 2.0 license (see LICENSES/Apache-2.0.txt in this collection)
# SPDX-License-Identifier: Apache-2.0

# Note that this module util is **PRIVATE** to the collection. It can have breaking changes at any time.
# Do not use this from other collections or standalone plugins/modules!

from __future__ import annotations

import io
import os
import random
import re
import tarfile
import tempfile
import typing as t

from ..constants import IS_WINDOWS_PLATFORM, WINDOWS_LONGPATH_PREFIX
from . import fnmatch


if t.TYPE_CHECKING:
    from collections.abc import Sequence


_SEP = re.compile("/|\\\\") if IS_WINDOWS_PLATFORM else re.compile("/")


def tar(
    path: str,
    exclude: list[str] | None = None,
    dockerfile: tuple[str, str | None] | tuple[None, None] | None = None,
    fileobj: t.IO[bytes] | None = None,
    gzip: bool = False,
) -> t.IO[bytes]:
    root = os.path.abspath(path)
    exclude = exclude or []
    dockerfile = dockerfile or (None, None)
    extra_files: list[tuple[str, str]] = []
    if dockerfile[1] is not None:
        assert dockerfile[0] is not None
        dockerignore_contents = "\n".join(
            (exclude or [".dockerignore"]) + [dockerfile[0]]
        )
        extra_files = [
            (".dockerignore", dockerignore_contents),
            dockerfile,  # type: ignore
        ]
    return create_archive(
        files=sorted(exclude_paths(root, exclude, dockerfile=dockerfile[0])),
        root=root,
        fileobj=fileobj,
        gzip=gzip,
        extra_files=extra_files,
    )


def exclude_paths(
    root: str, patterns: list[str], dockerfile: str | None = None
) -> set[str]:
    """
    Given a root directory path and a list of .dockerignore patterns, return
    an iterator of all paths (both regular files and directories) in the root
    directory that do *not* match any of the patterns.

    All paths returned are relative to the root.
    """

    if dockerfile is None:
        dockerfile = "Dockerfile"

    patterns.append("!" + dockerfile)
    pm = PatternMatcher(patterns)
    return set(pm.walk(root))


def build_file_list(root: str) -> list[str]:
    files = []
    for dirname, dirnames, fnames in os.walk(root):
        for filename in fnames + dirnames:
            longpath = os.path.join(dirname, filename)
            files.append(longpath.replace(root, "", 1).lstrip("/"))

    return files


def create_archive(
    root: str,
    files: Sequence[str] | None = None,
    fileobj: t.IO[bytes] | None = None,
    gzip: bool = False,
    extra_files: Sequence[tuple[str, str]] | None = None,
) -> t.IO[bytes]:
    extra_files = extra_files or []
    if not fileobj:
        # pylint: disable-next=consider-using-with
        fileobj = tempfile.NamedTemporaryFile()  # noqa: SIM115

    with tarfile.open(mode="w:gz" if gzip else "w", fileobj=fileobj) as tarf:
        if files is None:
            files = build_file_list(root)
        extra_names = set(e[0] for e in extra_files)
        for path in files:
            if path in extra_names:
                # Extra files override context files with the same name
                continue
            full_path = os.path.join(root, path)

            i = tarf.gettarinfo(full_path, arcname=path)
            if i is None:
                # This happens when we encounter a socket file. We can safely
                # ignore it and proceed.
                continue  # type: ignore

            # Workaround https://bugs.python.org/issue32713
            if i.mtime < 0 or i.mtime > 8**11 - 1:
                i.mtime = int(i.mtime)

            if IS_WINDOWS_PLATFORM:
                # Windows does not keep track of the execute bit, so we make files
                # and directories executable by default.
                i.mode = i.mode & 0o755 | 0o111

            if i.isfile():
                try:
                    with open(full_path, "rb") as f:
                        tarf.addfile(i, f)
                except IOError as exc:
                    raise IOError(f"Can not read file in context: {full_path}") from exc
            else:
                # Directories, FIFOs, symlinks... do not need to be read.
                tarf.addfile(i, None)

        for name, contents in extra_files:
            info = tarfile.TarInfo(name)
            contents_encoded = contents.encode("utf-8")
            info.size = len(contents_encoded)
            tarf.addfile(info, io.BytesIO(contents_encoded))

    fileobj.seek(0)
    return fileobj


def mkbuildcontext(dockerfile: io.BytesIO | t.IO[bytes]) -> t.IO[bytes]:
    # pylint: disable-next=consider-using-with
    f = tempfile.NamedTemporaryFile()  # noqa: SIM115
    try:
        with tarfile.open(mode="w", fileobj=f) as tarf:
            if isinstance(dockerfile, io.StringIO):  # type: ignore
                raise TypeError("Please use io.BytesIO to create in-memory Dockerfiles")
            if isinstance(dockerfile, io.BytesIO):
                dfinfo = tarfile.TarInfo("Dockerfile")
                dfinfo.size = len(dockerfile.getvalue())
                dockerfile.seek(0)
            else:
                dfinfo = tarf.gettarinfo(fileobj=dockerfile, arcname="Dockerfile")
            tarf.addfile(dfinfo, dockerfile)
        f.seek(0)
    except Exception:  # noqa: E722
        f.close()
        raise
    return f


def split_path(p: str) -> list[str]:
    return [pt for pt in re.split(_SEP, p) if pt and pt != "."]


def normalize_slashes(p: str) -> str:
    if IS_WINDOWS_PLATFORM:
        return "/".join(split_path(p))
    return p


def walk(root: str, patterns: Sequence[str], default: bool = True) -> t.Generator[str]:
    pm = PatternMatcher(patterns)
    return pm.walk(root)


# Heavily based on
# https://github.com/moby/moby/blob/master/pkg/fileutils/fileutils.go
class PatternMatcher:
    def __init__(self, patterns: Sequence[str]) -> None:
        self.patterns = list(filter(lambda p: p.dirs, [Pattern(p) for p in patterns]))
        self.patterns.append(Pattern("!.dockerignore"))

    def matches(self, filepath: str) -> bool:
        matched = False
        parent_path = os.path.dirname(filepath)
        parent_path_dirs = split_path(parent_path)

        for pattern in self.patterns:
            negative = pattern.exclusion
            match = pattern.match(filepath)
            if (
                not match
                and parent_path != ""
                and len(pattern.dirs) <= len(parent_path_dirs)
            ):
                match = pattern.match(
                    os.path.sep.join(parent_path_dirs[: len(pattern.dirs)])
                )

            if match:
                matched = not negative

        return matched

    def walk(self, root: str) -> t.Generator[str]:
        def rec_walk(current_dir: str) -> t.Generator[str]:
            for f in os.listdir(current_dir):
                fpath = os.path.join(os.path.relpath(current_dir, root), f)
                if fpath.startswith("." + os.path.sep):
                    fpath = fpath[2:]
                match = self.matches(fpath)
                if not match:
                    yield fpath

                cur = os.path.join(root, fpath)
                if not os.path.isdir(cur) or os.path.islink(cur):
                    continue

                if match:
                    # If we want to skip this file and it is a directory
                    # then we should first check to see if there's an
                    # excludes pattern (e.g. !dir/file) that starts with this
                    # dir. If so then we cannot skip this dir.
                    skip = True

                    for pat in self.patterns:
                        if not pat.exclusion:
                            continue
                        if pat.cleaned_pattern.startswith(normalize_slashes(fpath)):
                            skip = False
                            break
                    if skip:
                        continue
                yield from rec_walk(cur)

        return rec_walk(root)


class Pattern:
    def __init__(self, pattern_str: str) -> None:
        self.exclusion = False
        if pattern_str.startswith("!"):
            self.exclusion = True
            pattern_str = pattern_str[1:]

        self.dirs = self.normalize(pattern_str)
        self.cleaned_pattern = "/".join(self.dirs)

    @classmethod
    def normalize(cls, p: str) -> list[str]:
        # Remove trailing spaces
        p = p.strip()

        # Leading and trailing slashes are not relevant. Yes,
        # "foo.py/" must exclude the "foo.py" regular file. "."
        # components are not relevant either, even if the whole
        # pattern is only ".", as the Docker reference states: "For
        # historical reasons, the pattern . is ignored."
        # ".." component must be cleared with the potential previous
        # component, regardless of whether it exists: "A preprocessing
        # step [...]  eliminates . and .. elements using Go's
        # filepath.".
        i = 0
        split = split_path(p)
        while i < len(split):
            if split[i] == "..":
                del split[i]
                if i > 0:
                    del split[i - 1]
                    i -= 1
            else:
                i += 1
        return split

    def match(self, filepath: str) -> bool:
        return fnmatch.fnmatch(normalize_slashes(filepath), self.cleaned_pattern)


def process_dockerfile(
    dockerfile: str | None, path: str
) -> tuple[str, str | None] | tuple[None, None]:
    if not dockerfile:
        return (None, None)

    abs_dockerfile = dockerfile
    if not os.path.isabs(dockerfile):
        abs_dockerfile = os.path.join(path, dockerfile)
        if IS_WINDOWS_PLATFORM and path.startswith(WINDOWS_LONGPATH_PREFIX):
            abs_dockerfile = f"{WINDOWS_LONGPATH_PREFIX}{os.path.normpath(abs_dockerfile[len(WINDOWS_LONGPATH_PREFIX) :])}"
    if os.path.splitdrive(path)[0] != os.path.splitdrive(abs_dockerfile)[
        0
    ] or os.path.relpath(abs_dockerfile, path).startswith(".."):
        # Dockerfile not in context - read data to insert into tar later
        with open(abs_dockerfile, "rt", encoding="utf-8") as df:
            return (f".dockerfile.{random.getrandbits(160):x}", df.read())

    # Dockerfile is inside the context - return path relative to context root
    if dockerfile == abs_dockerfile:
        # Only calculate relpath if necessary to avoid errors
        # on Windows client -> Linux Docker
        # see https://github.com/docker/compose/issues/5969
        dockerfile = os.path.relpath(abs_dockerfile, path)
    return (dockerfile, None)
