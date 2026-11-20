<!-- catalog
{
  "title": "Relative navigation",
  "summary": "Link same-checkout guides and assets with paths relative to the Markdown file.",
  "tasks": [
    "navigation",
    "quickstart"
  ],
  "tags": [
    "links",
    "git",
    "onboarding"
  ],
  "aliases": [
    "same-checkout links",
    "relative documentation links"
  ],
  "evidence": "observed",
  "status": "active"
}
-->

# Relative navigation

**Problem.** A link to a moving branch can send readers to instructions that differ from the checkout they are using.

**Practice.** Use a relative path for a guide or asset shipped alongside the README. Resolve it from the directory of the file containing the link. Recheck the path if the README is copied to a new location.

**Example.** The pinned Veraphify README links its accompanying verification guide with the relative path `docs/verification.md`.

**Limits.** Use this for files meant to travel with the current checkout. Historical claims about a different revision need a link to that specific source.

**Result to check.** Open the route from the target branch and from a clone. Confirm that it points to the intended file and section in each location.

**Evidence.** Observed in the cited guidance or example. [GitHub’s relative-link guidance](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes#relative-links-and-image-paths-in-markdown-files) · [Pinned Veraphify README](https://github.com/vixttha/Veraphify/blob/88d5d08cd8c80de3927858685878e51b6d7c69b8/README.md)
