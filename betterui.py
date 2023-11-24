from nicegui import ui
import shutil
import os

def gzip_directory() -> None:
    dir_to_zip: str = directory.value
    output_filename: str = output.value
    if not os.path.isdir(dir_to_zip):
        result.value = f"{dir_to_zip} is not a directory."
        return
    shutil.make_archive(output_filename, 'gztar', dir_to_zip)
    result.set_text(f"Directory {dir_to_zip} has been gzipped successfully!")

result = ui.label(text='')
directory = ui.input(label='Enter directory to gzip')
output = ui.input(label='Enter output filename')
ui.button(text='Gzip Directory', on_click=gzip_directory)

ui.run(native=True)