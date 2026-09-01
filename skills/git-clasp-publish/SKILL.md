---
name: git-clasp-publish
description: Check whether a local Git repository is current, commit and push intended changes to GitHub, and conditionally push and redeploy a Google Apps Script project with clasp. Use when the user asks to check the latest code, sync or publish a repository, or commit/push and redeploy Apps Script if needed.
---

# Git and Clasp Publish

Bring the current repository and its configured remotes to the requested published state without creating empty commits, unnecessary Apps Script versions, or unintended merge commits.

## Authorization

Treat inspection, fetching, and comparison as read-only preparation. Commit, push, `clasp push`, and deployment are authorized only when the user asks to sync, publish, push, release, or deploy. A request to check status alone does not authorize external changes.

## Inspect and synchronize Git

1. Read the repository's `AGENTS.md` files and release documentation before acting.
2. Inspect the branch, upstream, remotes, working tree, staged changes, and recent commits. Preserve unrelated user changes and stage exact intended paths instead of using `git add -A` by default.
3. Fetch the upstream remote and compare it with `HEAD`, for example with `git rev-list --left-right --count HEAD...@{upstream}`. Retry a transient HTTPS/TLS reset with command-scoped HTTP/1.1 when useful; do not weaken SSL verification.
4. If the branch is only behind and the worktree permits it, update with `git pull --ff-only`. If histories diverge or local changes conflict with incoming work, inspect the commits and stop for direction when choosing merge versus rebase would materially change history.
5. Before pushing, record all paths that differ from upstream. This list determines whether the Apps Script backend changed even after Git becomes synchronized.

## Validate, commit, and push

- Review the actual diff, run the repository's relevant validation, and check intended staged content for secrets or local configuration.
- Do not create an empty commit. If intended changes exist, stage only those paths and use a concise imperative commit subject.
- Push the current branch to its configured upstream without force. If there is nothing ahead after synchronization, skip the push.
- Verify that the final branch is synchronized and the working tree contains no unintended changes.

## Decide whether clasp is needed

Run this section only when the repository has `.clasp.json` and `clasp` is available.

1. Run `clasp status` to identify files included in the Apps Script project. Do not infer that every repository file is deployed by clasp; static CSS, build sources, and documentation are often excluded.
2. Compare the recorded release paths with the clasp-tracked paths. Run `clasp push` only if tracked Apps Script content changed, unless the user explicitly requested an unconditional push.
3. If `clasp push` reports that it skipped the push because nothing changed, do not create a new Apps Script version for an "if needed" request.
4. After a successful upload, inspect `clasp deployments`. Update the existing production deployment ID rather than running a bare `clasp deploy`, which creates another deployment.
5. Select a deployment ID from the user's instruction or repository documentation. If there is exactly one versioned non-`@HEAD` deployment, it may be used. If several could be production and none is identified, ask the user instead of guessing from version number or description.
6. Redeploy with a short description that matches the released behavior, then verify that the same deployment ID points to the new version.

## Report

State whether Git was already current or which commit was pushed. Separately state whether clasp was skipped, pushed without redeployment, or redeployed, including the deployment version when available. Mention any remaining local changes or required manual verification.
