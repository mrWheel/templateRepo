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

You can change the template repository URL or the copied paths via command-line arguments.

---

## Requirements

- Python **3.8+**
- Git installed and available on your `PATH`
- Must be executed from the **root of a Git repository**

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
