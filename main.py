from datetime import datetime

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import image as mpimg
from sklearn.preprocessing import MinMaxScaler, StandardScaler
import math

level_width = 380
level_height = 44
ceil_size = 4

num_cols = math.ceil(level_width / ceil_size)
num_rows = math.ceil(level_height / ceil_size)

level = 0

EXCEL_PATH = "assets/Team404 Alpha Test Level Time Heatmap  (Responses).xlsx"

def one_session_mode():
    session_id = int(input("Select session id: ") or "0")
    global level

    df = pd.read_excel(EXCEL_PATH)

    df.columns = df.columns.str.strip()

    session_data = df[(df['Session ID'] == session_id) & (df['Level'] == level)]

    if session_data.empty:
        print(f"No data found for the specified session {session_id} and level {level}. Use default values instead.")
        session_id = 638796696694611015
        session_data = df[(df['Session ID'] == session_id) & (df['Level'] == level)]
        print(f"Use session id {session_id} and level {level}.")
    else:
        print(f"Data for the specified session {session_id} and level {level} has been found. Generating time-cost heatmap...")


    isCompleted = all(session_data['Completed'].unique())
    session_data = session_data[['Ceil row index', 'Ceil column index', 'Time spent on the ceil']]
    title = f"Time-cost Heatmap (Session ID = {session_id}, Level = {level}, Level Completed = {isCompleted})"

    pivot_table = session_data.pivot_table(
        index='Ceil row index',
        columns='Ceil column index',
        values='Time spent on the ceil',
        aggfunc='sum',
        fill_value=0
    )

    pivot_table = pivot_table.reindex(index=range(num_rows), columns=range(num_cols), fill_value=0)

    draw(title, pivot_table)

def one_session_one_checkpoint_mode():
    session_id = int(input("Select session id: ") or "0")
    checkpoint = int(input("Select checkpoint index: ") or "1")
    global level

    df = pd.read_excel(EXCEL_PATH)

    df.columns = df.columns.str.strip()

    checkpoint_data = df[(df['Session ID'] == session_id) & (df['Level'] == level) & (df['Checkpoint'] == checkpoint)]
    if checkpoint_data.empty:
        print(f"No data found for the specified session {session_id}, level {level}, and checkpoint {checkpoint}. Use default values instead.")
        session_id = 638796696694611015
        checkpoint = 1
        checkpoint_data = df[(df['Session ID'] == session_id) & (df['Level'] == level) & (df['Checkpoint'] == checkpoint)]
        print(f"Use the specified session {session_id}, level {level}, and checkpoint {checkpoint}.")
    else:
        print(f"Data for the specified session {session_id}, level {level}, and checkpoint {checkpoint} has been found. Generating time-cost heatmap...")

    isCompleted = all(checkpoint_data['Completed'].unique())
    checkpoint_data = checkpoint_data[['Ceil row index', 'Ceil column index', 'Time spent on the ceil']]
    title = f"Time-cost Heatmap (Session ID = {session_id}, Level = {level}, Checkpoint = {checkpoint}, Checkpoint Completed = {isCompleted})"

    pivot_table = checkpoint_data.pivot_table(
        index='Ceil row index',
        columns='Ceil column index',
        values='Time spent on the ceil',
        aggfunc='sum',
        fill_value=0
    )

    pivot_table = pivot_table.reindex(index=range(num_rows), columns=range(num_cols), fill_value=0)

    draw(title, pivot_table)

def all_sessions_mode():
    global level

    title = f"Time-cost Heatmap (All Sessions, Level={level})"
    df = pd.read_excel(EXCEL_PATH)
    df.columns = df.columns.str.strip()
    level_data = df[df['Level'] == level]
    grouped_data = level_data.groupby('Session ID')
    final_data = pd.DataFrame()

    for session_id, group in grouped_data:
        session_data = group[['Ceil row index', 'Ceil column index', 'Time spent on the ceil']]

        pivot_table = session_data.pivot_table(
            index='Ceil row index',
            columns='Ceil column index',
            values='Time spent on the ceil',
            aggfunc='sum',
            fill_value=0
        )

        pivot_table = pivot_table.reindex(index=range(num_rows), columns=range(num_cols), fill_value=0)

        scaler = MinMaxScaler()
        normalized = scaler.fit_transform(pivot_table)
        normalized_df = pd.DataFrame(normalized, index=pivot_table.index, columns=pivot_table.columns)

        if final_data.empty:
            final_data = normalized_df
        else:
            final_data += normalized_df

    draw(title, final_data)

def draw(title, table):
    scalar = MinMaxScaler()
    normalized = scalar.fit_transform(table)
    normalized_df = pd.DataFrame(normalized, index=table.index, columns=table.columns)

    fig_width = len(normalized_df.columns) * 0.70
    fig_height = len(normalized_df.index) * 0.85

    plt.figure(figsize=(fig_width, fig_height), dpi=100)

    background_img = mpimg.imread('assets/level-0.png')

    plt.imshow(background_img, aspect='auto', extent=[0, len(normalized_df.columns), 0, len(normalized_df.index)], origin='upper')

    ax = sns.heatmap(
        normalized_df,
        cmap="coolwarm",
        annot=True,
        linewidths=0.05,
        linecolor='gray',
        cbar=False,
        square=True,
        alpha=0.6,
        xticklabels=True,
        yticklabels=True,
        cbar_kws={"orientation": "horizontal", "pad": 0.1}
    )

    plt.title(title, fontsize=20, fontweight='bold', pad=20, fontname='Arial')
    ax.set_xlabel("Ceil Column Index", fontsize=16, fontweight='bold', fontname='Arial')
    ax.xaxis.set_label_position('bottom')  # 标签移上
    ax.xaxis.tick_top()
    ax.xaxis.set_label_coords(0.5, -0.06)
    plt.ylabel("Ceil Row Index", fontsize=16, fontweight='bold', fontname='Arial')

    plt.gca().xaxis.set_ticks_position('bottom')

    plt.tight_layout()

    plt.savefig(f"exports/{title}-{ datetime.now().strftime("%Y-%m-%d-%H-%M-%S")}.png", dpi=100)
    print(f"{title}.png has been generated.")
    plt.show()

def init():
    global level

    level = int(input("Select level index (or input -1 to exit): ") or "0")
    df = pd.read_excel(EXCEL_PATH)
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
            print("Initialization failed. Exit.")
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