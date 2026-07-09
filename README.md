# Knowledge Cleanup - 知识库去重

> 你在 Obsidian / Notion 里攒了 847 篇笔记，其中 613 篇是重复或近似重复。每次搜索都看到 10 条相同结果——但不知道该信哪条。
> Knowledge Cleanup 用五轮递进把 847 篇压缩到 211 篇 S/A 级知识原件。

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Reasonix](https://img.shields.io/badge/Reasonix-Ecosystem-58a6ff)](https://github.com/CS-Faith/reasonix-ecosystem)

---

## 一句话定位

| 输入 | 输出 |
|------|------|
| 重复、冲突、低质文件（847 篇） | 去重后的 S/A/B/C 分层知识库（211 篇） |

---

## 一键运行

```bash
knowledge-cleanup clean --path ./my-knowledge --auto
```

---

## 为什么不用 fdupes / rdfind？

| 工具 | 能做什么 | 不能做什么 |
|------|---------|-----------|
| `fdupes` / `rdfind` | 找 MD5 相同文件 | 找「改了 20% 内容的版本链」 |
| **Knowledge Cleanup** | MD5 → 版本链 → 归一化 → 压缩包 → 目录重组 | — |

第一轮先干掉纯重复（MD5），最后一轮把剩余文件按语义重组成目录。**只有 5 轮递进，才能从 847 → 211**——而不是 847 → 613。

---

## 真实数据（知识库清理前 vs 清理后）

| 指标 | 清理前 | 清理后 |
|------|--------|--------|
| 总文件数 | 847 | 211 |
| S 级原件（核心原理） | — | 47 |
| A 级原件（最佳实践） | — | 164 |
| 重复组 | 312 组 | 0 |

---

## 安全机制

- 所有操作前自动备份到 `.backup/` 目录
- 支持 `--preview` 预览模式（不实际修改任何文件）
- 所有删除操作可逆

---

<details>
<summary>📖 五轮完整流程（展开查看）</summary>

### Phase 1: MD5 精确去重
计算所有文件 MD5，删除完全相同的副本。

### Phase 2: 版本链检测
检测「同一文件的不同版本」（内容相似度 > 80%），保留最新版本。

### Phase 3: 归一化去重
统一格式（换行符、编码、空格）后再次比较。

### Phase 4: 压缩包检测
检测 ZIP / TAR 内的重复文件。

### Phase 5: 目录重组
按语义重新组织目录结构，合并相关文件。

</details>

---

## Next Step

清理完的知识可以喂给流水线 → [**llm-wiki-pipeline**](https://github.com/CS-Faith/llm-wiki-pipeline) 把 211 篇原件变成 70% 密度的 Obsidian 知识图谱

蒸馏对话丢失的知识 → [**Conversation Distiller**](https://github.com/CS-Faith/conversation-distiller) 把 AI 对话记录转成永久知识

---

## License
MIT © 2026 [CS-Faith](https://cs-faith.github.io)

<details>
<summary>English Version</summary>

**Knowledge Cleanup** — Dedup without the fear. Five progressive passes — nothing gets deleted unless you say so. File hoarding, cured.

Your knowledge base has duplicates you can't find with simple tools. `fdupes` finds MD5-identical files. Knowledge Cleanup finds version chains, near-duplicates, and semantic overlap.

### Five Rounds
1. MD5 exact dedup
2. Version chain detection (>80% similarity)
3. Normalization (line endings, encoding, whitespace)
4. Archive content dedup
5. Semantic directory restructuring

### Safety
- Auto-backup to `.backup/` before any operation
- `--preview` mode (no actual changes)
- All deletions are reversible
</details>