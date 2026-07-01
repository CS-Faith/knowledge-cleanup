---
description: Generate a deduplication analysis report without making changes
argument-hint: [path]
---

# Dedup Analysis Report

Analyze a directory for duplicate files without making any changes.

## Arguments
- $ARGUMENTS: Target directory path (defaults to current directory)

## Steps

1. Check if knowledge-cleanup is available
2. Run analysis-only mode:
   ```bash
   knowledge-cleanup $ARGUMENTS --analyze-only --format markdown
   ```
3. Present the report showing:
   - Total files scanned
   - Duplicate groups found
   - Potential space savings
   - File types breakdown
4. Suggest next steps (run /cleanup to dedupe)
