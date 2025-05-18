# Heatmap Analyzer Plotter

## Intro / 介绍

本项目用于将收集到的玩家行为数据从 Excel 文件中可视化为对应的时间消耗热力图，并叠加在关卡背景图上，绘图使用 Seaborn 和 Matplotlib 实现。 

This project visualizes collected player behavior data from Excel files into corresponding time-cost heatmaps, overlaid on level background images, using Seaborn and Matplotlib. 

工具支持以下三种分析模式： 

The tool supports three analysis modes:

1. **Single session analysis** / 单次会话分析
2. **Single checkpoint in a session** / 会话中单个检查点分析
3. **Aggregated data across all sessions** / 所有关卡会话数据汇总分析

### Excel Columns / Excel 字段示例
| Column                | Description (EN)                      | 描述（中文）                     |
| --------------------- | ------------------------------------- | -------------------------------- |
| `Session ID`          | Unique identifier for a game session  | 会话 ID                          |
| `Level`               | Name of the game level                | 关卡名称                         |
| `Checkpoint`          | Name of the checkpoint                | 检查点名称                       |
| `Heatmap JSON String` | JSON string of time data per tile     | 每个单元格的耗时数据 JSON 字符串 |
| `Success`             | Whether the level was completed       | 是否完成整个关卡                 |
| `Completed`           | Whether the checkpoint was completed  | 是否完成该检查点                 |
| `Level width`         | Level width in pixels                 | 关卡宽度（px）                   |
| `Level height`        | Level height in pixels                | 关卡高度（px）                   |
| `Ceil size`           | Side length of each heatmap cell (px) | 热力图单元格边长（px）           |

## File Structure / 文件结构

```bash
.
├── assets/                                                    # Resource files / 资源文件夹
│   ├── Team404 Time-cost Heatmap (Responses).xlsx             # Data source Excel file / 数据源 Excel 文件
│   └── levels/                                                # Background images folder / 背景图文件夹
│       └── {level}_Tilemap.png                                # Background image for each level / 每个关卡的背景图
├── exports/                                                   # Exported heatmap images / 输出生成的热力图图像
├── main.py                                                    # Main Python script / 主程序脚本
├── requirements.txt                                           # Python dependencies list / Python 依赖列表
└── .gitignore                                                 # Git ignore rules / Git 忽略文件配置
```

##Usage / 使用方法

### Requirements / 环境依赖

进入项目根目录后运行以下命令安装依赖：

Navigate to the project root directory and run the following command to install dependencies:

```bash
pip install -r requirements.txt
```

### Run / 运行

运行主程序：

Run the script:

```bash
python main.py
```

The program will guide you through the following steps:
程序将引导你完成以下步骤：

1. **Select a level** / 选择关卡
2. **Choose a mode** / 选择分析模式
   - `0`: Single session mode / 单次会话模式
   - `1`: Single session + checkpoint mode / 单次会话 + 指定检查点
   - `2`: All sessions mode / 所有会话汇总模式
3. **Follow prompts** to select Session ID or Checkpoint / 按提示选择会话 ID 和检查点
4. Heatmap will be saved in the `exports/` directory
    生成的热力图将保存至 `exports/` 目录

## Output Sample / 输出示例

- **Filename example** / 文件名示例： `Time-cost Heatmap (Session ID = 1, Level = L1, ...)-2025-05-18-16-45-12.png`

- **Content** / 内容：

  Background image overlaid with a heatmap where darker colors indicate higher time cost

  热力图叠加在关卡背景图上，颜色深浅表示耗时高低

- **Features** / 特性：

  - Logarithmic scaling for time values / 时间值对数缩放
  - Zero-value masking / 零值遮罩
  - Optional hotspot annotations / 支持热区注释

## Contact / 联系方式

欢迎根据需要修改或扩展本项目。如有疑问请提交 Issue 或联系作者。 

Feel free to modify or extend this project for your own analysis needs.  For questions, open an issue or contact the author. 