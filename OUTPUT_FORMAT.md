# Output Format

This document defines the standard output format of knowledge-cleanup
and how it feeds directly into [llm-wiki-pipeline](https://github.com/CS-Faith/llm-wiki-pipeline).

## Directory Structure

After running knowledge-cleanup, the target directory contains:

```
<target>/
├── cleaned/              # Phase 1 input for llm-wiki-pipeline
│   ├── project-A/        # Reorganized project folders
│   ├── project-B/
│   └── ...
├── knowledge-cleanup-log.json    # Stats and rollback metadata
└── rollback/             # Full backup for undo
```

## knowledge-cleanup-log.json

```json
{
  "timestamp": "2026-07-06T10:00:00Z",
  "source": "/path/to/raw-notes",
  "target": "/path/to/cleaned",
  "stats": {
    "filesBefore": 12847,
    "filesAfter": 7579,
    "removed": 5268,
    "reductionRate": 0.41,
    "spaceFreed": "2.3 GB"
  },
  "rounds": {
    "R1_md5": { "removed": 3201 },
    "R2_versionChain": { "removed": 892 },
    "R3_normalization": { "removed": 654 },
    "R4_archive": { "removed": 312 },
    "R5_reorganize": { "removed": 209 }
  },
  "rollbackAvailable": true
}
```

## Feeding into llm-wiki-pipeline

```bash
# Step 1: Clean
python run_cleanup.py ./raw-notes ./cleaned

# Step 2: Build wiki (reads ./cleaned/ directly)
cd ../llm-wiki-pipeline
python -m skills.karpathy-llm-wiki --input ../knowledge-cleanup/cleaned/
```

## llm-wiki-pipeline --skip-cleanup flag

When llm-wiki-pipeline detects a `knowledge-cleanup-log.json` in the input
directory, it automatically:

- Displays cleanup stats to the user
- Confirms the user wants to skip Phase 1 (dedup)
- Proceeds directly to Phase 2 (format conversion)

This avoids double-cleaning and respects the user's prior work.

## Version Compatibility

| knowledge-cleanup | llm-wiki-pipeline | Compatibility |
|:-----------------:|:-----------------:|:-------------:|
| v1.0+ | v1.0+ | Full |

## FAQ

**Q: Can I use knowledge-cleanup without llm-wiki-pipeline?**
A: Yes. Standalone cleanup produces a clean, organized directory ready for any tool.

**Q: Can I use llm-wiki-pipeline without knowledge-cleanup?**
A: Yes. llm-wiki-pipeline has its own Phase 1 dedup, but running
knowledge-cleanup first gives better results for severely bloated knowledge bases.

**Q: What if I need to rollback?**
A: Every round creates a backup in `rollback/`. Run `python run_cleanup.py --rollback`
to restore any round.
