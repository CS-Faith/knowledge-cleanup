---
description: Run knowledge base cleanup (dedup) on a directory
argument-hint: [path]
---

# Knowledge Cleanup

Run the AI-powered knowledge base cleanup tool on the specified directory.

## Arguments
- $ARGUMENTS: Target directory path (defaults to current directory)

## Steps

1. Check if knowledge-cleanup is installed:
   ```bash
   which knowledge-cleanup || pip show knowledge-cleanup
   ```

2. If not installed, offer to install:
   ```bash
   pip install git+https://github.com/CS-Faith/knowledge-cleanup.git
   ```

3. Run dry-run analysis first:
   ```bash
   knowledge-cleanup $ARGUMENTS --dry-run --report
   ```

4. Show the analysis report to the user (duplicates found, space savings)

5. Ask user to confirm before proceeding with actual cleanup

6. If confirmed, run:
   ```bash
   knowledge-cleanup $ARGUMENTS --execute --backup
   ```

7. Show results summary

## Safety Rules
- ALWAYS run dry-run first
- ALWAYS confirm with user before deleting
- ALWAYS use --backup flag
- Never delete files without user confirmation
