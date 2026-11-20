<!-- catalog
{
  "title": "List what each format can read, write, and preserve",
  "summary": "Separate input and output support.",
  "tasks": [
    "overview"
  ],
  "tags": [
    "project-scope"
  ],
  "aliases": [
    "format fidelity matrix"
  ],
  "evidence": "unverified",
  "status": "active",
  "use_when": "Import, export, or round-trip behavior varies by file format."
}
-->

# List what each format can read, write, and preserve

**Use when.** Import, export, or round-trip behavior varies by file format.

**Reader task.** Purpose and audience.

**Practice.** Separate input and output support. State which content or formatting a named conversion may lose, and how to check a result that needs fidelity. Pandoc distinguishes its readers and writers and explains lossy conversions.

**Example (illustrative).** OBJ can be read and written. Texture metadata survives a round trip only with glTF.

**Result to check.** Test each stated read, write, or round-trip claim with a representative file.

**Evidence.** Research reference. Run the reader check on the target project before relying on the documented outcome.

**Research references.** [Pandoc conversion guidance](https://pandoc.org/MANUAL.html#description)
