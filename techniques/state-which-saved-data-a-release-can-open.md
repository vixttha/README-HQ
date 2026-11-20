<!-- catalog
{
  "title": "State which saved data a release can open",
  "summary": "Name which older saves, archives, or project files the new version can read, and describe rollback separately where supported.",
  "tasks": [
    "first-result"
  ],
  "tags": [
    "stored-state"
  ],
  "aliases": [
    "saved file compatibility"
  ],
  "evidence": "unverified",
  "status": "active",
  "use_when": "File compatibility differs across releases or file format versions."
}
-->

# State which saved data a release can open

**Use when.** File compatibility differs across releases or file format versions.

**Reader task.** First result and recovery.

**Practice.** Name which older saves, archives, or project files the new version can read, and describe rollback separately where supported. OpenTTD documents loading saves from older revisions.

**Example (illustrative).** This release can open files from version 2 onward. Export old version 1 projects using the named bridge release.

**Result to check.** Representative old files take the documented direct or migration route.

**Evidence.** Research reference. Run the reader check on the target project before relying on the documented outcome.

**Research references.** [OpenTTD save compatibility](https://github.com/OpenTTD/OpenTTD/blob/e8a7f94481f0a545715b221c8ae63271b60df98b/README.md#L56-L62)
