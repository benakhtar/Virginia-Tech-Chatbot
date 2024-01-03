import gradio as gr
import pandas as pd
import numpy as np

# Global variable to store the DataFrame
df = None
# Global variable to keep track of the current row index
current_row = 0


def load_csv(file):
    global df
    global current_row
    # import the csv and set the data types to be int, string, string, string, string, string, string
    df = pd.read_csv(file.name, dtype={"id": int, "question": str, "answer": str})
    if "label" not in df.columns:
        df["label"] = None
    current_row = 0
    row_dict = df.iloc[current_row].to_dict()
    return row_dict["id"], row_dict["question"], row_dict["answer"], row_dict["label"]


def annotate_row_0():
    global df
    global current_row

    df.at[current_row, "label"] = 0

    if current_row < len(df) - 1:
        current_row += 1
    else:
        current_row = 0
    df.to_csv("annotated_data.csv", index=False)

    row_dict = df.iloc[current_row].to_dict()
    return row_dict["id"], row_dict["question"], row_dict["answer"], row_dict["label"], "annotated_data.csv"

def annotate_row_1():
    global df
    global current_row

    df.at[current_row, "label"] = 1

    if current_row < len(df) - 1:
        current_row += 1
    else:
        current_row = 0
    df.to_csv("annotated_data.csv", index=False)

    row_dict = df.iloc[current_row].to_dict()
    return row_dict["id"], row_dict["question"], row_dict["answer"], row_dict["label"], "annotated_data.csv"


def navigate(direction):
    global current_row
    if direction == "Previous":
        current_row = max(0, current_row - 1)
    elif direction == "Next":
        current_row = min(len(df) - 1, current_row + 1)
    elif direction == "First Unlabeled":
        unlabeled_row = df[df["label"].isna()].index.min()
        if not np.isnan(unlabeled_row):
            current_row = int(unlabeled_row)

    row_dict = df.iloc[current_row].to_dict()
    return row_dict["id"], row_dict["question"], row_dict["answer"], row_dict["label"]


with gr.Blocks(theme=gr.themes.Soft()) as annotator:
    gr.Markdown("## Data Annotation")

    with gr.Row():
        gr.Markdown("### Upload CSV")
        file_upload = gr.File()
        btn_load = gr.Button("Load CSV")

    with gr.Row():
        gr.Markdown("### Current Row")
        with gr.Row():
            idx = gr.Number(label="Index")
            Q = gr.Textbox(label="Question")
            A = gr.Textbox(label="Answer")

        with gr.Row():
            btn_annotate_1 = gr.Button("1")
            btn_annotate_0 = gr.Button("0")
            label = gr.Textbox(label="Label")

        with gr.Row():
            btn_previous = gr.Button("Previous")
            btn_next = gr.Button("Next")
            btn_first_unlabeled = gr.Button("First Unlabeled")

    with gr.Row():
        gr.Markdown("### Annotated Data File Download")
        file_download = gr.File()

    btn_load.click(
        load_csv,
        inputs=[file_upload],
        outputs=[
            idx,
            Q,
            A,
            label,
        ],
    )
    btn_annotate_0.click(
        annotate_row_0,
        inputs=[],
        outputs=[
            idx,
            Q,
            A,
            label,
            file_download,
        ],
    )
    btn_annotate_1.click(
        annotate_row_1,
        inputs=[],
        outputs=[
            idx,
            Q,
            A,
            label,
            file_download,
        ],
    )
    btn_previous.click(
        navigate,
        inputs=gr.Textbox("Previous", visible=False),
        outputs=[
            idx,
            Q,
            A,
            label,
        ],
    )
    btn_next.click(
        navigate,
        inputs=gr.Textbox("Next", visible=False),
        outputs=[
            idx,
            Q,
            A,
            label,
        ],
    )
    btn_first_unlabeled.click(
        navigate,
        inputs=gr.Textbox("First Unlabeled", visible=False),
        outputs=[
            idx,
            Q,
            A,
            label,
        ],
    )

annotator.launch()
