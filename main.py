from datetime import datetime
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import image as mpimg
import math
import json

level_width = 380
level_height = 44
ceil_size = 4

num_cols = math.ceil(level_width / ceil_size)
num_rows = math.ceil(level_height / ceil_size)

# levels = []
level = ""

checkpoints = []

EXCEL_PATH = "assets/Team404 Time-cost Heatmap (Responses).xlsx"


def get_heatmap_records(data):
    heatmap_records = []

    for json_str in data['Heatmap JSON String']:
        data_obj = json.loads(json_str)
        ceil_data_list = data_obj.get('ceilDataList', [])
        for entry in ceil_data_list:
            heatmap_records.append({
                'Ceil row index': entry['ceilRowIndex'],
                'Ceil column index': entry['ceilColIndex'],
                'Time spent on the ceil': entry['time']
            })

    heatmap_records = pd.DataFrame(heatmap_records)

    return heatmap_records

def one_session_mode():
    session_id = int(input("Select session id: ") or "0")
    global level

    background_img_path = f"assets/levels/{level}_Tilemap.png"
    df = pd.read_excel(EXCEL_PATH)

    df.columns = df.columns.str.strip()

    session_data = df[(df['Session ID'] == session_id) & (df['Level'] == level)]

    if session_data.empty:
        print(f"No data found for the specified session {session_id} and level {level}.")
        print("Exit.")
        return
    else:
        print(f"Data for the specified session {session_id} and level {level} has been found. Generating time-cost heatmap...")


    success = any(session_data['Success'].unique())

    session_data = get_heatmap_records(session_data)
    title = f"Time-cost Heatmap (Session ID = {session_id}, Level = {level}, Success = {success})"

    pivot_table = session_data.pivot_table(
        index='Ceil row index',
        columns='Ceil column index',
        values='Time spent on the ceil',
        aggfunc='sum',
        fill_value=0
    )

    pivot_table = pivot_table.reindex(index=range(num_rows), columns=range(num_cols), fill_value=0)

    draw(title, pivot_table, background_img_path)

def one_session_one_checkpoint_mode():
    session_id = int(input("Select session id: ") or "0")

    global level
    background_img_path = f"assets/levels/{level}_Tilemap.png"

    wannaExit = False
    df = pd.read_excel(EXCEL_PATH)

    df.columns = df.columns.str.strip()

    session_data = df[(df['Session ID'] == session_id) & (df['Level'] == level)]
    if session_data.empty:
        print(f"No data found for the specified session {session_id} and level {level}.")
        print("Exit.")
        return
    else:
        checkpoints_set = session_data['Checkpoint'].unique()
        while True:
            print("Available Checkpoints:")

            for i, checkpoint in enumerate(checkpoints_set, 1):
                print(f"{i}. Checkpoint {checkpoint}")

            selected_checkpoint_index = int(input("Select a checkpoint by entering the corresponding number or input -1 to exit: ")) - 1

            if 0 <= selected_checkpoint_index < len(checkpoints_set):
                checkpoint = checkpoints_set[selected_checkpoint_index]
                break
            elif selected_checkpoint_index < 0:
                wannaExit = True
                print("Exit.")
                break
            else:
                print(f"No such checkpoint {selected_checkpoint_index}. Please enter a valid checkpoint number.")
                continue
        if wannaExit:
            return

    checkpoint_data = session_data[session_data['Checkpoint'] == checkpoint]
    print(f"Data for the specified session {session_id}, level {level}, and checkpoint {checkpoint} has been found. Generating time-cost heatmap...")

    success = any(checkpoint_data['Success'].unique())
    completed = bool(checkpoint_data['Completed'].iloc[0])
    checkpoint_data = get_heatmap_records(checkpoint_data)
    title = f"Time-cost Heatmap (Session ID = {session_id}, Level = {level}, Checkpoint = {checkpoint}, Completed = {completed}, Success = {success})"

    pivot_table = checkpoint_data.pivot_table(
        index='Ceil row index',
        columns='Ceil column index',
        values='Time spent on the ceil',
        aggfunc='sum',
        fill_value=0
    )

    pivot_table = pivot_table.reindex(index=range(num_rows), columns=range(num_cols), fill_value=0)

    draw(title, pivot_table, background_img_path)

def all_sessions_mode():
    global level

    title = f"Time-cost Heatmap (All Sessions, Level={level})"
    background_img_path = f"assets/levels/{level}_Tilemap.png"
    df = pd.read_excel(EXCEL_PATH)

    df.columns = df.columns.str.strip()
    level_data = df[df['Level'] == level]
    grouped_data = level_data.groupby('Session ID')
    final_data = pd.DataFrame()

    for session_id, group in grouped_data:
        session_data = get_heatmap_records(group)
        pivot_table = session_data.pivot_table(
            index='Ceil row index',
            columns='Ceil column index',
            values='Time spent on the ceil',
            aggfunc='sum',
            fill_value=0
        )
        pivot_table = pivot_table.reindex(index=range(num_rows), columns=range(num_cols), fill_value=0)

        if final_data.empty:
            final_data = pivot_table
        else:
            final_data += pivot_table

    draw(title, final_data, background_img_path)


