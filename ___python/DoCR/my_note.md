# windows-only 微调一览

## 第一部分

首先, 采用 `uv` 管理依赖

为此, 需要安装 `uv`

```shell
# 测试可行性
powershell -c "irm https://astral.sh/uv/install.ps1 | more"
# 进行安装
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

<details>
<summary>
如果需要卸载请点此展开
</summary>

清理存储的数据（可选）：

```shell
uv cache clean
rm -r "$(uv python dir)"
rm -r "$(uv tool dir)"
```

删除 uv 和 uvx 二进制文件：

```shell
$ rm $HOME\.local\bin\uv.exe
$ rm $HOME\.local\bin\uvx.exe
```

</details>

<details>
<summary>相关uv操作点此查看</summary>

[文档跳转链接](https://uv.doczh.com/getting-started/features/)

```plaintext
uv init: 创建新 Python 项目
uv add: 为项目添加依赖
uv remove: 从项目移除依赖
uv sync: 同步项目依赖到环境
uv lock: 为项目依赖创建锁文件
uv run: 在项目环境中运行命令
uv tree: 查看项目依赖树
uv build: 构建项目为分发包
uv publish: 发布项目到包索引
```

</details>

## 第二部分

### (非必要)激活虚拟环境

```shell
deactivate
conda deactivate
.venv/Scripts/Activate
```

### 安装依赖

```shell
cd DoCR
uv venv .venv
.venv\Scripts\Activate
uv pip install torch torchvision --index-url https://download.pytorch.org/whl/cu124
uv pip install -e .
```

## 第三部分

### 复现运行

```shell
# 运行Base1任务
python -m docr.training.run_training --yaml config/mytest_base1.yaml

# 运行Base2任务
python -m docr.training.run_training --yaml config/mytest_base2.yaml

# 运行Base3任务
python -m docr.training.run_training --yaml config/mytest_base3.yaml
```
