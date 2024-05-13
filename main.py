import tkinter as tk
from tkinter import filedialog, messagebox
import zipfile
import pyzipper
from threading import Thread
 
 
class ZipCrackerApp(tk.Tk):
   def __init__(self):
       super().__init__()
       self.title("Zip File Brute Force")
       self.file_path = tk.StringVar()
       self.min_length = tk.IntVar()
       self.max_length = tk.IntVar()
       self.result_text = tk.StringVar()
       self.zip_type = tk.StringVar(value="standard")  # Default to standard zip
 
 
       self.create_widgets()
 
 
   def create_widgets(self):
       # File Selection
       file_label = tk.Label(self, text="Select Zip File:")
       file_label.grid(row=0, column=0, padx=5, pady=5)
       file_entry = tk.Entry(self, textvariable=self.file_path, width=50)
       file_entry.grid(row=0, column=1, padx=5, pady=5)
       browse_button = tk.Button(self, text="Browse", command=self.browse_file)
       browse_button.grid(row=0, column=2, padx=5, pady=5)
 
 
       # Zip Type Selection
       zip_type_label = tk.Label(self, text="Zip File Type:")
       zip_type_label.grid(row=1, column=0, padx=5, pady=5)
       zip_type_standard = tk.Radiobutton(self, text="Standard Zip", variable=self.zip_type, value="standard")
       zip_type_standard.grid(row=1, column=1, padx=5, pady=5)
       zip_type_aes = tk.Radiobutton(self, text="AES Encrypted Zip", variable=self.zip_type, value="aes")
       zip_type_aes.grid(row=1, column=2, padx=5, pady=5)
 
 
       # Password Length
       min_length_label = tk.Label(self, text="Minimum Password Length:")
       min_length_label.grid(row=2, column=0, padx=5, pady=5)
       min_length_entry = tk.Entry(self, textvariable=self.min_length, width=10)
       min_length_entry.grid(row=2, column=1, padx=5, pady=5)
       max_length_label = tk.Label(self, text="Maximum Password Length:")
       max_length_label.grid(row=2, column=2, padx=5, pady=5)
       max_length_entry = tk.Entry(self, textvariable=self.max_length, width=10)
       max_length_entry.grid(row=2, column=3, padx=5, pady=5)
 
 
       # Result Label
       result_label = tk.Label(self, textvariable=self.result_text)
       result_label.grid(row=3, column=0, columnspan=4, padx=5, pady=5)
 
 
       # Start Button
       start_button = tk.Button(self, text="Start Brute Force", command=self.start_brute_force)
       start_button.grid(row=4, column=0, columnspan=4, padx=5, pady=5)
 
 
   def browse_file(self):
       file_path = filedialog.askopenfilename(filetypes=[("Zip files", "*.zip")])
       if file_path:
           self.file_path.set(file_path)
 
 
   def brute_force(self):
       zip_file_path = self.file_path.get()
       min_length = self.min_length.get()
       max_length = self.max_length.get()
 
 
       try:
           if self.zip_type.get() == "aes":
               zip_file = pyzipper.AESZipFile(zip_file_path)
           else:
               zip_file = zipfile.ZipFile(zip_file_path, 'r')
 
 
           with zip_file:
               for length in range(min_length, max_length + 1):
                   for password in self.generate_passwords(length):
                       try:
                           if self.zip_type.get() == "aes":
                               zip_file.pwd = password.encode()
                               zip_file.extractall()
                           else:
                               zip_file.extractall(pwd=password.encode())
                           self.result_text.set(f"Password found: {password}")
                           return
                       except (RuntimeError, zipfile.BadZipFile):
                           pass
           self.result_text.set("Password not found.")
       except Exception as e:
           messagebox.showerror("Error", str(e))
 
 
   def start_brute_force(self):
       if not self.file_path.get():
           messagebox.showerror("Error", "Please select a ZIP file.")
           return
       if self.min_length.get() <= 0 or self.max_length.get() <= 0:
           messagebox.showerror("Error", "Password length should be greater than zero.")
           return
       if self.min_length.get() > self.max_length.get():
           messagebox.showerror("Error", "Minimum password length cannot be greater than maximum.")
           return
 
 
       self.result_text.set("Starting brute force...")
       Thread(target=self.brute_force).start()
 
 
   def generate_passwords(self, length):
       for i in range(26 ** length):
           password = ""
           for j in range(length):
               password += chr(ord('a') + (i // (26 ** j)) % 26)
           yield password
 
 
if __name__ == "__main__":
   app = ZipCrackerApp()
   app.mainloop()
