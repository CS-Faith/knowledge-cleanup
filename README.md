# knowledge-cleanup

> 10,000+ AI 生成的笔记不应该成为你的负担。knowledge-cleanup 通过 5 轮递进式清理，去除重复文件、版本链和目录混乱 —— 完整回滚保证，源文件零修改。

> **10,000 AI-generated notes shouldn't slow you down.** knowledge-cleanup removes duplicates, version chains, and directory chaos in 5 progressive rounds — with full rollback and zero source modification.

[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

**AI 驱动的知识库清理 Skill** — 智能整理你的 AI 知识库，去除重复、版本链和目录混乱。专为 AI 代理（Reasonix、Claude Code、AutoGen、LangChain）和开发者设计。

## 🎯 核心特性

### 5 轮递进式清理算法
| 轮次 | 操作 | 说明 |
|-------|-----------|-------------|
| **R1** | MD5 精确去重 | 字节级重复文件删除 |
| **R2** | 文件名相似度 | 版本链检测（V1→V2→V3...） |
| **R3** | 激进归一化 | 自动发现隐式版本 |
| **R4** | 压缩包检测 | 安全移除已解压的压缩包 |
| **R5** | 目录重组 | 项目/管理双层结构 |

### 核心能力
- 🔍 智能检测：语义分析文件版本模式
- 🛡️ 安全操作：源目录只读，每次修改前备份
- 📊 详细报告：每轮清理后生成报告
- 🔄 回滚支持：每轮均可回滚
- 🤖 AI 代理集成：原生 Reasonix Skill 支持
- 🚀 跨平台：Windows、macOS、Linux 通用

## 🚀 快速开始

```bash
git clone https://github.com/CS-Faith/knowledge-cleanup.git
cd knowledge-cleanup
python run_cleanup.py <源目录> <目标目录>
```

## 📊 性能指标
- **9,676 files → 7,579 files**（-21.7% 清理率）
- 典型清理释放约 **~2GB** 空间
- 每步需要用户确认，安全执行

## 🤖 AI 框架集成
- **Reasonix**：原生 Skill 支持 `/skill knowledge-cleanup`
- **Claude Code**：直接执行
- **AutoGen**：工具集成
- **LangChain**：可作为 LangChain tool 使用

## 🛡️ 安全保障
- 每次修改前自动备份
- 每轮均可完整回滚
- **源目录只读** — 从不修改源文件
- 所有操作仅在目标目录进行

## 📜 许可证
MIT License — 详见 [LICENSE](LICENSE) 文件。

## 📞 联系方式
- **GitHub**：[CS-Faith](https://github.com/CS-Faith)
- **仓库**：[knowledge-cleanup](https://github.com/CS-Faith/knowledge-cleanup)

---

## Next step

Cleaned your knowledge base? Build a structured Obsidian knowledge graph with [llm-wiki-pipeline](https://github.com/CS-Faith/llm-wiki-pipeline).

See [OUTPUT_FORMAT.md](OUTPUT_FORMAT.md) for the technical integration spec.

---

## 🔗 相关项目

| 项目 | 描述 | 链接 |
|------|------|------|
| **reasonix-portakit** | 便携工具箱 | [CS-Faith/reasonix-portakit](https://github.com/CS-Faith/reasonix-portakit) |
| **reasonix-migration-assistant** | 配置迁移升级助手 | [CS-Faith/reasonix-migration-assistant](https://github.com/CS-Faith/reasonix-migration-assistant) |
| **llm-wiki-pipeline** | 知识库构建流水线 | [CS-Faith/llm-wiki-pipeline](https://github.com/CS-Faith/llm-wiki-pipeline) |

---

# knowledge-cleanup (English)

**AI-Powered Knowledge Base Cleanup Skill** — Intelligent cleanup for AI-generated note collections. Built for AI agents (Reasonix, Claude Code, AutoGen, LangChain) and developers.

## Key Features

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

## Quick Start

```bash
git clone https://github.com/CS-Faith/knowledge-cleanup.git
cd knowledge-cleanup
python run_cleanup.py <source_directory> <target_directory>
```

## Performance
- **9,676 files → 7,579 files** (-21.7% cleanup rate)
- **~2GB space freed** in typical cleanup
- **Safe execution** with user confirmation at each step

## AI Framework Integration
- **Reasonix**: Native Skill support with `/skill knowledge-cleanup`
- **Claude Code**: Direct execution support
- **AutoGen**: Tool integration for AI agents
- **LangChain**: Compatible as a LangChain tool

## Safety Features
- Automatic backups before every modification
- Full rollback capability for each round
- Source directory is **read-only** — never modified
- All operations happen in target directory only

## License
MIT License - see the [LICENSE](LICENSE) file for details.

## Contact
- **GitHub**: [CS-Faith](https://github.com/CS-Faith)
- **Repository**: [knowledge-cleanup](https://github.com/CS-Faith/knowledge-cleanup)
