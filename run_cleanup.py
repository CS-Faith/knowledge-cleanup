#!/usr/bin/env python3
"""
知识库文件查重与整理 — 统一脚本
用法: python run_cleanup.py <源目录> <结果目录>

五轮递进式清理:
  R1: MD5 完全重复
  R2: 文件名相似度版本链
  R3: 激进版归一化自动清理
  R4: 压缩包检测
  R5: 目录结构重组（需用户交互确认结构）
"""

import os, sys, re, hashlib, shutil, zipfile
from collections import defaultdict
from datetime import datetime

# ═══════════════════════════════════════════════════════════
# UTILITIES
# ═══════════════════════════════════════════════════════════

def md5_file(path):
    try:
        with open(path, 'rb') as f:
            return hashlib.md5(f.read()).hexdigest()
    except:
        return None

def backup_path(target, round_num):
    return os.path.join(target, '_backup', f'round{round_num}')

def make_backup(target, round_num, files):
    """Copy files to backup before modifying"""
    bp = backup_path(target, round_num)
    for rel in files:
        src = os.path.join(target, rel)
        dst = os.path.join(bp, rel)
        if os.path.exists(src):
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            try:
                if os.path.isdir(src):
                    shutil.copytree(src, dst)
                else:
                    shutil.copy2(src, dst)
            except:
                pass

def write_report(target, round_num, name, content):
    report_path = os.path.join(target, f'清理报告_R{round_num}_{name}.md')
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(f'# 清理报告 — 第{round_num}轮：{name}\n\n')
        f.write(f'> 执行时间：{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n\n')
        f.write(content)
    print(f'\n📄 报告: {report_path}')

def ask_confirm(round_num, name):
    print(f'\n⏸️  第{round_num}轮（{name}）完成。')
    print('   输入 y 继续下一轮，n 终止，r 回滚本轮: ', end='')
    try:
        resp = input().strip().lower()
        if resp == 'r':
            return 'rollback'
        return resp == 'y'
    except EOFError:
        return True  # non-interactive, auto-continue

def rollback_round(target, round_num):
    bp = backup_path(target, round_num)
    if not os.path.exists(bp):
        print('   无备份可回滚')
        return
    for dirpath, _, filenames in os.walk(bp):
        for fn in filenames:
            src = os.path.join(dirpath, fn)
            rel = os.path.relpath(src, bp)
            dst = os.path.join(target, rel)
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copy2(src, dst)
    print(f'   已从 _backup/round{round_num} 回滚')

# ═══════════════════════════════════════════════════════════
# ROUND 1: MD5 Exact Duplicates
# ═══════════════════════════════════════════════════════════

# Extensions to skip (tool-generated resources)
SKIP_EXTS = {'.html', '.css', '.js', '.svg', '.woff2', '.eot', '.ttf',
             '.cur', '.gif', '.ico', '.bmp', '.png', '.jpg', '.jpeg',
             '.dll', '.mexw64', '.msi', '.chm', '.inf', '.cab',
             '.sa3', '.sn3', '.at3', '.dl_', '._br', '._cn', '._de',
             '._es', '._fr', '._hu', '._it', '._jp', '.ldb'}

