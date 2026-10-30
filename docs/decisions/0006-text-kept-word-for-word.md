# 0006: Text kept word for word

Date: 2026-09-26. Status: accepted.

## Context

Phase E rewrites most of the profile README from a template. Some of the old text is
personal, and some of it carries facts only I can vouch for. That text should not
change as a side effect of the rewrite.

## Options

1. Rewrite everything to the new plan and check it all again. I would have to find
   my own lines again inside new text.
2. Keep those lines exactly as they are, and change them only on purpose.

## Decision

Option 2. These parts of the README at commit `fe5d040` are kept byte for byte:

- The "Also" block: the `## Also` heading and its three lines. This includes the Hack
  the North line, which is also covered by the guard in
  [ADR 0004](0004-checks-and-the-hack-the-north-guard.md).
- The contact line under it, with the email address and the two links.

They sit in `README.template.md` as plain text, with no placeholders, at the end of
the file. The guard test checks them on every render.

Everything else in today's README (the opening lines, the two project paragraphs and
the Tools list) may be rewritten to follow plan section `5.6`. Facts about me in the
new text come only from my own written notes.

If a later change needs a kept line to change, that edit is made on its own, in a
commit that names the line and the reason.

## Consequences

- My own words and the facts only I can confirm stay as I wrote them.
- The rewritten parts of the README are new text. I read the whole profile again
  before I share it.
