<!-- catalog
{
  "title": "Describe what the installer changes",
  "summary": "Tell readers where binaries or files are installed, which persistent user settings change, and what supported option controls those changes.",
  "tasks": [
    "quickstart"
  ],
  "tags": [
    "onboarding",
    "installation"
  ],
  "aliases": [
    "installer side effects"
  ],
  "evidence": "unverified",
  "status": "active",
  "use_when": "Installation modifies files, configuration, or running services."
}
-->

# Describe what the installer changes

**Use when.** Installation modifies files, configuration, or running services.

**Reader task.** Quickstart and adoption.

**Practice.** Tell readers where binaries or files are installed, which persistent user settings change, and what supported option controls those changes. uv documents its installation directory and shell-profile behavior.

**Example (illustrative).** List the directories, shell profile entries, and services the installer creates.

**Result to check.** Compare a clean environment before and after installation against the documented inventory.

**Evidence.** Research reference. Run the reader check on the target project before relying on the documented outcome.

**Research references.** [uv installer options](https://docs.astral.sh/uv/reference/installer/)