def round1_md5(target):
    print('\n' + '='*60)
    print('🔍 第1轮：MD5 完全重复检测')
    print('='*60)

    # Scan files
    file_by_md5 = defaultdict(list)
    total = 0
    for dirpath, _, filenames in os.walk(target):
        # Skip backup dirs
        if '_backup' in dirpath:
            continue
        for fn in filenames:
            total += 1
            ext = os.path.splitext(fn)[1].lower()
            fullpath = os.path.join(dirpath, fn)
            relpath = os.path.relpath(fullpath, target)

            if ext in SKIP_EXTS:
                continue

            h = md5_file(fullpath)
            if h:
                file_by_md5[h].append(relpath)

    # Find duplicates
    dup_groups = {h: files for h, files in file_by_md5.items() if len(files) > 1}
    total_dup_files = sum(len(files) - 1 for files in dup_groups.values())

    # Report
    lines = []
    lines.append(f'| 指标 | 数值 |')
    lines.append(f'|------|------|')
    lines.append(f'| 扫描文件数 | {total} |')
    lines.append(f'| 重复 MD5 组数 | {len(dup_groups)} |')
    lines.append(f'| 可清理文件数 | {total_dup_files} |')
    lines.append('')

    if dup_groups:
        lines.append('### 重复详情（前30组）')
        lines.append('| MD5 | 文件数 | 文件列表 |')
        lines.append('|-----|--------|----------|')
        for h, files in list(dup_groups.items())[:30]:
            names = '、'.join(os.path.basename(f) for f in files[:5])
            if len(files) > 5:
                names += f' ... (+{len(files)-5})'
            lines.append(f'| {h[:16]}... | {len(files)} | {names} |')

    # Execute: move duplicates to backup
    backup_files = []
    for h, files in dup_groups.items():
        for f in files[1:]:  # keep first, trash rest
            backup_files.append(f)
            src = os.path.join(target, f)
            dst = os.path.join(backup_path(target, 1), f)
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            try:
                shutil.move(src, dst)
            except:
                pass

    lines.append('')
    lines.append(f'### 执行结果')
    lines.append(f'已移入 `_backup/round1/`: {len(backup_files)} 个重复文件')

    write_report(target, 1, 'MD5完全重复', '\n'.join(lines))
    return total_dup_files

# ═══════════════════════════════════════════════════════════
# ROUND 2: Filename Similarity Version Chains
# ═══════════════════════════════════════════════════════════

DOC_EXTS = {'.doc', '.docx', '.pdf', '.txt', '.xlsx', '.xls', '.xlsm',
            '.pptx', '.ppt', '.xmind', '.eapx', '.eap', '.rp', '.rar',
            '.zip', '.md', '.vsdx', '.eddx'}

def normalize_light(name):
    """Light normalization - strip obvious version markers"""
    stem, ext = os.path.splitext(name)
    base = stem
    # Remove parenthesized content
    base = re.sub(r'[（(][^）)]*[）)]', '', base)
    # Remove bracket content 【】
    base = re.sub(r'【[^】]*】', '', base)
    # Remove V version tags
    base = re.sub(r'[_\- ]?[Vv]\d+[.\d]*', '', base)
    # Remove date suffixes like 9.23, 3.25
    base = re.sub(r'[_\- ]?\d{1,2}[.]\d{1,2}$', '', base)
    # Remove common qualifiers
    for q in ['新', '最新', '最新版', '最终', '最终版', '备份', '备份新',
              '副本', '原始版', '本地版', '修正版', '完整版', '改后',
              '改后2', '改后3', '定稿版', '新增用例版', '正式版']:
        base = re.sub(r'[_\- ]?' + re.escape(q) + r'$', '', base)
    base = re.sub(r'[\s_\-]+$', '', base).strip()
    return base if base else stem

