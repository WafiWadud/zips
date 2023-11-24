import tarfile
from gi.repository import Gtk, Gio


class ZipApp(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Zip Files")
        self.set_border_width(10)

        button = Gtk.Button(label="Zip Files")
        button.connect("clicked", self.on_button_clicked)
        self.add(button)

    def on_button_clicked(self, widget):
        dialog = Gtk.FileChooserDialog(
            title="Select Directory to Zip",
            action=Gtk.FileChooserAction.SELECT_FOLDER,
        )
        dialog.add_buttons(
            Gtk.STOCK_CANCEL,
            Gtk.ResponseType.CANCEL,
            "Select",
            Gtk.ResponseType.OK,
        )

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            self.gzip_files(dialog.get_filename())
        dialog.destroy()

    def gzip_files(self, input_dir):
        dialog = Gtk.FileChooserDialog(
            title="Save GZip File",
            action=Gtk.FileChooserAction.SAVE,
        )
        dialog.add_buttons(
            Gtk.STOCK_CANCEL,
            Gtk.ResponseType.CANCEL,
            Gtk.STOCK_SAVE,
            Gtk.ResponseType.OK,
        )
        dialog.set_do_overwrite_confirmation(True)
        dialog.set_current_name("archive.tar.gz")

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            self.gzip_dir(input_dir, dialog.get_filename())
        dialog.destroy()

    def gzip_dir(self, input_dir, output_gz):
        with tarfile.open(output_gz, 'w:gz') as tar:
            tar.add(input_dir, arcname='')


win = ZipApp()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
