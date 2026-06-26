import os
import tempfile

import gradio as gr

from services.model_service import ModelService

MAX_FILE_SIZE = 100 * 1024 * 1024  # 100 MB


# -----------------------------------------------------------------------------
# Upload Audio
# -----------------------------------------------------------------------------
def process_audio(audio_file, state):
    if audio_file is None:
        return (
            state,
            "",
            [],
            gr.Tabs(visible=False),
        )

    if os.path.getsize(audio_file) > MAX_FILE_SIZE:
        raise gr.Error("Please upload an audio file smaller than 100 MB.")

    filename = os.path.basename(audio_file)

    if (
        state is not None
        and state.get("uploaded_file_name") == filename
    ):
        return (
            state,
            state["summary"],
            [],
            gr.Tabs(
                visible=True,
                selected=0,
            ),
        )

    suffix = os.path.splitext(filename)[1]

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=suffix,
    ) as temp_file:

        with open(audio_file, "rb") as f:
            temp_file.write(f.read())

        temp_path = temp_file.name

    try:
        model_service = ModelService(temp_path)
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

    state = {
        "model_service": model_service,
        "summary": "",
        "summary_generated": False,
        "uploaded_file_name": filename,
    }

    return (
        state,
        "### ⏳ Generating summary...",
        [],
        gr.Tabs(
            visible=True,
            selected=0,
        ),
    )


# -----------------------------------------------------------------------------
# Summary Generator
# -----------------------------------------------------------------------------
def generate_summary(state):
    if state is None:
        yield ""
        return

    if state["summary_generated"]:
        yield state["summary"]
        return

    summary = ""

    for chunk in state["model_service"].summarize():
        summary = chunk
        yield summary

    state["summary"] = summary
    state["summary_generated"] = True


# -----------------------------------------------------------------------------
# Chat
# -----------------------------------------------------------------------------
def chat(message, history, state):
    if state is None:
        raise gr.Error("Please upload an audio file first.")

    response = ""

    for chunk in state["model_service"].chat(message, history):
        response = chunk
        yield response


# -----------------------------------------------------------------------------
# UI
# -----------------------------------------------------------------------------
with gr.Blocks(title="AI Meeting Assistant") as demo:

    gr.Markdown("# 🎙️ AI Meeting Assistant")
    gr.Markdown(
        "Upload a meeting recording to automatically generate a summary and chat with the transcript."
    )

    state = gr.State(None)

    audio = gr.File(
        label="Upload Audio",
        file_types=[".mp3", ".wav", ".m4a"],
        type="filepath",
    )

    with gr.Tabs() as tabs:

        with gr.Tab("📝 Meeting Summary"):
            summary_box = gr.Markdown(
                "Upload an audio file to begin."
            )

        with gr.Tab("💬 Chat with Meeting"):

            chatbot = gr.Chatbot(
                type="messages",
                height=500,
            )

            gr.ChatInterface(
                fn=chat,
                chatbot=chatbot,
                additional_inputs=[state],
                type="messages",
            )

    (
        audio.upload(
            fn=process_audio,
            inputs=[audio, state],
            outputs=[
                state,
                summary_box,
                chatbot,
                tabs,
            ],
        )
        .then(
            fn=generate_summary,
            inputs=state,
            outputs=summary_box,
            show_progress="minimal",
        )
    )

demo.launch()