def round2_similarity(target):
    print('\n' + '='*60)
    print('🔍 第2轮：文件名相似度版本链')
    print('='*60)

    file_groups = defaultdict(list)
    for dirpath, _, filenames in os.walk(target):
        if '_backup' in dirpath:
            continue
        for fn in filenames:
            ext = os.path.splitext(fn)[1].lower()
            fullpath = os.path.join(dirpath, fn)
            relpath = os.path.relpath(fullpath, target)
            try:
                st = os.stat(fullpath)
            except:
                continue
            base = normalize_light(fn)
            file_groups[base].append({
                'name': fn, 'relpath': relpath,
                'size': st.st_size, 'mtime': st.st_mtime
            })

    # Find version chains (2+ files with different sizes)
    chains = []
    for base, files in file_groups.items():
        if len(files) < 2:
            continue
        sizes = [f['size'] for f in files]
        if len(set(sizes)) == 1:
            continue  # Skip identical-size (already handled by R1)
        # Only include groups with at least one document-type file
        if not any(os.path.splitext(f['name'])[1].lower() in DOC_EXTS for f in files):
            continue
        files_sorted = sorted(files, key=lambda f: f['mtime'])
        chains.append((base, files_sorted, files_sorted[-1]))  # newest is keeper

    # Execute
    lines = []
    trashed = 0
    for base, files, keeper in chains:
        lines.append(f'### {base[:60]}（{len(files)}个版本）')
        lines.append(f'| 操作 | 文件 | 大小 | 修改时间 |')
        lines.append(f'|------|------|------|----------|')
        for f in files[:-1]:  # all except newest
            src = os.path.join(target, f['relpath'])
            dst = os.path.join(backup_path(target, 2), f['relpath'])
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            try:
                shutil.move(src, dst)
                trashed += 1
            except:
                pass
            lines.append(f'| 🗑️ | {f["name"][:50]} | {f["size"]/1024:.1f}KB | {datetime.fromtimestamp(f["mtime"]).strftime("%Y-%m-%d")} |')
        lines.append(f'| ✅ 保留 | {keeper["name"][:50]} | {keeper["size"]/1024:.1f}KB | {datetime.fromtimestamp(keeper["mtime"]).strftime("%Y-%m-%d")} |')
        lines.append('')

    summary = f'| 指标 | 数值 |\n|------|------|\n| 版本链组数 | {len(chains)} |\n| 清理旧版本数 | {trashed} |'
    lines.insert(0, summary + '\n')

    write_report(target, 2, '文件名相似度版本链', '\n'.join(lines))
    return trashed

# ═══════════════════════════════════════════════════════════
# ROUND 3: Aggressive Normalization
# ═══════════════════════════════════════════════════════════

def normalize_aggressive(name):
    stem, ext = os.path.splitext(name)
    base = stem
    base = re.sub(r'[（(][^）)]*[）)]', '', base)
    base = re.sub(r'【[^】]*】', '', base)
    base = re.sub(r'［[^］]*］', '', base)
    base = re.sub(r'[_\- ]?[Vv]\s*\d+([.\-]\d+)*([_\-]\w+)*', '', base)
    base = re.sub(r'[_\- ]?\d{8}', '', base)
    base = re.sub(r'[_\- ]?\d{4}[._-]\d{1,2}[._-]\d{1,2}', '', base)
    base = re.sub(r'[_\- ]?\d{1,2}[.]\d{1,2}$', '', base)
    qualifiers = ['新增用例版', '征求意见稿', '适用于矩阵岗位双维度考核使用',
                  '最新版', '最终版', '最终', '原始版', '本地版', '修正版',
                  '完整版', '正式版', '涉密人员', '自我评分',
                  '备份新', '备份', '副本', '改后3', '改后2', '改后', '修改',
                  '新', '最新', '旧', '定稿版', 'final', 'temp', 'old']
    for q in sorted(qualifiers, key=len, reverse=True):
        base = re.sub(r'(?:[_\- ]|^)' + re.escape(q) + r'(?:[_\- ]|$)', ' ', base)
        base = re.sub(re.escape(q) + r'$', '', base)
    base = re.sub(r'[_\- ]\d+$', '', base)
    base = re.sub(r'[\s_\-]+', ' ', base).strip(' _-')
    return base if base else stem

