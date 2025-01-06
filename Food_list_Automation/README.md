# Food Automation Script Documentation

## Overview
This script processes and merges data from food-related CSV files, categorizing items into food groups and associating them with specific rationales. The output is a consolidated dataset with refined information about foods to consume or avoid and their associated impacts.

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
python3 Food.py <Final_CSV> <Tokens_CSV>
```

### Arguments:
1. **`<Final_CSV>`**: CSV file containing raw food data to be processed.
2. **`<Tokens_CSV>`**: CSV file where processed data will be merged starting at a specified column.

---

## Input File Structure
### **Final CSV**
- Should include the following columns:
  - `Food_group`
  - `Item`
  - `Final Call` (e.g., "Take" or "Avoid")
  - `Rationale`

### **Tokens CSV**
- A pre-existing CSV file where the processed food data will be appended.

---

## Output Files
1. **Processed Data**:
   - **Name**: `<Final_CSV>_Processed.csv`
   - **Location**: Saved in the `output` directory.
   - **Contents**: Cleaned and categorized food data.

2. **Merged Tokens**:
   - **Name**: `<Tokens_CSV>_Merged.csv`
   - **Location**: Saved in the `output` directory.
   - **Contents**: The tokens CSV with appended processed food data.

---

## Script Workflow

### 1. **Input Validation**
   - Ensures all required arguments are provided.
   - Verifies the existence of input files in the `input` directory.

### 2. **Data Processing**
#### **Food Data Cleaning**:
   - Standardizes food group names (e.g., merges "Milk & Milk Products" into "Others").
   - Fills missing values with placeholders (e.g., "-").
   - Cleans and restructures `Rationale` values for consistency.

#### **Categorization**:
   - Groups items by `Food_group` and further categorizes them as "Eat freely" or "Reduce eating" based on the `Final Call` column.
   - Associates rationales with each food group and action.

### 3. **Post-Processing**
   - Refines output text to include formatted rationale information.
   - Handles special cases (e.g., "Nutritional Balance" logic).

### 4. **Data Merging**
   - Appends processed data to the specified `Tokens CSV` file starting at a predefined column.
   - Ensures the output file includes all required columns.

### 5. **Output Generation**
   - Saves the processed data and the merged tokens CSV to the `output` directory.

---

## File Paths
- **Base Directory**: `/Users/rajathtalpady/Desktop/Iom_Bioworks/Food_list_Automation`
  - **Input Directory**: `input`
  - **Output Directory**: `output`

The script automatically creates the output directory if it does not exist.

---

## Example Command
```bash
python3 Food.py IOMID_Final.csv IOMID_Tokens.csv
```

---

## Error Handling
- Exits with an error message if any input file is missing.
- Ensures all required columns exist in the input files.
- Handles unexpected food group names gracefully with clear error messages.

---

## Contact
For issues or questions, please contact:
**Rajath Talpady**
- Email: rajath@iombio.com
- GitHub: [github.com/rajathtalpady](https://github.com/rajathtalpady)

