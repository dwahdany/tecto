# tecto

Prebuilt [Tectonic](https://tectonic-typesetting.github.io/) binary wheels for
pip and uv.

```sh
uvx tecto --help
uvx tecto -X compile mydoc.tex
```

Or install into an environment:

```sh
pip install tecto
tectonic -X compile mydoc.tex   # or: tecto -X compile mydoc.tex
```

## What this is

`tecto` repackages the official upstream `tectonic` release binaries from
<https://github.com/tectonic-typesetting/tectonic/releases> into
platform-tagged Python wheels. There is no Python code — the wheel ships the
native `tectonic` executable directly and `pip` drops it on your `PATH`.

Two commands are installed, both identical: `tectonic` (matches upstream so
existing scripts and docs work) and `tecto` (matches the package name so
`uvx tecto` works without `--from`).

Versions track upstream tectonic versions exactly.

## Supported platforms

- macOS: arm64 (Apple Silicon), x86_64
- Linux: x86_64 (glibc + musl), aarch64 (musl)
- Windows: x86_64

Other platforms listed in the upstream release (32-bit, armv7) are not
currently published; open an issue if you need one.

## Relationship to upstream

This is an unofficial packaging project. Bug reports about `tectonic` itself
belong upstream: <https://github.com/tectonic-typesetting/tectonic/issues>.
Bug reports about packaging, release automation, or missing platforms belong
in this repository.
