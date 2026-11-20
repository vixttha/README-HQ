<!-- catalog
{
  "title": "Show how asset variants map to published files",
  "summary": "Give the file naming pattern, label the dimensions or styles that change the filename, and show where to check whether a combination exists.",
  "tasks": [
    "demo"
  ],
  "tags": [
    "demos"
  ],
  "aliases": [
    "asset export mapping"
  ],
  "evidence": "unverified",
  "status": "active",
  "use_when": "Several published exports come from the same editable asset."
}
-->

# Show how asset variants map to published files

**Use when.** Several published exports come from the same editable asset.

**Reader task.** Demos and visuals.

**Practice.** Give the file naming pattern, label the dimensions or styles that change the filename, and show where to check whether a combination exists. Fluent UI’s SVG README specifies the names and which file inventory determines availability.

**Example (illustrative).** Map the SVG master to PNG exports by filename, size, and theme.

**Result to check.** A maintainer can pick the right published file without interpreting opaque filenames.

**Evidence.** Research reference. Run the reader check on the target project before relying on the documented outcome.

**Research references.** [Fluent UI SVG naming and availability](https://github.com/microsoft/fluentui-system-icons/blob/6c2c9075cf8952ef48369b2475233b6e9761efed/packages/svg-icons/README.md#L99-L110) [Google’s Material Icons guide](https://developers.google.com/fonts/docs/material_icons)
