<!-- cc-header-version: <VERSION> -->
# Context Compass: how this repository works

Context Compass agents coordinate in GitHub Issues in `<REPOSITORY>`
(`work_tracking.backend: github_issues`). Every agent reads this issue first.

<!-- BEGIN MANAGED: header -->
## Where things are

| What | Where |
| --- | --- |
| Tickets | issues labelled `cc-epic`, `cc-story` or `cc-task` |
| Current focus | open issues labelled `cc-active`, and each ticket's `## Route` section |
| Who holds a ticket | `claim`, `release` and `break` comments on the ticket |
| Agents | open issues labelled `cc-agent` |
| Messages | `message` comments on the recipient's agent issue |
| Artifacts and context packs | each ticket's Artifact Links and Context Management sections |
| Closed work | closed ticket issues |

## Rules every agent follows

- Posting a comment never overwrites anyone. Event comments are never edited.
- Each agent keeps one card comment per issue, marked with its own name, and edits
  only that card.
- Only a ticket's holder saves its body, title or state, and it checks the edit
  history after every save.
- The holder is the earliest `primary` claim that has not been released or broken.
- The holder copies what matters from cards and events into the body, and stamps
  the last comment it included.
- Labels are added and removed one at a time.
- Agents check out when they finish: they release their claims and close their
  agent issue. An agent silent for more than a day is stale, and another agent may
  check it out.

The full rules ship with Context Compass in
`context_compass/agent_onboarding/default/general/skills/github/issues_backend.md`.
<!-- END MANAGED: header -->

## Owner notes

Standing instructions for every agent in this repository. Agents keep this
section exactly as the owner writes it.

<!-- BEGIN USER-DEFINED: notes -->
<!-- END USER-DEFINED: notes -->
