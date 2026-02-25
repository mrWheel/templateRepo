# Template Repo Applier

A small Python utility that applies a predefined GitHub template repository to an existing Git repository.

It copies files and directories **only if they do not already exist**, leaving existing project-specific files untouched.  
After copying, it automatically enables Git hooks from the template.

This is useful for enforcing shared tooling such as:
- Git hooks
- GitHub Actions workflows
- Formatting or linting configuration files

---

## Features

- ✅ Copies files and directories from a template repository
- ✅ Never overwrites existing files
- ✅ Works on existing Git repositories
- ✅ Automatically enables Git hooks
- ✅ Uses a shallow clone for speed
- ✅ No external Python dependencies

---

## What This Tool Does

1. Clones the template repository into a temporary directory
2. Copies selected files and folders into the target repository
3. Skips any file that already exists
4. Makes Git hooks executable (on POSIX systems)
5. Configures Git to use the template’s hooks directory
6. Ensures `createProjectStructure.py` is executable when present

---

## Template Repository

By default, this tool uses:

```bash
https://github.com/mrWheel/templateRepo
```

The template repository is expected to contain shared project assets such as:

- `.github/workflows/`
- `tools/git-hooks/`
- `.clang-format`
- `.codingRules.md`
- `createProjectStructure.py`

You can change the template repository URL or the copied paths via command-line arguments.

For `.github/workflows/tag-release.yml`, the workflow extracts only a semantic
version token in the form `vX.Y.Z` from `PROG_VERSION` in your source file.
Additional text around that token is allowed, as long as the `vX.Y.Z` part exists.

When `tag-release.yml` already exists in the target project and is overwritten by
the template version, these existing target values are preserved automatically:

- `PROGRAM_NAME`
- `PROGRAM_SRC`
- `PROGRAM_DIR`

---

## Requirements

- Python **3.8+**
- Git installed and available on your `PATH`
- A target project path must be provided as an argument

---

## Installation

No installation required.

Just copy the script into your repository (or anywhere you like):

```bash
applyTemplate.py
```

Make it executable (optional):

```bash
chmod +x applyTemplate.py
```

Run it by passing the target project root path:

```bash
./applyTemplate.py /path/to/your/project
```

If you run it without a path, it prints a help/usage message.

When a file already exists in the target directory and `--on-existing ask` is used,
the script prompts with:

- `O` = overwrite
- `K` = keep existing file
- `D` = show diff (then ask again)
- `Q` = quit the script immediately

Input is case-insensitive (`o/k/d/q` also works).

