import matplotlib.pyplot as plt
import pandas as pd
import os
import sys

def generate_graphs(csv_file, output_dir):
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Read the CSV file
    data = pd.read_csv(csv_file)

    # Define categories for the graphs
    categories = [
        ("Energy", "Energy_Available_initial", "Energy_Available_final", 2),  # Percentage (+1) column index
        ("Fatigue", "Energy_Fatigue_initial", "Energy_Fatigue_final", 3),  # Percentage (-1) column index
        ("Sleep Quality", "Sleep_Quality_initial", "Sleep_Quality_final", 2),  # Percentage (+1) column index
        ("Sleep Duration", "Sleep_Duration_initial", "Sleep_Duration_final", 2),  # Percentage (+1) column index
        ("Sleep Efficiency", "Sleep_Efficiency_initial", "Sleep_Efficiency_final", 2),  # Percentage (+1) column index
        ("Anxiety", "Stress_Anxiety_initial", "Stress_Anxiety_final", 3),  # Percentage (-1) column index
        ("Depression", "Stress_Depression_initial", "Stress_Depression_final", 3),  # Percentage (-1) column index
        ("Stress", "Stress_Stress_initial", "Stress_Stress_final", 3),  # Percentage (-1) column index
    ]

    # Colors for the rings
    fatigue_anxiety_colors = ['#388087', '#f0f0f0']
    energy_sleep_colors = ['#1E1F3F', '#f0f0f0']
    inner_colors = ['#f5c25b', '#f0f0f0']

    # Generate graphs
    for title, initial_key, final_key, percentage_column_index in categories:
        try:
            # Access the percentage values based on the column index (3rd or 4th column)
            initial_value = data.loc[data['Id'] == initial_key].iloc[0, percentage_column_index]
            final_value = data.loc[data['Id'] == final_key].iloc[0, percentage_column_index]

            # Determine the outer colors based on the category
            if title in ["Anxiety", "Depression", "Stress", "Fatigue"]:
                outer_colors = fatigue_anxiety_colors
            else:
                outer_colors = energy_sleep_colors

            # Create the figure
            fig, ax = plt.subplots(figsize=(6, 6))

            # Plot outer ring (Final/Optimised)
            ax.pie([final_value, 100 - final_value],
                   radius=1,
                   colors=outer_colors,
                   startangle=90,
                   counterclock=False,
                   wedgeprops=dict(width=0.25, edgecolor='w'))

            # Plot inner ring (Initial/Now)
            ax.pie([initial_value, 100 - initial_value],
                   radius=0.7,
                   colors=inner_colors,
                   startangle=90,
                   counterclock=False,
                   wedgeprops=dict(width=0.25, edgecolor='w'))

            # Add the central text
            plt.text(0, 0, title, ha='center', va='center', fontsize=12, color='gray')

            # Add the legend
            handles = [
                plt.Line2D([0], [0], color=outer_colors[0], lw=3),  # Outer ring color for "Optimised"
                plt.Line2D([0], [0], color=inner_colors[0], lw=3)   # Inner ring color for "Now"
            ]
            plt.legend(handles,
                       ['Optimised', 'Now'],
                       loc="upper center",
                       bbox_to_anchor=(0.5, -0.1),
                       ncol=2,
                       handlelength=2,
                       handleheight=0.2,
                       fontsize=10)

            # Title for the chart
            plt.title(title.upper(), fontsize=20, weight='bold', pad=20)

            # Ensure the pie is drawn as a circle
            ax.axis('equal')

            # Save the chart
            file_name = f"{title.replace(' ', '_')}.png"
            file_path = os.path.join(output_dir, file_name)
            plt.savefig(file_path, dpi=300, bbox_inches='tight')
            plt.close(fig)
            print(f"Chart saved: {file_path}")
        except IndexError:
            print(f"Data for '{title}' is missing or incomplete in the CSV file.")

if __name__ == "__main__":
    # Define base and input directories
    base_dir = "/Users/rajathtalpady/Desktop/Iom_Bioworks/Sens_2.0_Charts"
    input_dir = os.path.join(base_dir, "input")
    
    # Ensure the input directory exists
    if not os.path.exists(input_dir):
        print(f"Input directory not found: {input_dir}")
        sys.exit(1)
    
    # Ensure at least one CSV file is passed
    if len(sys.argv) < 2:
        print("Usage: python3 chart.py <csv_file_name>")
        sys.exit(1)
    
    csv_file_name = sys.argv[1]
    csv_file = os.path.join(input_dir, csv_file_name)
    if not os.path.exists(csv_file):
        print(f"File not found: {csv_file}")
        sys.exit(1)

    # Extract the base name for the output folder (before the first underscore)
    output_folder_name = csv_file_name.split("_")[0]  # Extracts "IOMHPL006"
    output_dir = os.path.join(base_dir, "output", output_folder_name)

    # Generate graphs
    generate_graphs(csv_file, output_dir)
    
    # Command: python3 Sens_2.0_charts.py IOMHPL006_Scores.csv 
