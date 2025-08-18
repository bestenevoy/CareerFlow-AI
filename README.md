# CareerFlow-AI

一个AI驱动的劳动力市场研究系统，结合了数据库查询、职位分析和自动报告生成功能。

## 🚀 功能

### 核心功能
- **多智能体架构**: 包含专业子智能体的分层系统
- **数据库集成**: 本地SQLite数据库与CSV数据加载
- **职位分析**: 自动化职位数据提取和分析
- **报告生成**: AI驱动的市场研究报告创建

### 智能体系统
- **分析智能体**: 主协调智能体
- **数据库智能体**: 处理结构化数据查询
- **职位推荐智能体**: 分析职位数据并生成推荐
- **简历分析智能体**: 处理简历数据

## 📁 项目结构

```
CareerFlow-AI/
├── agent/                          # 多智能体系统
│   ├── agent.py                    # 主智能体
│   ├── llm_config.py               # LLM配置
│   ├── analysis_agent/             # 分析智能体
│   ├── database_agent/             # 数据库智能体
│   ├── job_recommend_agent/        # 职位推荐智能体
│   └── resume_agent/               # 简历分析智能体
├── output/                         # 输出目录
├── static/                         # 静态文件
├── uploads/                        # 上传文件
├── pyproject.toml                  # 项目依赖
└── README.md                       # 本文件
```

## 🛠️ 安装

### 前提条件
- Python 3.12或更高版本
- UV包管理器(推荐)

### 设置

1. **克隆仓库**
   ```bash
   git clone <repository-url>
   cd CareerFlow-AI
   ```

2. **安装依赖**
   ```bash
   uv sync
   ```

3. **设置环境变量**
   ```bash
   # 创建.env文件并添加API密钥
   echo "DEEPSEEK_API_KEY=your_openai_key_here" > .env
   ```

## 🚀 快速开始

```bash
python -m http.server 12800  --directory static
uv run adk web
```

## 🤖 智能体工作流程

1. **数据处理**
   - 加载和分析职位数据
   - 处理简历信息

2. **分析阶段**
   - 执行市场分析
   - 生成职位推荐

3. **报告生成**
   - 编译所有发现
   - 生成综合报告

4. **简历修改**
   - 分析用户简历
   - 生成优化建议

## 📝 依赖

主要依赖包括:
- `google-adk>=1.5.0` - Google智能体开发工具包
- `litellm>=1.73.1` - LLM抽象层
- `pandas>=2.3.0` - 数据处理
- `pydantic>=2.11.7` - 数据验证
