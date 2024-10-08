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
            label=file_path.split('/')[-1],)  # Negate Im(Z) for correct plot

plt.xlabel('Re(Z) (Ohm)',fontsize='18')
plt.ylabel('-Im(Z) (Ohm)',fontsize='18')
plt.title('Nyquist Plots for Multiple Files')
plt.legend('10°C','40°C','25°C',fontsize='18')
plt.grid(True)
plt.show(block=False)  # Show the plot without blocking

# Initialize the second plot for Bode plot with dual y-axes and logarithmic scales
fig, ax1 = plt.subplots(figsize=(10, 6))

# Plot Frequency (Hz) vs Im(Z) (Ohm) on the primary y-axis with logarithmic scales
for file_path in file_paths:
    data = pd.read_csv(file_path, delimiter="\t", decimal=",")
    df = pd.DataFrame(data)

    # Ensure that Frequency, Re(Z), and -Im(Z) are in the correct columns
    df_filtered = df[(df.iloc[:, 2] != 0) & (df.iloc[:, 3] != 0)]

    # Plot Frequency (Hz) vs -Im(Z)
    ax1.plot(df_filtered.values[:, 1], -df_filtered.values[:, 3], label=file_path.split('/')[-1] + ' (Im(Z))')

ax1.set_xlabel('Frequency (Hz)')
ax1.set_ylabel('-Im(Z) (Ohm)', color='tab:blue')
ax1.tick_params(axis='y', labelcolor='tab:blue')
ax1.set_xscale('log')
ax1.set_yscale('log')

# Create a secondary y-axis for Re(Z) (Ohm) with logarithmic scales
ax2 = ax1.twinx()
for file_path in file_paths:
    data = pd.read_csv(file_path, delimiter="\t", decimal=",")
    df = pd.DataFrame(data)

    # Plot Frequency (Hz) vs Re(Z)
    ax2.plot(df_filtered.iloc[:, 1], df_filtered.iloc[:, 2], linestyle='--',
             label=file_path.split('/')[-1] + ' (Re(Z))', color='tab:red')

ax2.set_ylabel('Re(Z) (Ohm)', color='tab:red')
ax2.tick_params(axis='y', labelcolor='tab:red')
ax2.set_yscale('log')

fig.suptitle('Bode Plot with Dual Y-Axis and Logarithmic Scales for Multiple Files')
fig.legend(loc='upper left', bbox_to_anchor=(0.1, 0.9))
fig.tight_layout()
plt.show()  # Show the plot without blocking

