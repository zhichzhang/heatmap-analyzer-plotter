# Heatmap Analyzer Plotter

This project is available in multiple languages:

- [English](README.md)
- [简体中文](README.zh-CN.md)

## Intro

This project visualizes player behavior data—collected from our team-developed game [BroCapsule](https://github.com/CSCI-526/main-team404)—by converting Excel files into time-cost heatmaps overlaid on level background images, using Seaborn and Matplotlib.

The tool supports three analysis modes:

1. Single session analysis
2. Single checkpoint in a session
3. Aggregated data across all sessions 

### Excel Columns
| Item               | Description                     |
| --------------------- | ------------------------------------- |
| `Session ID`          | Unique identifier for a game session  |
| `Level`               | Name of the game level                |
| `Checkpoint`          | Name of the checkpoint                |
| `Heatmap JSON String` | JSON string of time data per tile     | 
| `Success`             | Whether the level was completed       |
| `Completed`           | Whether the checkpoint was completed  |
| `Level width`         | Level width in pixels                 |
| `Level height`        | Level height in pixels                |
| `Ceil size`           | Side length of each heatmap cell (px) |

## File Structure

```bash
.
├── assets/                                                    # Resource files 
│   ├── Team404 Time-cost Heatmap (Responses).xlsx             # Data source Excel file 
│   └── levels/                                                # Background images folder 
│       └── {level}_Tilemap.png                                # Background image for each level
├── exports/                                                   # Exported heatmap images
├── main.py                                                    # Main Python script
├── requirements.txt                                           # Python dependencies list
└── .gitignore                                                 # Git ignore rules
```

## Usage

### Requirements

Navigate to the project root directory and run the following command to install dependencies:

```bash
pip install -r requirements.txt
```

### Run

Run the script:

```bash
python main.py
```

The program will guide you through the following steps:

1. Select a level
2. Choose a mode
   - `0`: Single session mode
   - `1`: Single session + checkpoint mode
   - `2`: All sessions mode
3. **Follow prompts** to select Session ID or Checkpoint
4. Heatmap will be saved in the `exports/` directory

## Output Sample
- Filename example： `Time-cost Heatmap (Session ID = 1, Level = L1, ...)-2025-05-18-16-45-12.png`
- Content：Background image overlaid with a heatmap where darker colors indicate higher time cost

  ![exmaple](https://github.com/zhichzhang/heatmap-analyzer-plotter/blob/main/exports/Time-cost%20Heatmap%20(All%20Sessions%2C%20Level%3DL0_tutorial_remake2)-2025-04-28-16-42-39.png)
  
- Features：
  - Logarithmic scaling for time values
  - Zero-value masking 
  - Optional hotspot annotations

## Contact

Feel free to modify or extend this project for your own analysis needs.  For questions, open an issue or contact the author. 
