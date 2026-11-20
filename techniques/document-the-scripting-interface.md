<!-- catalog
{
  "title": "Document the scripting interface",
  "summary": "Show where scripts can find structured output and which outcomes return which exit codes.",
  "tasks": [
    "first-result"
  ],
  "tags": [
    "automation"
  ],
  "aliases": [
    "command line automation"
  ],
  "evidence": "unverified",
  "status": "active",
  "use_when": "People or tools need to automate the task without parsing prose output."
}
-->

# Document the scripting interface

**Use when.** People or tools need to automate the task without parsing prose output.

**Reader task.** First result and recovery.

**Practice.** Show where scripts can find structured output and which outcomes return which exit codes. Include command-specific exceptions when they affect automation. GitHub CLI documents both formatting and exit behavior.

**Example (illustrative).** Document a JSON output option, exit codes, and one pipeline consuming the result.

**Result to check.** A script can distinguish success from failure without scraping human-oriented output.

**Evidence.** Research reference. Run the reader check on the target project before relying on the documented outcome.

**Research references.** [GitHub CLI output formatting](https://cli.github.com/manual/gh_help_formatting) · [Exit codes](https://cli.github.com/manual/gh_help_exit-codes) · [Authentication status exception](https://cli.github.com/manual/gh_auth_status)
