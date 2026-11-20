<!-- catalog
{
  "title": "List the local service URLs by purpose",
  "summary": "When setup starts several services, tell readers which address opens the app, dashboard, API, or other local tool.",
  "tasks": [
    "quickstart"
  ],
  "tags": [
    "onboarding",
    "configuration"
  ],
  "aliases": [
    "local ports and endpoints"
  ],
  "evidence": "unverified",
  "status": "active",
  "use_when": "Several local services or ports become available during setup."
}
-->

# List the local service URLs by purpose

**Use when.** Several local services or ports become available during setup.

**Reader task.** Quickstart and adoption.

**Practice.** When setup starts several services, tell readers which address opens the app, dashboard, API, or other local tool. Supabase CLI labels the addresses it prints for its development stack.

**Example (illustrative).** List the UI, health endpoint, and development API with a purpose beside each URL.

**Result to check.** Each documented URL reaches the named service after the prescribed startup.

**Evidence.** Research reference. Run the reader check on the target project before relying on the documented outcome.

**Research references.** [Supabase local development output](https://supabase.com/docs/guides/local-development/cli/getting-started) [Docker’s container development walkthrough](https://docs.docker.com/guides/lab-container-supported-development/)
