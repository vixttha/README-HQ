<!-- catalog
{
  "title": "Preview changes before applying them",
  "summary": "When a workflow changes state and offers a preview, give the preview and apply steps distinct labels.",
  "tasks": [
    "quickstart"
  ],
  "tags": [
    "maintenance"
  ],
  "aliases": [
    "dry run before apply"
  ],
  "evidence": "unverified",
  "status": "active",
  "use_when": "An operation can describe its planned changes before it applies them."
}
-->

# Preview changes before applying them

**Use when.** An operation can describe its planned changes before it applies them.

**Reader task.** Quickstart and adoption.

**Practice.** When a workflow changes state and offers a preview, give the preview and apply steps distinct labels. Explain which changes the preview can predict. Terraform documents its plan separately from apply.

**Example (illustrative).** Run the plan command and inspect the file changes before using the apply command.

**Result to check.** The preview lists the relevant changes and leaves the target unchanged.

**Evidence.** Research reference. Run the reader check on the target project before relying on the documented outcome.

**Research references.** [Terraform plan](https://developer.hashicorp.com/terraform/cli/commands/plan) · [Ansible check mode limits](https://docs.ansible.com/projects/ansible/latest/playbooks_checkmode.html) [Helm upgrade preview options](https://helm.sh/docs/helm/helm_upgrade/)
