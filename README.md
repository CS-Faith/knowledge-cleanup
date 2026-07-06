# knowledge-cleanup

> **10,000 AI-generated notes shouldn't slow you down.** knowledge-cleanup removes duplicates, version chains, and directory chaos in 5 progressive rounds — with full rollback and zero source modification.

[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![GitHub Stars](https://img.shields.io/github/stars/CS-Faith/knowledge-cleanup?style=social)](https://github.com/CS-Faith/knowledge-cleanup/stargazers)
[![Reasonix Skill](https://img.shields.io/badge/Reasonix-Skill-green)](https://github.com/CS-Faith/knowledge-cleanup)

**AI-Powered Knowledge Base Cleanup Skill**

A 5-step progressive cleanup AI Skill for intelligent knowledge base organization. Built for AI agents (Reasonix, Claude Code, AutoGen, LangChain) and developers.

## 🎯 Key Features

### 5-Round Progressive Cleanup Algorithm
| Round | Operation | Description |
|-------|-----------|-------------|
| **R1** | MD5 Exact Duplicates | Byte-level duplicate file removal |
| **R2** | Filename Similarity | Version chain detection (V1→V2→V3...) |
| **R3** | Aggressive Normalization | Automatic implicit version discovery |
| **R4** | Archive Detection | Safe removal of extracted archives |
| **R5** | Directory Reorganization | Project/Management two-tier structure |

### Core Capabilities
- 🔍 Intelligent Detection: Semantic analysis for file versioning patterns
- 🛡️ Safe Operations: Read-only source, backup before every modification
- 📊 Detailed Reporting: Comprehensive cleanup reports for each round
- 🔄 Rollback Support: Full rollback capability for each round
- 🤖 AI Agent Integration: Native Reasonix Skill support
- 🚀 Cross-Platform: Works on Windows, macOS, and Linux

## 🚀 Quick Start

```bash
git clone https://github.com/CS-Faith/knowledge-cleanup.git
cd knowledge-cleanup
python run_cleanup.py <source_directory> <target_directory>
```

## 📊 Performance
- **9,676 files → 7,579 files** (-21.7% cleanup rate)
- **~2GB space freed** in typical cleanup
- **Safe execution** with user confirmation at each step

## 🤖 AI Framework Integration
- **Reasonix**: Native Skill support with `/skill knowledge-cleanup`
- **Claude Code**: Direct execution support
- **AutoGen**: Tool integration for AI agents
- **LangChain**: Compatible as a LangChain tool

## 🛡️ Safety Features
- Automatic backups before every modification
- Full rollback capability for each round
- Source directory is **read-only** - never modified
- All operations happen in target directory only

## 📜 License
MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Contact
- **GitHub**: [CS-Faith](https://github.com/CS-Faith)
- **Repository**: [knowledge-cleanup](https://github.com/CS-Faith/knowledge-cleanup)


---

## Next step

Cleaned your knowledge base? Build a structured Obsidian knowledge graph with [llm-wiki-pipeline](https://github.com/CS-Faith/llm-wiki-pipeline).

---

## 🔗 相关项目

| 项目 | 描述 | 链接 |
|------|------|------|
| **reasonix-portakit** | 便携工具箱 | [CS-Faith/reasonix-portakit](https://github.com/CS-Faith/reasonix-portakit) |
| **reasonix-migration-assistant** | 配置迁移升级助手 | [CS-Faith/reasonix-migration-assistant](https://github.com/CS-Faith/reasonix-migration-assistant) |
| **llm-wiki-pipeline** | 知识库构建流水线 | [CS-Faith/llm-wiki-pipeline](https://github.com/CS-Faith/llm-wiki-pipeline) |

