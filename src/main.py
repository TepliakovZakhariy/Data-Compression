import tkinter
import os
from tkinter import filedialog
import tkinter.messagebox
import customtkinter
from lz77 import LZ77
from lz78 import Codder
from lzw import LZW
from huffman import Huffman

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")


class App(customtkinter.CTk):

    def __init__(self):
        super().__init__()

        self.browsed_filename = ""
        self.file_to_compress_path = ""
        self.extension = ""
        self.file_to_decompress_path = ""
        self.huffman = Huffman()
        self.lz77 = LZ77(100)

        # create tabview
        self.tabview = customtkinter.CTkTabview(self, width=250)
        self.tabview.pack(padx=10, pady=10)
        self.tabview.add("Compress")
        self.tabview.add("Decompress")

        # first tab
        self.label_tab_compress = customtkinter.CTkLabel(
            self.tabview.tab("Compress"), text="Choose the method"
        )
        self.label_tab_compress.pack_propagate(False)
        self.label_tab_compress.pack()

        # second tab
        self.label_tab_decompress = customtkinter.CTkLabel(
            self.tabview.tab("Decompress"), text="Choose the file to decompress"
        )
        self.label_tab_decompress.pack_propagate(False)
        self.label_tab_decompress.pack()

        # create first frame
        self.compress_frame = customtkinter.CTkFrame(self.tabview.tab("Compress"))
        self.compress_var = tkinter.StringVar(value="")
        self.compress_frame.pack()

        self.compress_button_1 = customtkinter.CTkRadioButton(
            text="LZ77",
            master=self.compress_frame,
            variable=self.compress_var,
            value="lz77",
        )
        self.compress_button_1.pack(pady=10)

        self.compress_button_2 = customtkinter.CTkRadioButton(
            text="LZ78",
            master=self.compress_frame,
            variable=self.compress_var,
            value="lz78",
        )
        self.compress_button_2.pack(pady=10)

        self.compress_button_3 = customtkinter.CTkRadioButton(
            text="LZW",
            master=self.compress_frame,
            variable=self.compress_var,
            value="lzw",
        )
        self.compress_button_3.pack(pady=10)

        self.compress_button_4 = customtkinter.CTkRadioButton(
            text="Huffman",
            master=self.compress_frame,
            variable=self.compress_var,
            value="huf",
        )
        self.compress_button_4.pack(pady=10)

        self.compress_button_5 = customtkinter.CTkRadioButton(
            text="Deflate",
            master=self.compress_frame,
            variable=self.compress_var,
            value="def",
        )
        self.compress_button_5.pack(pady=10)

        # create second frame
        self.decompress_frame = customtkinter.CTkFrame(self.tabview.tab("Decompress"))
        self.decompress_frame.pack()

        # create compress filename line
        self.file_to_compress_name = customtkinter.CTkEntry(
            master=self.tabview.tab("Compress"), state="disabled", width=230
        )
        self.file_to_compress_name.pack(pady=10)

        # create decompress filename line
        self.file_to_decompress_name = customtkinter.CTkEntry(
            master=self.decompress_frame, state="disabled", width=230
        )
        self.file_to_decompress_name.pack(pady=10)

        # create compress choose file label
        self.choose_file_to_compress_label = customtkinter.CTkLabel(
            master=self.tabview.tab("Compress"), text="Choose the file to compress"
        )
        self.choose_file_to_compress_label.pack()

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

        # create decompress browse file button
        self.decompress_browse_button = customtkinter.CTkButton(
            master=self.decompress_frame,
            text="Browse File",
            fg_color="transparent",
            border_width=2,
            text_color=("gray10", "#DCE4EE"),
            command=self.BrowseFileToDecompress,
        )
        self.decompress_browse_button.pack(pady=10)

        # create compress save file button
        self.compress_save_button = customtkinter.CTkButton(
            master=self.tabview.tab("Compress"),
            text="Compress and save",
            fg_color="transparent",
            border_width=2,
            text_color=("gray10", "#DCE4EE"),
            command=self.SaveCompressedFile,
        )
        self.compress_save_button.pack()

        # create decompress save file button
        self.decompress_save_button = customtkinter.CTkButton(
            master=self.decompress_frame,
            text="Decompress and save",
            fg_color="transparent",
            border_width=2,
            text_color=("gray10", "#DCE4EE"),
            command=self.SaveDecompressedFile,
        )
        self.decompress_save_button.pack()

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

    def BrowseFileToDecompress(self):
        self.file_to_decompress_name.configure(state="normal")
        self.file_to_decompress_name.delete(0, "end")
        self.file_to_decompress_name.insert(
            0,
            filedialog.askopenfilename(initialdir=os.getcwd(), title="Select File"),
        )
        self.file_to_decompress_name.configure(state="disabled")
        self.file_to_decompress_path = self.file_to_decompress_name.get()
        self.extension = self.file_to_decompress_path.split(".")[-1]

        if self.extension == "lz77":
            self.decompressed_filetype = self.lz77.get_extension(
                self.file_to_decompress_path
            )
        elif self.extension == "lz78":
            self.decompressed_filetype = Codder.get_extension(
                self.file_to_decompress_path
            )
        elif self.extension == "lzw":
            self.decompressed_filetype = LZW.get_extension(self.file_to_decompress_path)
        elif self.extension == "huf":
            self.decompressed_filetype = Huffman.get_extension(
                self.file_to_decompress_path
            )
        else:
            tkinter.messagebox.showerror("File Error", "Unknown type of file")

    def SaveCompressedFile(self):
        if not self.compress_var.get():
            tkinter.messagebox.showerror(
                "File Error", "Choose the method of compression"
            )
        elif not self.file_to_compress_path:
            tkinter.messagebox.showerror("File Error", "Choose the file to decompress")

        else:
            extension = self.compress_var.get()
            if not extension:
                tkinter.messagebox.showerror(
                    "File Error", "Choose the method of compression"
                )
            self.file_to_compress_name.configure(state="normal")
            self.file_to_compress_name.delete(0, "end")
            self.file_to_compress_name.insert(0, "Compression in progress...")
            self.file_to_compress_name.configure(state="disabled")

            file = None
            file = filedialog.asksaveasfile(
                title="Save File", defaultextension=f".{extension}"
            )

            if file and extension in ["lz77", "lz78", "lzw", "huf"]:

                if extension == "lz77":
                    self.lz77.encode_file(self.file_to_compress_path, file.name)

                elif extension == "lz78":
                    Codder.encoding(self.file_to_compress_path, file.name)

                elif extension == "lzw":
                    LZW.encode_file(self.file_to_compress_path, file.name)

                elif extension == "huf":
                    self.huffman.encode_file(self.file_to_compress_path, file.name)

                tkinter.messagebox.showinfo(
                    "Success", "The file has been successfully compressed!"
                )
                self.file_to_compress_name.configure(state="normal")
                self.file_to_compress_name.delete(0, "end")
                self.file_to_compress_name.configure(state="disabled")

            else:
                self.file_to_compress_name.configure(state="normal")
                self.file_to_compress_name.delete(0, "end")
                self.file_to_compress_name.insert(0, self.file_to_compress_path)
                self.file_to_compress_name.configure(state="disabled")

    def SaveDecompressedFile(self):
        if not self.file_to_decompress_path:
            tkinter.messagebox.showerror("File Error", "Choose the file to decompress")
        else:
            self.file_to_decompress_name.configure(state="normal")
            self.file_to_decompress_name.delete(0, "end")
            self.file_to_decompress_name.insert(0, "Decompression in progress...")
            self.file_to_decompress_name.configure(state="disabled")

            file = None
            file = filedialog.asksaveasfile(
                title="Save File", defaultextension=f".{self.decompressed_filetype}"
            )

            if file and self.extension in ["lz77", "lz78", "lzw", "huf"]:

                if self.extension == "lz77":
                    self.lz77.decode_file(self.file_to_decompress_path, file.name)

                elif self.extension == "lz78":
                    Codder.decoding(self.file_to_decompress_path, file.name)

                elif self.extension == "lzw":
                    LZW.decode_file(self.file_to_decompress_path, file.name)

                elif self.extension == "huf":
                    self.huffman.decode_file(self.file_to_decompress_path, file.name)

                tkinter.messagebox.showinfo(
                    "Success", "The file has been successfully decompressed!"
                )
                self.file_to_decompress_name.configure(state="normal")
                self.file_to_decompress_name.delete(0, "end")
                self.file_to_decompress_name.configure(state="disabled")

            else:
                self.file_to_decompress_name.configure(state="normal")
                self.file_to_decompress_name.delete(0, "end")
                self.file_to_decompress_name.insert(0, self.file_to_decompress_path)
                self.file_to_decompress_name.configure(state="disabled")


if __name__ == "__main__":
    app = App()
    app.title("Data Compression")
    app.iconbitmap("assets/image.ico")
    app.resizable(width=False, height=False)
    app.mainloop()
