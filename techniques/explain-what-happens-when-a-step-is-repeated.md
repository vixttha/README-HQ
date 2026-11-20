<!-- catalog
{
  "title": "Explain what happens when a step is repeated",
  "summary": "State whether repeating a command converges on the same result, resumes work, or creates another copy.",
  "tasks": [
    "first-result"
  ],
  "tags": [
    "troubleshooting"
  ],
  "aliases": [
    "rerun behavior and idempotency"
  ],
  "evidence": "unverified",
  "status": "active",
  "use_when": "A script or setup step may be run again on the same input."
}
-->

# Explain what happens when a step is repeated

**Use when.** A script or setup step may be run again on the same input.

**Reader task.** First result and recovery.

**Practice.** State whether repeating a command converges on the same result, resumes work, or creates another copy. Ansible’s module guide describes idempotency as a behavior that module authors should provide. Check the actual commands before promising it.

**Example (illustrative).** Running the generator again replaces only generated files in its output directory.

**Result to check.** Two runs on the same input leave the documented state and preserve named user files.

**Evidence.** Research reference. Run the reader check on the target project before relying on the documented outcome.

**Research references.** [Ansible module behavior](https://docs.ansible.com/projects/ansible/latest/module_plugin_guide/modules_intro.html)
