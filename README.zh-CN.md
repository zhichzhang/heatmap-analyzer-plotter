# 热力图分析器绘图工具

## 介绍

本项目用于将收集到的玩家行为数据从 Excel 文件中可视化为对应的时间消耗热力图，并叠加在关卡背景图上，绘图使用 Seaborn 和 Matplotlib 实现。 

工具支持以下三种分析模式：  

1. 单次会话分析
2. 会话中单个检查点分析
3. 所有关卡会话数据汇总分析

### 字段示例
| 项目               | 描述（中文）                     |
| --------------------- | ------------------------------  |
| `Session ID`          | 会话 ID                          |
| `Level`               | 关卡名称                         |
| `Checkpoint`          | 检查点名称                       |
| `Heatmap JSON String` | 每个单元格的耗时数据 JSON 字符串 |
| `Success`             | 是否完成整个关卡                 |
| `Completed`           | 是否完成该检查点                 |
| `Level width`         | 关卡宽度（px）                   |
| `Level height`        | 关卡高度（px）                   |
| `Ceil size`           | S热力图单元格边长（px）           |

## 文件结构

```bash
.
├── assets/                                                    # 资源文件夹
│   ├── Team404 Time-cost Heatmap (Responses).xlsx             # 数据源 Excel 文件
│   └── levels/                                                # 背景图文件夹
│       └── {level}_Tilemap.png                                # 每个关卡的背景图
├── exports/                                                   # 输出生成的热力图图像
├── main.py                                                    # 主程序脚本
├── requirements.txt                                           # Python 依赖列表
└── .gitignore                                                 # Git 忽略文件配置
```

## 使用方法

### 环境依赖

进入项目根目录后运行以下命令安装依赖：

```bash
pip install -r requirements.txt
```

### 运行

运行主程序：

```bash
python main.py
```

程序将引导你完成以下步骤：

1. 选择关卡
2. 选择分析模式
   - `0`: 单次会话模式
   - `1`: 单次会话 + 指定检查点
   - `2`: 所有会话汇总模式
3. 按提示选择会话 ID 和检查点
4. 生成的热力图将保存至 `exports/` 目录

## 输出示例

- 文件名示例： `Time-cost Heatmap (Session ID = 1, Level = L1, ...)-2025-05-18-16-45-12.png`

- 内容：热力图叠加在关卡背景图上，颜色深浅表示耗时高低

  ![exmaple](https://github.com/zhichzhang/heatmap-analyzer-plotter/blob/main/exports/Time-cost%20Heatmap%20(All%20Sessions%2C%20Level%3DL0_tutorial_remake2)-2025-04-28-16-42-39.png)

- 特性：
  - 时间值对数缩放
  - 零值遮罩
  - 支持热区注释

## 联系方式

欢迎根据需要修改或扩展本项目。如有疑问请提交 Issue 或联系作者。 