def round3_aggressive(target):
    print('\n' + '='*60)
    print('🔍 第3轮：激进版文件名归一化')
    print('='*60)

    file_groups = defaultdict(list)
    for dirpath, _, filenames in os.walk(target):
        if '_backup' in dirpath:
            continue
        for fn in filenames:
            ext = os.path.splitext(fn)[1].lower()
            if ext in SKIP_EXTS:
                continue
            fullpath = os.path.join(dirpath, fn)
            relpath = os.path.relpath(fullpath, target)
            try:
                st = os.stat(fullpath)
            except:
                continue
            base = normalize_aggressive(fn)
            file_groups[base].append({
                'name': fn, 'relpath': relpath,
                'size': st.st_size, 'mtime': st.st_mtime
            })

    chains = []
    for base, files in file_groups.items():
        if len(files) < 2:
            continue
        sizes = [f['size'] for f in files]
        if len(set(sizes)) <= 1:
            continue
        if not any(os.path.splitext(f['name'])[1].lower() in DOC_EXTS for f in files):
            continue
        files_sorted = sorted(files, key=lambda f: f['mtime'])
        chains.append((base, files_sorted))

    lines = []
    trashed = 0
    for base, files in chains:
        lines.append(f'### {base[:60]}（{len(files)}个版本）')
        lines.append(f'| 操作 | 文件 | 大小 | 修改时间 |')
        lines.append(f'|------|------|------|----------|')
        for f in files[:-1]:
            src = os.path.join(target, f['relpath'])
            dst = os.path.join(backup_path(target, 3), f['relpath'])
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            try:
                shutil.move(src, dst)
                trashed += 1
            except:
                pass
            lines.append(f'| 🗑️ | {f["name"][:50]} | {f["size"]/1024:.1f}KB | {datetime.fromtimestamp(f["mtime"]).strftime("%Y-%m-%d")} |')
        k = files[-1]
        lines.append(f'| ✅ 保留 | {k["name"][:50]} | {k["size"]/1024:.1f}KB | {datetime.fromtimestamp(k["mtime"]).strftime("%Y-%m-%d")} |')
        lines.append('')

    summary = f'| 指标 | 数值 |\n|------|------|\n| 版本链组数 | {len(chains)} |\n| 清理旧版本数 | {trashed} |'
    lines.insert(0, summary + '\n')

    write_report(target, 3, '激进版文件名归一化', '\n'.join(lines))
    return trashed

# ═══════════════════════════════════════════════════════════
# ROUND 4: Archive Detection
# ═══════════════════════════════════════════════════════════

def round4_archives(target):
    print('\n' + '='*60)
    print('🔍 第4轮：压缩包检测')
    print('='*60)

    archives = []
    for dirpath, _, filenames in os.walk(target):
        if '_backup' in dirpath:
            continue
        for fn in filenames:
            if fn.lower().endswith(('.rar', '.zip', '.7z')):
                archives.append((dirpath, fn))

    lines = []
    trashed = 0
    freed = 0

    for dirpath, fn in archives:
        fullpath = os.path.join(dirpath, fn)
        basename = os.path.splitext(fn)[0]
        extracted_dir = os.path.join(dirpath, basename)
        size_mb = os.path.getsize(fullpath) / (1024 * 1024)

        if os.path.isdir(extracted_dir) and os.listdir(extracted_dir):
            # Already extracted
            rel = os.path.relpath(fullpath, target)
            dst = os.path.join(backup_path(target, 4), rel)
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.move(fullpath, dst)
            trashed += 1
            freed += size_mb
            lines.append(f'| 🗑️ | {fn[:50]} | {size_mb:.1f}MB | ✅ 已解压到 `{basename}/` |')
        else:
            lines.append(f'| ⏭️ | {fn[:50]} | {size_mb:.1f}MB | ❌ 未解压，保留 |')

    summary = (f'| 指标 | 数值 |\n|------|------|\n'
               f'| 扫描压缩包数 | {len(archives)} |\n'
               f'| 已解压可删除 | {trashed} |\n'
               f'| 释放空间 | {freed:.0f} MB |')
    header = summary + '\n\n| 操作 | 压缩包 | 大小 | 状态 |\n|------|--------|------|------|'
    lines.insert(0, header)

    write_report(target, 4, '压缩包检测', '\n'.join(lines))
    return trashed

# ═══════════════════════════════════════════════════════════
# ROUND 5: Directory Reorganization
# ═══════════════════════════════════════════════════════════