def draw(title, table, background_img_path):
    table_log_transformed = np.log1p(table)

    normalized_df = pd.DataFrame(table_log_transformed, index=table.index, columns=table.columns)

    fig_width = len(normalized_df.columns) * 0.70
    fig_height = len(normalized_df.index) * 0.85

    plt.figure(figsize=(fig_width, fig_height), dpi=100)

    background_img = mpimg.imread(background_img_path)
    # print(background_img.shape)

    bg_height, bg_width, _ = background_img.shape
    required_width = len(normalized_df.columns)
    required_height = len(normalized_df.index)

    width_diff = math.ceil(bg_width / required_width) * required_width - bg_width
    height_diff = math.ceil(bg_height / required_height) * required_height - bg_height

    padding_right = width_diff if width_diff > 0 else 0
    padding_bottom = height_diff if height_diff > 0 else 0

    padded_bg = np.pad(background_img,
                       ((0, padding_bottom), (0, padding_right), (0, 0)),
                       mode='constant',
                       constant_values=(0, 0))

    plt.imshow(padded_bg, interpolation='bilinear', aspect='auto', zorder=0,
               extent=(0.0, required_width, 0.0, required_height), origin='lower')

    mask = normalized_df == 0

    ax = sns.heatmap(
        normalized_df,
        cmap="coolwarm",
        annot=True,
        linewidths=0.05,
        linecolor='gray',
        cbar=False,
        square=True,
        alpha=0.9,
        mask=mask,
        xticklabels=True,
        yticklabels=True,
        cbar_kws={"orientation": "horizontal", "pad": 0.1}
    )

    plt.title(title, fontsize=32, fontweight='bold', pad=20, fontname='Arial')
    ax.set_xlabel("Ceil Column Index", fontsize=20, fontweight='bold', fontname='Arial')
    ax.xaxis.set_label_position('bottom')  # 标签移上
    ax.xaxis.tick_top()
    ax.xaxis.set_label_coords(0.5, -0.03)
    plt.ylabel("Ceil Row Index", fontsize=20, fontweight='bold', fontname='Arial')
    plt.tick_params(axis='both', labelsize=16, width=2)
    plt.gca().xaxis.set_ticks_position('bottom')

    plt.tight_layout()

    plt.savefig(f"exports/{title}-{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.png", dpi=100)
    print(f"{title}.png has been generated.")

    plt.show()

def init():
    global level

    df = pd.read_excel(EXCEL_PATH)
    while True:
        print("Available levels:")

        levels_set = df['Level'].unique()
        for i, level_name in enumerate(levels_set, 1):
            print(f"{i}. Checkpoint {level_name}")
        level_index = int(input(f"Select a level by entering the corresponding number or or input -1 to exit: ")) - 1

        if 0 <= level_index < len(levels_set):
            level = levels_set[level_index]
            break
        elif level_index < 0:
            print("Exit.")
            return False
        else:
            print(f"No such level {level_index}. Please enter a valid level number.")
            continue

    level_data = df[df['Level'] == level]

    if level_data.empty:
        print(f"No data found for the specified level {level}.")
        return False
    else:
        print(f"Data for the specified level {level} has been found. Initializing...")
        global level_width, level_height, ceil_size, num_cols, num_rows
        level_width = int(level_data['Level width'].unique()[0])
        level_height = int(level_data['Level height'].unique()[0])
        ceil_size = int(level_data['Ceil size'].unique()[0])
        num_cols = math.ceil(level_width / ceil_size)
        num_rows = math.ceil(level_height / ceil_size)
        print(f"Level: {level}")
        print(f"Width: {level_width} px")
        print(f"Height: {level_height} px")
        print(f'Ceil size: {ceil_size} px')
        print(f"Number of columns: {num_cols}")
        print(f"Number of rows: {num_rows}")
        print(f"Initialization completed.")
        return True

if __name__ == '__main__':
    while True:
        print("-" * 50)
        if not init():
            print("Initialization failed.")
            print("Exit.")
            break
        choose_mode = int(input("Choose Mode (0: one session, 1: one checkpoint, 2: all session, other: exit): ") or "0")
        if choose_mode == 0:
            one_session_mode()
        elif choose_mode == 1:
            one_session_one_checkpoint_mode()
        elif choose_mode == 2:
            all_sessions_mode()
        else:
            break