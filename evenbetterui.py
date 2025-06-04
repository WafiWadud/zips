from nicegui import ui
import shutil
import os
import tempfile

# Global variables to store paths
uploaded_files = []
output_filename = None


def handle_upload(e):
    global uploaded_files

    try:
        # e.content is the file content, e.name is the filename
        file_name = e.name
        file_content = e.content.read()

        # Store file info
        uploaded_files.append(
            {"name": file_name, "content": file_content, "size": len(file_content)}
        )

        # Update UI
        update_file_list()
        ui.notify(f"Uploaded: {file_name}", type="positive")

    except Exception as ex:
        ui.notify(f"Upload error: {str(ex)}", type="negative")
        print(f"Upload error: {ex}")


def update_file_list():
    if uploaded_files:
        file_names = [f["name"] for f in uploaded_files]
        total_size = sum(f["size"] for f in uploaded_files)
        size_mb = total_size / (1024 * 1024)

        directory_label.set_text(f"Files: {', '.join(file_names[:3])}")
        if len(file_names) > 3:
            directory_label.set_text(
                f"Files: {', '.join(file_names[:3])} and {len(file_names)-3} more"
            )

        file_count_label.set_text(f"{len(uploaded_files)} files ({size_mb:.1f} MB)")
    else:
        directory_label.set_text("No files uploaded")
        file_count_label.set_text("")


def clear_files():
    global uploaded_files
    uploaded_files = []
    update_file_list()
    ui.notify("Files cleared", type="info")


def set_output_name():
    global output_filename
    if filename := output_input.value.strip():
        # Remove .tar.gz if user added it
        if filename.endswith(".tar.gz"):
            filename = filename[:-7]
        output_filename = filename
        output_label.set_text(f"Output will be: {filename}.tar.gz")
        ui.notify("Output filename set", type="positive")
    else:
        ui.notify("Please enter a filename", type="warning")


def gzip_directory() -> None:
    global uploaded_files, output_filename

    if not uploaded_files:
        result_label.set_text("Please upload files first.")
        ui.notify("No files uploaded", type="negative")
        return

    if not output_filename:
        result_label.set_text("Please specify output filename first.")
        ui.notify("No output filename specified", type="negative")
        return

    try:
        create_archive_from_files(uploaded_files, output_filename)
    except Exception as e:
        result_label.set_text(f"Error creating archive: {str(e)}")
        ui.notify(f"Error: {str(e)}", type="negative")


def create_archive_from_files(uploaded_files, output_filename):
    # Create a temporary directory and write all files
    temp_dir = tempfile.mkdtemp()

    for file_info in uploaded_files:
        file_path = os.path.join(temp_dir, file_info["name"])

        # Create subdirectories if needed
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        # Write the file
        with open(file_path, "wb") as f:
            f.write(file_info["content"])

    # Create the archive
    output_path = f"{output_filename}.tar.gz"
    shutil.make_archive(output_filename, "gztar", temp_dir)

    # Clean up temp directory
    shutil.rmtree(temp_dir)

    result_label.set_text(f"Archive created successfully: {output_path}")
    ui.notify("Archive created successfully!", type="positive")

    # Show download info
    if os.path.exists(output_path):
        download_info.set_text(f"Archive saved as: {os.path.abspath(output_path)}")
        download_info.set_visibility(True)


# Create the UI
with ui.column().classes("mx-auto max-w-2xl p-4"):
    ui.label("Directory Compression Tool").classes("text-2xl font-bold mb-4")

    # File upload section
    with ui.card().classes("w-full p-4 mb-4"):
        ui.label("1. Upload Files").classes("text-lg font-semibold mb-2")

        with ui.row().classes("w-full items-center gap-2 mb-2"):
            upload = (
                ui.upload(multiple=True, on_upload=handle_upload, auto_upload=True)
                .props('accept="*" color="primary"')
                .classes("flex-grow")
            )

            ui.button("Clear Files", on_click=clear_files).props(
                'color="negative" outline'
            )

        directory_label = ui.label("No files uploaded").classes("text-sm text-gray-600")
        file_count_label = ui.label("").classes("text-xs text-gray-500")

    # Output filename section
    with ui.card().classes("w-full p-4 mb-4"):
        ui.label("2. Set Output Filename").classes("text-lg font-semibold mb-2")
        with ui.row().classes("w-full gap-2"):
            output_input = ui.input(
                label="Archive name", placeholder="my_archive", value="archive"
            ).classes("flex-grow")
            ui.button("Set Name", on_click=set_output_name).props("color=secondary")
        output_label = ui.label("Output: archive.tar.gz").classes(
            "text-sm text-gray-600 mt-2"
        )

    # Create archive section
    with ui.card().classes("w-full p-4 mb-4"):
        ui.label("3. Create Archive").classes("text-lg font-semibold mb-2")
        ui.button("Create GZip Archive", on_click=gzip_directory).props(
            "color=primary size=lg"
        ).classes("w-full")

    # Result display
    with ui.card().classes("w-full p-4"):
        ui.label("Result").classes("text-lg font-semibold mb-2")
        result_label = ui.label("Ready to create archive...").classes("text-sm mb-2")
        download_info = ui.label("").classes("text-xs text-green-600 hidden")

# Instructions
with ui.card().classes("mx-auto max-w-2xl p-4 mt-4 bg-blue-50"):
    ui.label("Instructions:").classes("font-semibold text-blue-800 mb-2")
    with ui.column().classes("text-sm text-blue-700"):
        ui.label('• Click "Browse" to select multiple files')
        ui.label("• You can upload files one by one or select multiple at once")
        ui.label("• Files will be compressed maintaining their original names")
        ui.label("• Enter a name for your archive file")
        ui.label('• Click "Create GZip Archive" to compress all uploaded files')
        ui.label("• The archive will be saved in the same directory as this script")

ui.run(native=True, reload=False)
