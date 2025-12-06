import tkinter as tk
from tkinter import filedialog, messagebox
from collections import defaultdict

def merge_listfiles():
    filepaths = filedialog.askopenfilenames(
        title="Select listfiles to merge",
        filetypes=[("Text files", "*.txt")]
    )
    if not filepaths:
        return

    all_entries = {}
    duplicates = defaultdict(list)

    for filepath in filepaths:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            for line_num, line in enumerate(f, 1):
                entry = line.strip()
                if not entry:
                    continue

                key = entry.lower()
                if key in all_entries:
                    duplicates[key].append((filepath, line_num, entry))
                else:
                    all_entries[key] = entry

    output_path = filedialog.asksaveasfilename(
        title="Save merged listfile as",
        defaultextension=".txt",
        filetypes=[("Text files", "*.txt")]
    )
    if not output_path:
        return

    with open(output_path, "w", encoding="utf-8") as out:
        for entry in sorted(all_entries.values(), key=lambda s: s.lower()):
            out.write(entry + "\n")

    msg = f"Merged {len(all_entries)} unique entries.\n"
    if duplicates:
        msg += f"{sum(len(v) for v in duplicates.values())} duplicates ignored."
    else:
        msg += "No duplicates found."

    messagebox.showinfo("Merge Complete", msg)

root = tk.Tk()
root.title("ListM")
root.geometry("400x200")

label = tk.Label(root, text="Merge WoW listfiles into one clean file", font=("Arial", 12))
label.pack(pady=20)

merge_button = tk.Button(root, text="Select listfiles and Merge", command=merge_listfiles, font=("Arial", 10), width=25)
merge_button.pack(pady=20)

quit_button = tk.Button(root, text="Quit", command=root.quit, font=("Arial", 10), width=25)
quit_button.pack(pady=10)


root.mainloop()
