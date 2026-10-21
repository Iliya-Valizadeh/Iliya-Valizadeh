# 0005: Drafts stay out of the README

Date: 2026-09-26. Status: accepted.

## Context

Text that Iliya will publish in his own voice starts with the line
`DRAFT: Iliya to edit` and stays unpublished until he removes that line himself. The
profile has a Notes section that links to notes on the site. The notes are drafts
until he edits them. The same rule has to hold for any section of the README template
that is written for him but not yet read by him.

## Options

1. Keep drafts on a separate branch. Easy to forget, and the sync workflow runs only
   on `main`.
2. Let the author remember to leave drafts out. Nothing checks it.
3. Have the renderer drop anything marked as a draft, and fail if the marker reaches
   the output.

## Decision

Option 3, with one shared rule for the profile and the site.

What counts as a draft:

- A section of `README.template.md` is a draft when the first line of text under its
  heading, after blank lines, starts with `DRAFT: Iliya to edit`. The heading and
  everything under it, up to the next heading of the same or a higher level, are left
  out of `README.md`.
- A whole template is a draft when its first line of text starts with the marker. The
  renderer then refuses to write anything.
- A note is published only when the site lists it. The profile does not read note
  files. It reads `https://iliya-valizadeh.github.io/notes.json` from the live site, which the site's build writes from
  published notes only. The site repo's own decision record says how the site decides.
  If that file does not exist yet (the site has not been deployed by its new build),
  the Notes section is left out. Any other error stops the render, so a network
  problem cannot quietly remove the section.
- With no published notes, the Notes section is left out of the README entirely. It
  never says "coming soon".

Fail-closed checks:

- If the marker text appears anywhere in the template other than as the first line of
  a section or file, the render fails. The renderer does not guess.
- After rendering, if `DRAFT: Iliya to edit` appears anywhere in `README.md`, the
  render fails and nothing is written.
- Tests cover each case with small fixture templates: a draft section, a draft file, a
  stray marker in the middle of a paragraph, zero published notes, and one published
  note.

## Consequences

- Iliya publishes a note by deleting one line in the site repo. The profile picks it up
  on the next daily sync.
- The profile README itself is not marked as a draft. It goes live when this phase is
  merged. The review task adds a "Needs Iliya" item asking him to read it first.
