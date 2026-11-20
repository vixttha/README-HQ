<!-- catalog
{
  "title": "Expose discovery metadata through the README",
  "summary": "Use host-supported metadata for fields such as dataset language, license, tags, and file layout.",
  "tasks": [
    "handoff",
    "navigation"
  ],
  "tags": [
    "publication"
  ],
  "aliases": [
    "yaml discovery metadata"
  ],
  "evidence": "unverified",
  "status": "active",
  "use_when": "A host indexes documented machine-readable metadata in a README."
}
-->

# Expose discovery metadata through the README

**Use when.** A host indexes documented machine-readable metadata in a README.

**Reader task.** Handoff and maintenance.

**Practice.** Use host-supported metadata for fields such as dataset language, license, tags, and file layout. Hugging Face renders a dataset README as a card and uses its YAML fields for discovery and configuration.

**Example (illustrative).** Declare a dataset’s task, language, and license in its documented README metadata fields.

**Result to check.** The hosting platform parses the metadata and exposes the record under the expected filters.

**Evidence.** Research reference. Run the reader check on the target project before relying on the documented outcome.

**Research references.** [Hugging Face dataset cards](https://huggingface.co/docs/hub/datasets-cards)
