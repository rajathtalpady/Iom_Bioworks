# Nature Nurture Automation Script Documentation

## Overview
This script processes and merges data from multiple CSV files related to home remedies and outputs a consolidated dataset. It identifies and matches relevant remedies based on predefined conditions and appends the results to an output file.

---

## Requirements
- **Python version**: 3.6 or later
- **Dependencies**:
  - `pandas`
  - `os`
  - `sys`

Install missing dependencies using:
```bash
pip install pandas
```

---

## Usage
Run the script using the following command:
```bash
python3 Nature_nurture_automation.py <Meta_Data_csv> <Reference_csv> <Tokens_csv>
```

### Arguments:
1. **`<Meta_Data_csv>`**: CSV file containing metadata, including a row for home remedies.
2. **`<Reference_csv>`**: CSV file with reference data mapping remedies to doses and durations.
3. **`<Tokens_csv>`**: CSV file where results will be appended starting at a specified column.

---

## Input File Structure
### **Meta Data CSV**
- Must contain the following columns:
  - `Questions`
  - `Answers`
- Should include a row where `Questions` is "home remedies" and `Answers` contains a list of remedies.

### **Reference CSV**
- Maps home remedies to doses and durations.
- Should include columns:
  - `Home Remedy for`
  - `Dose & Duration`

### **Tokens CSV**
- The file where the matched data will be appended.

---

## Output File
- **Name**: `<Tokens_csv>_Processed.csv`
- **Location**: Saved in the `output` directory.
- **Contents**: The `Tokens_csv` file with appended matched remedies and doses.

---

## Script Workflow
### 1. **Input Validation**
   - Verifies the presence of required command-line arguments.
   - Ensures all input files exist in the specified input directory.

### 2. **Data Extraction and Cleaning**
#### **Home Remedies Extraction**:
   - Extracts the "home remedies" row from the metadata CSV.
   - Cleans and formats the remedies list by removing special characters and handling specific conditions.

#### **Matching Remedies**:
   - Normalizes strings for case-insensitive partial matching.
   - Matches remedies from the metadata file with the reference data.

### 3. **Appending Data**
   - Creates a single row containing matched remedies and their corresponding doses/durations.
   - Appends the data to the tokens CSV starting from a specified column.

### 4. **Output Generation**
   - Saves the updated tokens CSV to the `output` directory.

---

## File Paths
- **Base Directory**: `/Users/rajathtalpady/Desktop/Iom_Bioworks/Nature_nurture_Automation`
  - **Input Directory**: `input`
  - **Output Directory**: `output`

The script automatically creates the output directory if it does not exist.

---

## Example Command
```bash
python3 Nature_nurture_automation.py IOM119F130723_Meta_data_Notes.csv reference.csv IOM119F130723_Tokens.csv
```

---

## Error Handling
- If any input file is missing, the script exits with an error message.
- If no "home remedies" row is found, the script exits with a warning.
- Handles cases where no matches are found in the reference file.

---

## Contact
For issues or questions, please contact:
**Rajath Talpady**
- Email: rajath@iombio.com
- GitHub: [github.com/rajathtalpady](https://github.com/rajathtalpady)

