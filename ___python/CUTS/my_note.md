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
uv sync
```

> !由于win平台特性, 不想一个个去改了, 此处暂时仅保留一条完整的流程

### 复现运行:

**Data Provided**

For data, please see https://github.com/ChenLiu-1996/CUTS/tree/main/data.

The entire dataset can also be downloaded from [Huggingface](https://huggingface.co/datasets/ChenLiu1996/CUTS).

**To reproduce the results in the paper.**

The following commands are using `retina_seed2` as an example (retina dataset, random seed set to 2022).

<details>
  <summary>Unzip data</summary>

```
cd ./data/
unzip retina.zip
```
</details>

<details>
  <summary>Activate environment</summary>

```
conda activate cuts
```
</details>

<details>
  <summary><b>Stage 1.</b> Training the convolutional encoder</summary>

#### To train a model.
```
## Under `src`
python main.py --mode train --config ../config/retina_seed2.yaml
```
#### To test a model (automatically done during `train` mode).
```
## Under `src`
python main.py --mode test --config ../config/retina_seed2.yaml
```
</details>

<details>
  <summary>(Optional) [Comparison] Training a supervised model</summary>

```
## Under `src/`
python main_supervised.py --mode train --config ../retina_seed2.yaml
```
</details>

<details>
  <summary>(Optional) [Comparison] Training other models</summary>

#### To train STEGO.
```
## Under `comparison/STEGO/CUTS_scripts/`
python step01_prepare_data.py --config ../../../config/retina_seed2.yaml
python step02_precompute_knns.py --train-config ./train_config/train_config_retina_seed2.yaml
python step03_train_segmentation.py --train-config ./train_config/train_config_retina_seed2.yaml
python step04_produce_results.py --config ../../../config/retina_seed2.yaml --eval-config ./eval_config/eval_config_retina_seed2.yaml
```

#### To train Differentiable Feature Clustering (DFC).
```
## Under `comparison/DFC/CUTS_scripts/`
python step01_produce_results.py --config ../../../config/retina_seed2.yaml
```

#### To use Segment Anything Model (SAM).
```
## Under `comparison/SAM/`
mkdir SAM_checkpoint && cd SAM_checkpoint
wget https://dl.fbaipublicfiles.com/segment_anything/sam_vit_h_4b8939.pth

## Under `comparison/SAM/CUTS_scripts/`
python step01_produce_results.py --config ../../../config/retina_seed2.yaml
```

#### To use MedSAM.
```
## Under `comparison/MedSAM/`
mkdir MedSAM_checkpoint && cd MedSAM_checkpoint
download from https://drive.google.com/file/d/1ARiB5RkSsWmAB_8mqWnwDF8ZKTtFwsjl/view

## Under `comparison/SAM_Med2D/CUTS_scripts/`
python step01_produce_results.py --config ../../../config/retina_seed2.yaml
```

#### To use SAM-Med2D.
```
## Under `comparison/SAM_Med2D/`
mkdir SAM_Med2D_checkpoint && cd SAM_Med2D_checkpoint
download from https://drive.google.com/file/d/1ARiB5RkSsWmAB_8mqWnwDF8ZKTtFwsjl/view