def round5_reorganize(target):
    print('\n' + '='*60)
    print('🔍 第5轮：目录结构重组')
    print('='*60)

    # Survey current structure
    lines = []
    lines.append('### 当前顶层结构')
    lines.append('')
    for item in sorted(os.listdir(target)):
        if item.startswith('_') or item.startswith('清理报告'):
            continue
        ip = os.path.join(target, item)
        if os.path.isdir(ip):
            fc = sum(1 for _ in os.walk(ip) for f in _[2])
            lines.append(f'- `{item}/` ({fc} files)')
        else:
            lines.append(f'- `{item}`')
    lines.append('')

    lines.append('### 重组建议')
    lines.append('')
    lines.append('请根据以下抽象判据，对上述目录进行分类：')
    lines.append('')
    lines.append('| 分类 | 判据 |')
    lines.append('|------|------|')
    lines.append('| **项目** | 服务于特定交付物的完整工作集：系统设计、技术规格、需求文档、测试方案、外部合作项目全套产物 |')
    lines.append('| **管理** | 跨项目的重复性管理产物：工作计划与周报、绩效考核、资质申报、业务分析、竞对研究、宣传材料 |')
    lines.append('| **其他** | 无法归类的零散文件 |')
    lines.append('')
    lines.append('> ⚠️ 本 Skill 仅生成分类建议，需用户确认后由 Agent 执行具体重组。')
    lines.append('> 工具软件安装包/ISO 等不应出现在知识库中，建议移到独立目录。')

    write_report(target, 5, '目录结构重组', '\n'.join(lines))
    print('\n📋 第5轮需要人工交互。请 Agent 根据上方判据设计方案，用户确认后执行。')
    return 0  # R5 is interactive

# ═══════════════════════════════════════════════════════════
# FINAL REPORT
# ═══════════════════════════════════════════════════════════

