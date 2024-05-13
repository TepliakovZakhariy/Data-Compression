import tkinter
import os
from tkinter import filedialog
import tkinter.messagebox
import customtkinter
import tkinter.test
from lz78.lz78 import Codder

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("dark-blue")


class App(customtkinter.CTk):

    def __init__(self):
        super().__init__()

        self.browsed_filename = ""
        self.file_to_compress_path = ""

        # create tabview
        self.tabview = customtkinter.CTkTabview(self, width=250)
        self.tabview.pack(expand=1)
        self.tabview.add("Compress")
        self.tabview.add("Decompress")

        # first tab
        self.label_tab_compress = customtkinter.CTkLabel(
            self.tabview.tab("Compress"), text="Choose the method"
        )
        self.label_tab_compress.pack_propagate(False)
        self.label_tab_compress.pack()

        # create first frame
        self.compress_frame = customtkinter.CTkFrame(self.tabview.tab("Compress"))
        self.compress_var = tkinter.StringVar(value="")
        self.compress_frame.pack()
        self.compress_button_1 = customtkinter.CTkRadioButton(
            text="LZ78",
            master=self.compress_frame,
            variable=self.compress_var,
            value="lz78",
        )
        self.compress_button_1.pack(padx=10, pady=10)
        self.compress_button_2 = customtkinter.CTkRadioButton(
            text="Oleg2",
            master=self.compress_frame,
            variable=self.compress_var,
            value=2,
        )
        self.compress_button_2.pack(padx=10, pady=10)
        self.compress_button_3 = customtkinter.CTkRadioButton(
            text="Oleg3",
            master=self.compress_frame,
            variable=self.compress_var,
            value=3,
        )
        self.compress_button_3.pack(padx=10, pady=10)

        # create compress browse file button
        self.compress_browse_button = customtkinter.CTkButton(
            master=self.tabview.tab("Compress"),
            text="Browse File",
            fg_color="transparent",
            border_width=2,
            text_color=("gray10", "#DCE4EE"),
            command=self.BrowseFileToCompress,
        )
        self.compress_browse_button.pack(pady=10)

        # second tab
        self.label_tab_decompress = customtkinter.CTkLabel(
            self.tabview.tab("Decompress"), text="Choose the method"
        )
        self.label_tab_decompress.pack_propagate(False)
        self.label_tab_decompress.pack()

        # create second frame
        self.decompress_frame = customtkinter.CTkFrame(self.tabview.tab("Decompress"))
        self.decompress_var = tkinter.IntVar(value=0)
        self.decompress_frame.pack()
        self.decompress_button_1 = customtkinter.CTkRadioButton(
            text="Oleg4",
            master=self.decompress_frame,
            variable=self.decompress_var,
            value=4,
        )
        self.decompress_button_1.pack(padx=10, pady=10)
        self.decompress_button_2 = customtkinter.CTkRadioButton(
            text="Oleg5",
            master=self.decompress_frame,
            variable=self.decompress_var,
            value=5,
        )
        self.decompress_button_2.pack(padx=10, pady=10)
        self.decompress_button_3 = customtkinter.CTkRadioButton(
            text="Oleg6",
            master=self.decompress_frame,
            variable=self.decompress_var,
            value=6,
        )
        self.decompress_button_3.pack(padx=10, pady=10)

        # create decompress browse file button
        self.decompress_browse_button = customtkinter.CTkButton(
            master=self.tabview.tab("Decompress"),
            text="Browse File",
            fg_color="transparent",
            border_width=2,
            text_color=("gray10", "#DCE4EE"),
            command=self.BrowseFileToDecompress,
        )
        self.decompress_browse_button.pack(pady=10)

        # create compress filename line
        self.filepath = customtkinter.StringVar(value="")
        self.file_to_compress_name = customtkinter.CTkEntry(
            master=self.tabview.tab("Compress"), state="disabled"
        )
        self.file_to_compress_name.pack()

        # create decompress filename line
        self.filepath = customtkinter.StringVar(value="")
        self.file_to_decompress_name = customtkinter.CTkEntry(
            master=self.tabview.tab("Decompress"), state="disabled"
        )
        self.file_to_decompress_name.pack()

        # create decompress save file button
        self.decompress_save_button = customtkinter.CTkButton(
            master=self.tabview.tab("Decompress"),
            text="Save File",
            fg_color="transparent",
            border_width=2,
            text_color=("gray10", "#DCE4EE"),
            command=self.SaveDecompressedFile,
        )
        self.decompress_save_button.pack(pady=10)

        # create compress save file button
        self.compress_save_button = customtkinter.CTkButton(
            master=self.tabview.tab("Compress"),
            text="Save File",
            fg_color="transparent",
            border_width=2,
            text_color=("gray10", "#DCE4EE"),
            command=self.SaveCompressedFile,
        )
        self.compress_save_button.pack(pady=10)

    def BrowseFileToCompress(self):
        if not self.compress_var.get():
            tkinter.messagebox.showerror(
                "File Error", "Choose the method of compression"
            )
        else:
            self.file_to_compress_name.configure(state="normal")
            self.file_to_compress_name.delete(0, "end")
            self.file_to_compress_name.insert(
                0,
                filedialog.askopenfilename(initialdir=os.getcwd(), title="Select File"),
            )
            self.file_to_compress_name.configure(state="disabled")
            self.file_to_compress_path = self.file_to_compress_name.get()

            print(f"res: {self.file_to_compress_path, self.compress_var.get()}")

    def BrowseFileToDecompress(self):
        self.file_to_decompress_name.configure(state="normal")
        self.file_to_decompress_name.delete(0, "end")
        self.file_to_decompress_name.insert(
            0,
            filedialog.askopenfilename(initialdir=os.getcwd(), title="Select File"),
        )
        self.file_to_decompress_name.configure(state="disabled")
        self.file_to_decompress_path = self.file_to_decompress_name.get()
        print(f"res: {self.file_to_decompress_path, self.decompress_var.get()}")

    def SaveDecompressedFile(self):
        if not self.file_to_decompress_path:
            tkinter.messagebox.showerror("File Error", "Choose the file to decompress")
        else:
            file = filedialog.asksaveasfile(title="Save File", defaultextension=".oleg")
            with open(file.name, "w", encoding="utf-8") as new_file:
                new_file.write(self.file_to_decompress_path)

    def SaveCompressedFile(self):
        if not self.file_to_compress_path:
            tkinter.messagebox.showerror("File Error", "Choose the file to decompress")

        else:
            extension = self.compress_var.get()
            if not extension:
                tkinter.messagebox.showerror(
                    "File Error", "Choose the method of compression"
                )

            file = filedialog.asksaveasfile(
                title="Save File", defaultextension=f".{extension}"
            )

            if extension == "lz78":
                Codder.encoding(self.file_to_compress_path, file.name)

                tkinter.messagebox.showerror("Success", "Success")
                self.file_to_compress_name.configure(state="normal")
                self.file_to_compress_name.delete(0, "end")
                self.file_to_compress_name.configure(state="disabled")


if __name__ == "__main__":
    app = App()
    app.title("Sigma App")
    app.iconbitmap("../sticker_019.ico")
    app.geometry("600x400")
    app.resizable(width=False, height=False)
    app.mainloop()
