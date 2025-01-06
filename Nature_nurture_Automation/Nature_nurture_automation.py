import os
import sys
import pandas as pd

def append_matched_data_to_csv(input_csv_1, input_csv_2, input_csv_3, output_csv, start_column=80):
    # Load the input CSVs
    df1 = pd.read_csv(input_csv_1)
    df2 = pd.read_csv(input_csv_2)
    df3 = pd.read_csv(input_csv_3)

    # Extract and format home remedies from df1
    home_remedies_row = df1[df1["Questions"] == 'home remedies']
    if not home_remedies_row.empty:
        home_remedies_answers = home_remedies_row['Answers'].values[0]
        
        # Remove square brackets, single quotes, and split into a list
        home_remedies_list = home_remedies_answers.replace("[", "").replace("]", "").replace("'", "").split(",")

        # Clean and format the remedies list
        home_remedies_list = [
            item.strip().replace(" -", "-").replace("- ", "-")
            for item in home_remedies_list
        ]

        # Check condition and remove 'IBS /Digestive boost' if both conditions are met
        if ('IBS /Digestive boost' and 'Metabolic boost') in home_remedies_list:
            home_remedies_list.remove('IBS /Digestive boost')
    else:
        print("No home remedies found in the input data.")
        return

    # Normalize strings for matching
    df2["Normalized Remedy"] = df2["Home Remedy for"].str.strip().str.lower()

    # Match and extract rows that contain any of the partial matches
    matched_rows = df2[df2["Normalized Remedy"].apply(
        lambda remedy: any(partial.lower() in remedy for partial in home_remedies_list)
    )].copy()

    # Drop the helper column after matching
    df2.drop(columns=["Normalized Remedy"], inplace=True)
    matched_rows.drop(columns=["Normalized Remedy"], inplace=True)

    # Prepare data for a single row with multiple columns
    if not matched_rows.empty:
        # Create a list of remedies and doses for output
        big_list = []
        for _, row in matched_rows.iterrows():
            big_list.extend([row["Home Remedy for"], row["Dose & Duration"]])

        # Ensure df3 has enough columns to accommodate the start column and data
        while len(df3.columns) < start_column + len(big_list):
            df3[f'Column_{len(df3.columns) + 1}'] = ''

        # Add `big_list` values into `df3` starting at the specified column
        for i, value in enumerate(big_list):
            df3.iloc[0, start_column + i] = value

        # Save the modified DataFrame to a new CSV
        df3.to_csv(output_csv, index=False)
        print(f"Data merged and saved to: {output_csv}")
    else:
        print("No matches found.")


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python3 script.py <Meta_Data_csv> <Reference_csv> <Tokens_csv>")
        sys.exit(1)

    # Define base directories
    base_dir = "/Users/rajathtalpady/Desktop/Iom_Bioworks/Nature_nurture_Automation"
    input_dir = os.path.join(base_dir, "input")
    output_dir = os.path.join(base_dir, "output")
    os.makedirs(output_dir, exist_ok=True)

    # Input and output file paths
    input_csv_1 = os.path.join(input_dir, sys.argv[1])
    input_csv_2 = os.path.join(input_dir, sys.argv[2])
    input_csv_3 = os.path.join(input_dir, sys.argv[3])
    output_csv = os.path.join(output_dir, f"{os.path.splitext(sys.argv[3])[0]}_Processed.csv")

    # Check if input files exist
    for file in [input_csv_1, input_csv_2, input_csv_3]:
        if not os.path.exists(file):
            print(f"Error: File '{file}' not found in the input folder.")
            sys.exit(1)

    # Call the function to process and save the output
    append_matched_data_to_csv(input_csv_1, input_csv_2, input_csv_3, output_csv, start_column=80)
    print("Processing completed successfully.")
    
# Command: python3 Nature_nurture_automation.py IOM119F130723_Meta_data_Notes.csv reference.csv IOM119F130723_Tokens.csv
