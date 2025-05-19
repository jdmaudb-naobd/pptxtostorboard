import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
from pathlib import Path
import threading
from pptx_extractor import PowerPointExtractor

class PowerPointExtractorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("PowerPoint Extractor")
        self.root.geometry("600x400")
        
        # Create main frame
        main_frame = ttk.Frame(root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Example folder selection
        ttk.Label(main_frame, text="Example Folder (with paired .pptx/.docx files):").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.example_folder = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.example_folder, width=50).grid(row=1, column=0, padx=5)
        ttk.Button(main_frame, text="Browse", command=self.browse_example_folder).grid(row=1, column=1)
        
        # Input folder selection
        ttk.Label(main_frame, text="Input PowerPoint Folder:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.input_folder = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.input_folder, width=50).grid(row=3, column=0, padx=5)
        ttk.Button(main_frame, text="Browse", command=self.browse_input_folder).grid(row=3, column=1)
        
        # Output folder selection
        ttk.Label(main_frame, text="Output Folder:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.output_folder = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.output_folder, width=50).grid(row=5, column=0, padx=5)
        ttk.Button(main_frame, text="Browse", command=self.browse_output_folder).grid(row=5, column=1)
        
        # Progress bar
        self.progress = ttk.Progressbar(main_frame, length=400, mode='determinate')
        self.progress.grid(row=6, column=0, columnspan=2, pady=20)
        
        # Status label
        self.status_var = tk.StringVar(value="Ready")
        ttk.Label(main_frame, textvariable=self.status_var).grid(row=7, column=0, columnspan=2)
        
        # Process button
        self.process_btn = ttk.Button(main_frame, text="Process Files", command=self.process_files)
        self.process_btn.grid(row=8, column=0, columnspan=2, pady=10)
        
    def browse_example_folder(self):
        folder = filedialog.askdirectory(title="Select Example Folder")
        if folder:
            self.example_folder.set(folder)
            
    def browse_input_folder(self):
        folder = filedialog.askdirectory(title="Select Input PowerPoint Folder")
        if folder:
            self.input_folder.set(folder)
            
    def browse_output_folder(self):
        folder = filedialog.askdirectory(title="Select Output Folder")
        if folder:
            self.output_folder.set(folder)
            
    def validate_inputs(self):
        if not self.example_folder.get():
            messagebox.showerror("Error", "Please select an example folder")
            return False
        if not self.input_folder.get():
            messagebox.showerror("Error", "Please select an input folder")
            return False
        if not self.output_folder.get():
            messagebox.showerror("Error", "Please select an output folder")
            return False
        return True
    
    def process_files(self):
        if not self.validate_inputs():
            return
            
        self.process_btn.state(['disabled'])
        self.status_var.set("Processing...")
        self.progress['value'] = 0
        
        # Start processing in a separate thread
        thread = threading.Thread(target=self.run_processing)
        thread.daemon = True
        thread.start()
    
    def run_processing(self):
        try:
            extractor = PowerPointExtractor()
            
            # Get list of input files
            input_files = [f for f in os.listdir(self.input_folder.get()) if f.endswith('.pptx')]
            total_files = len(input_files)
            
            for i, input_file in enumerate(input_files):
                input_path = os.path.join(self.input_folder.get(), input_file)
                output_path = os.path.join(self.output_folder.get(), 
                                         os.path.splitext(input_file)[0] + '.docx')
                
                # Update progress
                progress = (i + 1) / total_files * 100
                self.progress['value'] = progress
                self.status_var.set(f"Processing {input_file}...")
                
                # Process the file
                extractor.process_presentation(input_path, output_path)
            
            self.status_var.set("Processing complete!")
            messagebox.showinfo("Success", "All files have been processed successfully!")
            
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            self.status_var.set("Error occurred during processing")
        
        finally:
            self.process_btn.state(['!disabled'])
            self.progress['value'] = 0

if __name__ == "__main__":
    root = tk.Tk()
    app = PowerPointExtractorGUI(root)
    root.mainloop() 