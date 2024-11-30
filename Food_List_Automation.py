import os
import sys
import pandas as pd

def process_food_data(data):
    """
    Processes the food data to create a new table based on specified requirements.
    """
    output_rows = []
    food_groups = data['Food_group'].unique()
    
    for group in food_groups:
        group_data = data[data['Food_group'] == group]
        take_items = group_data[group_data['Final Call'] == 'Take']['Item'].tolist()
        avoid_items = group_data[group_data['Final Call'] == 'Avoid']['Item'].tolist()
        take_rationales = group_data[group_data['Final Call'] == 'Take']['Rationale'].dropna().unique().tolist()
        avoid_rationales = group_data[group_data['Final Call'] == 'Avoid']['Rationale'].dropna().unique().tolist()
        
        output_rows.append({
            "Food group": group,
            "Eat freely (take)": ", ".join(take_items) + (f"\nRationale: {', '.join(take_rationales)}" if take_rationales else ""),
            "Reduce eating": ", ".join(avoid_items) + (f"\nRationale: {', '.join(avoid_rationales)}" if avoid_rationales else "")
        })
    
    return pd.DataFrame(output_rows)

if __name__ == "__main__":
    # Check for correct number of arguments
    if len(sys.argv) < 2:
        print("Usage: python3 process_food_list.py IOM_file1 IOM_file2 ... IOM_fileN")
        sys.exit(1)
    
    # Set up directories
    base_dir = "/Users/rajathtalpady/Desktop/Iom_Bioworks/Food_list_Automation"
    input_dir = os.path.join(base_dir, "input")
    output_dir = os.path.join(base_dir, "output")
    os.makedirs(output_dir, exist_ok=True)

    # Process each IOM file passed as arguments
    iom_files = sys.argv[1:]
    for iom_file in iom_files:
        # Construct input and output file paths
        input_file_path = os.path.join(input_dir, iom_file)
        if not os.path.exists(input_file_path):
            print(f"Error: IOM file '{iom_file}' not found.")
            continue

        # Define output file path
        output_file_name = f"{os.path.splitext(iom_file)[0]}_Processed.csv"
        output_file_path = os.path.join(output_dir, output_file_name)

        # Process the file directly (no try-except block)
        data = pd.read_csv(input_file_path)
        processed_data = process_food_data(data)
        processed_data.to_csv(output_file_path, index=False)
        print(f"Processed file saved to: {output_file_path}")

    print(f"{iom_file} Food list processing completed.")
    
    # Command = python3 Food_list.py IOM119F130723_Final.csv
