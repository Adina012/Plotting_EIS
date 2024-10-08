import pandas as pd
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog


# Function to get file paths using a file picker dialog
def get_file_paths():
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    file_paths = filedialog.askopenfilenames(title="Select files",
                                             filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    root.quit()  # Close the Tkinter root window properly
    return file_paths


# Get the file paths from the user
file_paths = get_file_paths()

# Initialize the first plot for Nyquist plot (Re(Z) vs -Im(Z))
plt.figure(figsize=(10, 6))
for file_path in file_paths:
    data = pd.read_csv(file_path, delimiter="\t", decimal=",")
    df = pd.DataFrame(data)

    # Ensure that Re(Z) is in column 2 and -Im(Z) is in column 3
    # Filter out rows where either Re(Z) or -Im(Z) is zero
    df_filtered = df[(df.iloc[:, 2] != 0) & (df.iloc[:, 3] != 0)]

    # Plot Re(Z) against -Im(Z)
    plt.plot(df_filtered.values[:, 2], df_filtered.values[:, 3],
            label=file_path.split('/')[-1])  # Negate Im(Z) for correct plot

plt.xlabel('Re(Z) (Ohm)', fontsize='18')
plt.ylabel('-Im(Z) (Ohm)', fontsize='18')
plt.title('Nyquist Plots for Multiple Files')
plt.legend('{10°C} {40°C} {25°C}',fontsize='18')
plt.grid(True)
plt.show(block=False)  # Show the plot without blocking


plt.show()
