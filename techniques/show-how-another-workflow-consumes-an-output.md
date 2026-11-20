<!-- catalog
{
  "title": "Show how another workflow consumes an output",
  "summary": "Document output names and show a caller reading one of those outputs.",
  "tasks": [
    "handoff"
  ],
  "tags": [
    "interfaces"
  ],
  "aliases": [
    "downstream workflow example"
  ],
  "evidence": "unverified",
  "status": "active",
  "use_when": "A consumer uses a producer’s file, output value, or artifact."
}
-->

# Show how another workflow consumes an output

**Use when.** A consumer uses a producer’s file, output value, or artifact.

**Reader task.** Handoff and maintenance.

**Practice.** Document output names and show a caller reading one of those outputs. Demonstrate the boundary between steps or jobs when it changes the syntax.

**Example (illustrative).** Map the producer’s report path to the downstream workflow’s input setting.

**Result to check.** A downstream run consumes the sample output with the stated filename and format.

**Evidence.** Research reference. Run the reader check on the target project before relying on the documented outcome.

**Research references.** [Artifact action outputs](https://github.com/actions/upload-artifact/blob/cf430e030ddbb5b0abf93d22962f4752f3646cd9/README.md#L118-L125) · [Caller examples](https://github.com/actions/upload-artifact/blob/cf430e030ddbb5b0abf93d22962f4752f3646cd9/README.md#L362-L389)