## Under `comparison/SAM_Med2D/CUTS_scripts/`
python step01_produce_results.py --config ../../../config/retina_seed2.yaml
```
</details>


<details>
  <summary><b>Stage 2.</b> Results Generation</summary>

#### To generate and save the segmentation using spectral k-means.
```
## Under `src/scripts_analysis`
python generate_kmeans.py --config ../../config/retina_seed2.yaml
```
#### To generate and save the segmentation using diffusion condensation.
```
## Under `src/scripts_analysis`
python generate_diffusion.py --config ../../config/retina_seed2.yaml
```
#### To generate and save the segmentation using baseline methods.
```
## Under `src/scripts_analysis`
python generate_baselines.py --config ../../config/retina_seed2.yaml
```
</details>

<details>
  <summary>Results Plotting</summary>

#### To reproduce the figures in the paper.
There is one single script for this purpose (previously two but we recently merged them): `plot_paper_figure_main.py`.

The `image-idx` argument shall be followed by space-separated index/indices of the images to be plotted.

Without the `--comparison` flag, the CUTS-only results will be plotted.
With the ` --comparison` flag, the side-by-side comparison against other methods will be plotted.

With the ` --grayscale` flag, the input images and reconstructed images will be plotted in grayscale.

With the `--binary` flag, the labels will be binarized using a consistent method described in the paper.

With the `--separate` flag, the labels will be displayed as separate masks. Otherwise they will be overlaid. This flag is altomatically turned on (and cannot be turned off) for multi-class segmentation cases.

```
## Under `src/scripts_analysis`

# 注意这一块配置文件名称有些许不同, 但是retina_seed2是在的, berkeley_seed2等有后缀年份信息, 运行时候需要注意

## For natural images (berkeley), multi-class segmentation.
### Diffusion condensation trajectory.
python plot_paper_figure_main.py --config ../../config/berkeley_seed2.yaml --image-idx 8 22 89
### Segmentation comparison.
python plot_paper_figure_main.py --config ../../config/berkeley_seed2.yaml --image-idx 8 22 89 --comparison --separate

## For medical images with color (retina), binary segmentation.
### Diffusion condensation trajectory.
python plot_paper_figure_main.py --config ../../config/retina_seed2.yaml --image-idx 4 7 18
### Segmentation comparison (overlay).
python plot_paper_figure_main.py --config ../../config/retina_seed2.yaml --image-idx 4 7 18 --comparison --binary
### Segmentation comparison (non-overlay).
python plot_paper_figure_main.py --config ../../config/retina_seed2.yaml --image-idx 4 7 18 --comparison --binary --separate

## For medical images without color (brain ventricles, brain tumor), binary segmentation.
### Diffusion condensation trajectory.
python plot_paper_figure_main.py --config ../../config/brain_ventricles_seed2.yaml --image-idx 35 41 88 --grayscale
### Segmentation comparison (overlay).
python plot_paper_figure_main.py --config ../../config/brain_ventricles_seed2.yaml --image-idx 35 41 88 --grayscale --comparison --binary
### Segmentation comparison (non-overlay).
python plot_paper_figure_main.py --config ../../config/brain_ventricles_seed2.yaml --image-idx 35 41 88 --grayscale --comparison --binary --separate
### Diffusion condensation trajectory.
python plot_paper_figure_main.py --config ../../config/brain_tumor_seed2.yaml --image-idx 1 25 31 --grayscale
### Segmentation comparison (overlay).
python plot_paper_figure_main.py --config ../../config/brain_tumor_seed2.yaml --image-idx 1 25 31 --grayscale --comparison --binary
### Segmentation comparison (non-overlay).
python plot_paper_figure_main.py --config ../../config/brain_tumor_seed2.yaml --image-idx 1 25 31 --grayscale --comparison --binary --separate

## We also have an option to not overlay binary segmentation.
python plot_paper_figure_main.py --config ../../config/retina_seed2.yaml --image-idx 4 7 14 --comparison --binary

```
</details>

<details>
  <summary>Results Analysis</summary>

#### To compute the quantitative metrics (single experiment).
Assuming segmentation results have already been generated and saved.
```
## Under $CUTS_ROOT/src/scripts_analysis
python run_metrics.py --config ../../config/retina_seed2.yaml
```

#### To compute the quantitative metrics (multiple experiments).
Assuming segmentation results have already been generated and saved.
```
## Under $CUTS_ROOT/src/scripts_analysis
python run_metrics.py --config ../../config/retina_seed1.yaml ../../config/retina_seed2.yaml ../../config/retina_seed3.yaml
```

</details>

## 未完待续
