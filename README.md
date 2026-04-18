# tecto

Prebuilt [Tectonic](https://tectonic-typesetting.github.io/) binary wheels for
pip and uv.

One-off run (no install):

```sh
uvx tecto mydoc.tex        # compiles to mydoc.pdf
uvx tecto --help
```

Install globally with `uv` — adds both `tecto` and `tectonic` to your PATH:

```sh
uv tool install tecto
tectonic mydoc.tex         # or: tecto mydoc.tex
```

Or via pip into an environment:

```sh
pip install tecto
tectonic mydoc.tex
```

For multi-document projects with a `Tectonic.toml` manifest, use V2 mode:
`uvx tecto -X new myproj`, then `uvx tecto -X build`. See the
[upstream docs](https://tectonic-typesetting.github.io/book/latest/) for
details.

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
