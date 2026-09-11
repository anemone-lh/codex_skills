# Codex Skills

本仓库用于维护可移植、可测试的个人 Codex Skills。目前包含 `collecting-internship-applications`：它可以从用户提供的招聘链接中提取职位信息，并根据本地简历模板生成针对特定岗位的定制简历。

## Collecting Internship Applications

源码：[`skill-src/collecting-internship-applications`](skill-src/collecting-internship-applications)

功能：

- 提取公司、岗位、地点、薪资、申请链接、内推码和岗位要求。
- 将信息写入带 UTF-8 BOM 的 CSV 求职跟踪表，并支持 URL 规范化和重复记录合并。
- 使用 CSV 中的 `generate_resume` 字段作为可移植的开关：`false` 表示只记录岗位，`true` 表示需要生成针对性简历。
- 只改写原始简历中已有事实，使用简洁的 STAR 风格要点和真实匹配的 ATS 关键词。
- 经过渲染质量检查后，同时生成可编辑的 DOCX 和可直接投递的 PDF。
- 不会自动提交求职申请、输入账户凭据或虚构候选人经历。

## 安装与配置

将 Skill 复制到 Codex Skills 目录：

```bash
cp -R skill-src/collecting-internship-applications /absolute/path/to/codex/skills/
```

在已安装的 `SKILL.md` 旁创建私有本地配置：

```bash
cp /absolute/path/to/codex/skills/collecting-internship-applications/config.example.json \
  /absolute/path/to/codex/skills/collecting-internship-applications/config.local.json
```

编辑 `config.local.json`，填写三个绝对路径：

```json
{
  "tracker_csv": "/absolute/path/to/job-search/Intership_Information.csv",
  "resume_template": "/absolute/path/to/resume/editable-template.docx",
  "resume_output_root": "/absolute/path/to/job-search/tailored-resumes"
}
```

Git 会忽略 `config.local.json`。请勿提交求职跟踪表、简历、生成的文档或包含私人路径的配置。

验证配置且不输出其中的路径值：

```bash
python3 /absolute/path/to/codex/skills/collecting-internship-applications/scripts/validate_config.py \
  --config /absolute/path/to/codex/skills/collecting-internship-applications/config.local.json
```

## 使用方法

示例提示词：

```text
将这个实习岗位收集到我的求职跟踪表中：https://example.com/job/123
```

```text
处理求职跟踪表中 generate_resume 开关为 true 的岗位。
```

CSV 规范请参阅 [`tracker-schema.md`](skill-src/collecting-internship-applications/references/tracker-schema.md)，简历真实性和渲染要求请参阅 [`resume-tailoring.md`](skill-src/collecting-internship-applications/references/resume-tailoring.md)。

## 测试

```bash
python3 -m unittest discover \
  -s skill-src/collecting-internship-applications/tests \
  -v
```

使用 Codex 安装目录中附带的验证器检查 Skill 目录。该验证器依赖 `PyYAML`。

仓库中的所有测试均在临时目录内运行，不会写入真实的求职跟踪表或简历目录。
