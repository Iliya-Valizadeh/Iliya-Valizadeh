# 0006: Text kept word for word

Date: 2026-09-26. Status: accepted.

## Context

Phase E rewrites most of the profile README from a template. Some of the text is
Iliya's own, and some of it carries facts only he can vouch for. That text should not
be rewritten by an agent.

## Options

1. Rewrite everything to the new plan and ask Iliya to check it all. He would have to
   find his own lines again inside new text.
2. Keep his lines exactly as they are, and change them only when he asks.

## Decision

Option 2. These parts of the README at commit `fe5d040` are kept byte for byte:

- The "Also" block: the `## Also` heading and its three lines. This includes the Hack
  the North line, which is also covered by the guard in
  [ADR 0004](0004-checks-and-the-hack-the-north-guard.md).
- The contact line under it, with the email address and the two links.

They sit in `README.template.md` as plain text, with no placeholders, at the end of
the file. The guard test checks them on every render.

Everything else in today's README (the opening lines, the two project paragraphs and
the Tools list) may be rewritten by the content task, which follows plan section `5.6`.
Facts about Iliya come only from `CLAUDE.md` at the root of the workspace.

If a later task finds a reason to change a kept line, it does not change it. It adds a
"Needs Iliya" item to `_portfolio/STATUS.md` that names the line and the reason, and
he decides.

## Consequences

- His own words and the facts only he can confirm stay as he wrote them.
- The rewritten parts of the README are drafts he has not read. The review task at the
  end of this phase asks him to read the profile before he shares it.
