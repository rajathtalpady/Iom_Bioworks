# Sens 2.0 Charts Generator

This Python script generates graphical visualizations from a CSV file containing data on various health metrics. The visualizations are saved as PNG files in an output directory for easy sharing and analysis.

## Features

- Generates **dual-ring pie charts** comparing initial and final values for various categories such as energy, sleep quality, anxiety, and more.
- Automatically organizes output into folders based on input file names.
- Supports user-friendly configuration via command-line arguments.

## Requirements

- Python 3.6 or higher
- Libraries:
  - `matplotlib`
  - `pandas`

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/sens-2.0-charts.git
   cd sens-2.0-charts
   ```

2. Install the required Python libraries:

   ```bash
   pip install matplotlib pandas
   ```

## Usage

1. Place your input CSV files in the `input` directory:

   ```
   Sens_2.0_Charts/
   ├── input/
   │   └── <your_csv_file>.csv
   ```

2. Run the script:

   ```bash
   python3 chart.py <csv_file_name>
   ```

   Replace `<csv_file_name>` with the name of your CSV file, e.g., `IOMHPL006_Data.csv`.

3. Find the generated charts in the `output` directory:

   ```
   Sens_2.0_Charts/
   ├── output/
   │   └── IOMHPL006/
   │       ├── Energy.png
   │       ├── Sleep_Quality.png
   │       └── ...
   ```

## CSV Format

Ensure your CSV file follows the structure below:

| Id                     | Energy_Available_initial | Energy_Available_final | Percentage | ... |
|------------------------|---------------------------|-------------------------|------------|-----|
| Energy_Available       | 50                       | 80                     | 75         | ... |
| Energy_Fatigue         | 30                       | 50                     | 40         | ... |

### Categories Visualized:

- **Energy**
- **Fatigue**
- **Sleep Quality**
- **Sleep Duration**
- **Sleep Efficiency**
- **Anxiety**
- **Depression**
- **Stress**

## Error Handling

- If the input directory does not exist, the script will display an error and exit.
- If the CSV file is missing required data, a warning will be displayed for the affected category, and the chart will be skipped.

## Output Visualization

Each category generates a chart with:
- **Outer ring:** Final/Optimized values
- **Inner ring:** Initial/Current values
- A clear legend and a centered title for easy interpretation.

## Contributing

Contributions are welcome! Please submit a pull request or raise an issue for any improvements or bug fixes.

## Contact

For any questions or feedback, feel free to reach out at rajath.iombio.com