def generate_final_report(target, source, remaining, backup_count):
    """Aggregate all round reports into a comprehensive final report."""
    print('\n📄 生成综合清理报告...')

    report_path = os.path.join(target, '综合清理报告.md')
    lines = []
    lines.append('# 综合清理报告')
    lines.append('')
    lines.append(f'> 源目录: `{source}`')
    lines.append(f'> 结果目录: `{target}`')
    lines.append(f'> 完成时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
    lines.append('')
    lines.append('---')
    lines.append('')

    # ── Summary ──
    lines.append('## 总览')
    lines.append('')
    lines.append('| 指标 | 数值 |')
    lines.append('|------|------|')
    lines.append(f'| 结果目录文件数 | {remaining} |')
    lines.append(f'| 备份区文件数 | {backup_count} |')

    # Source file count
    src_count = sum(1 for _ in os.walk(source) for f in _[2]) if os.path.exists(source) else 0
    lines.append(f'| 源目录文件数 | {src_count} |')
    if src_count > 0:
        lines.append(f'| 清理率 | {(src_count - remaining) / src_count * 100:.1f}% |')
    lines.append('')

    # ── Per-round summary ──
    lines.append('## 各轮执行摘要')
    lines.append('')

    round_names = {
        1: 'MD5 完全重复',
        2: '文件名相似度版本链',
        3: '激进版文件名归一化',
        4: '压缩包检测',
        5: '目录结构重组',
    }

    for num in range(1, 6):
        name = round_names[num]
        lines.append(f'### 第{num}轮：{name}')
        lines.append('')

        # Try to read the per-round report
        round_report = os.path.join(target, f'清理报告_R{num}_{name}.md')
        if os.path.exists(round_report):
            with open(round_report, 'r', encoding='utf-8') as f:
                content = f.read()
            # Extract the body (skip the title line)
            body_lines = content.split('\n')
            # Skip the first 4 lines (title + blank + timestamp + blank)
            if len(body_lines) > 4:
                body = '\n'.join(body_lines[4:])
                lines.append(body)
            else:
                lines.append('(报告内容为空)')
        else:
            lines.append('(未生成报告 — 可能未执行或执行失败)')
        lines.append('')

    # ── Execution log ──
    lines.append('---')
    lines.append('')
    lines.append('## 执行过程')
    lines.append('')
    lines.append('| 轮次 | 操作 | 状态 |')
    lines.append('|------|------|------|')
    for num in range(1, 6):
        name = round_names[num]
        report_file = os.path.join(target, f'清理报告_R{num}_{name}.md')
        status = '✅ 已执行' if os.path.exists(report_file) else '⏭️ 未执行'
        lines.append(f'| {num} | {name} | {status} |')
    lines.append('')

    # ── Final directory structure ──
    lines.append('## 最终目录结构')
    lines.append('')
    lines.append('```')
    for item in sorted(os.listdir(target)):
        if item.startswith('_backup') or item.startswith('清理报告') or item == '综合清理报告.md':
            continue
        ip = os.path.join(target, item)
        if os.path.isdir(ip):
            fc = sum(1 for _ in os.walk(ip) for f in _[2])
            lines.append(f'{item}/ ({fc} files)')
        else:
            lines.append(item)
    lines.append('```')
    lines.append('')

    # ── Cleanup instruction ──
    lines.append('## 后续操作')
    lines.append('')
    lines.append(f'- 备份文件在 `_backup/` 目录（{backup_count} 个文件），确认无误后可删除')
    lines.append('- 删除备份后，知识库整理完成')
    lines.append('')
    lines.append('---')
    lines.append(f'*报告由 knowledge-cleanup Skill 自动生成*')

    with open(report_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

    print(f'   ✅ {report_path}')

# ═══════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════

def main():
    if len(sys.argv) < 3:
        print('用法: python run_cleanup.py <源目录> <结果目录>')
        print('示例: python run_cleanup.py D:\\原始材料 D:\\整理后')
        sys.exit(1)

    source = sys.argv[1]
    target = sys.argv[2]

    if not os.path.isdir(source):
        print(f'❌ 源目录不存在: {source}')
        sys.exit(1)

    print('═' * 60)
    print('  知识库文件查重与整理')
    print('═' * 60)
    print(f'  源目录: {source}')
    print(f'  结果目录: {target}')
    print()
    print('  ⚠️  所有操作在结果目录中进行，源目录只读不修改。')
    print()

    # Copy source to target
    if not os.path.exists(target):
        print(f'📋 正在复制源目录到结果目录...')
        shutil.copytree(source, target)
        print(f'   复制完成。')
    else:
        print(f'📋 结果目录已存在，跳过复制。')

    rounds = [
        (1, 'MD5完全重复', round1_md5),
        (2, '文件名相似度版本链', round2_similarity),
        (3, '激进版文件名归一化', round3_aggressive),
        (4, '压缩包检测', round4_archives),
        (5, '目录结构重组', round5_reorganize),
    ]

    for num, name, func in rounds:
        try:
            result = func(target)
        except Exception as e:
            print(f'\n❌ 第{num}轮执行出错: {e}')
            import traceback
            traceback.print_exc()
            result = 0

        if num < 5:
            action = ask_confirm(num, name)
            if action == 'rollback':
                rollback_round(target, num)
                print('   已回滚。是否重新执行本轮？(y/n): ', end='')
                if input().strip().lower() == 'y':
                    func(target)
                    ask_confirm(num, name)
            elif not action:
                print('   用户终止。')
                break
        else:
            print('\n📋 第5轮需人工设计重组方案并交互确认。')
            break

    # Final stats
    remaining = sum(1 for _ in os.walk(target) for f in _[2]
                    if '_backup' not in _[0])
    backup_count = sum(1 for _ in os.walk(os.path.join(target, '_backup')) for f in _[2]
                       if os.path.exists(os.path.join(target, '_backup')))

    print(f'\n{"="*60}')
    print(f'📊 当前状态')
    print(f'   结果目录文件: {remaining}')
    print(f'   备份文件: {backup_count}')
    print(f'   全部确认后，可删除 _backup/ 完成清理。')
    print(f'{"="*60}')

    # ── Generate final comprehensive report ──
    generate_final_report(target, source, remaining, backup_count)

if __name__ == '__main__':
    main()
