import os
import sys
import pandas as pd

# Function to process food data
def process_food_data(data):
    # Standardize and clean the 'Food_group' column
    data['Food_group'] = data['Food_group'].replace(['Milk & Milk products', 'Milk & milk products', 'Meat'], 'Others')
    data['Food_group'] = data['Food_group'].str.strip().str.title()
    # Fill missing values with a placeholder
    data.fillna('-', inplace=True)
    # Standardize the 'Rationale' column
    data['Rationale'] = data['Rationale'].replace({r'\bIncrease\b': 'Increases', r'\bDecrease\b': 'Decreases'}, regex=True)

    # Initialize a list for cleaned rationales
    comm = []
    for comment in data['Rationale']:
        if len(comment) > 1:
            cmt = comment.split(', ')
            # Process each rationale component
            if len(cmt) > 1:
                for i in range(1, len(cmt) + 1):
                    if cmt[len(cmt) - i].startswith("Increases") or cmt[len(cmt) - i].startswith("Decreases"):
                        continue
                    elif cmt[0].startswith("Increases"): 
                        cmt[len(cmt) - i] = 'Increases ' + str((cmt[len(cmt) - i]).strip())
                    elif cmt[0].startswith("Decreases"):
                        cmt[len(cmt) - i] = 'Decreases ' + str((cmt[len(cmt) - i]).strip())
            cmt = ', '.join(cmt)
        else:
            cmt = '-'
        comm.append(cmt)
    data['Rationale'] = comm

    # Prepare output rows for each food group
    output_rows = []
    food_groups = sorted(data['Food_group'].unique())
    for group in food_groups:
        group_data = data[data['Food_group'] == group]
        take_items = group_data[group_data['Final Call'] == 'Take']['Item'].tolist()
        avoid_items = group_data[group_data['Final Call'] == 'Avoid']['Item'].tolist()
        take_rationales = group_data[group_data['Final Call'] == 'Take']['Rationale'].dropna().unique().tolist()
        avoid_rationales = group_data[group_data['Final Call'] == 'Avoid']['Rationale'].dropna().unique().tolist()

        # Create a dictionary for each group with processed information
        output_rows.append({
            "Food_groups": group,
            "Eat freely (take)": ", ".join(take_items) + (f"\n#{', '.join(take_rationales)}" if take_rationales else ""),
            "Reduce eating": ", ".join(avoid_items) + (f"\n#{', '.join(avoid_rationales)}" if avoid_rationales else "")                                                 
        })
    
    return pd.DataFrame(output_rows)

# Function to post-process textual data
def post_process_data(text):
    # Skip processing if text is NaN or lacks '#'
    if pd.isna(text) or '#' not in text:
        return text

    # Split text into pre-# and post-# components
    pre_hash, post_hash = text.split('#', 1)
    pre_hash = pre_hash.strip()
    post_hash = post_hash.strip()

    # Process individual parts of the post-hash text
    parts = [p.strip() for p in post_hash.split(',')]
    increases = []
    decreases = []
    other = []
    for part in parts:
        if part.startswith("Increases"):
            microbe = part.replace("Increases", "").strip()
            if microbe not in increases:
                increases.append(microbe)
        elif part.startswith("Decreases"):
            microbe = part.replace("Decreases", "").strip()
            if microbe not in decreases:
                decreases.append(microbe)
        else:
            if part != "Nutritional Balance" and part not in increases + decreases + other:
                other.append(part)

    # Handle special case of 'Nutritional Balance'
    if len(increases) == 0 and len(decreases) == 0 and not other:
        other = ["#Nutritional Balance"]

    # Combine processed parts back into text
    increases_part = f"#Increases: {', '.join(increases)}" if increases else ""
    decreases_part = f"#Decreases: {', '.join(decreases)}" if decreases else ""
    other_part = ', '.join(other)

    # Finalize the processed text
    components = [p for p in [increases_part, decreases_part, other_part] if p]
    hash_part = '\n'.join(components).strip()
    return f"{pre_hash}\n{hash_part}" if hash_part else pre_hash

# Function to extract and merge data into a new CSV file
def extract_and_merge_data(input_csv, existing_csv, output_csv, start_column=62):
    data = pd.read_csv(input_csv)
    df = pd.DataFrame(data)

    # Initialize dictionaries for food categories
    Nuts, Fruits, Grains, Others, Seeds, Spices, Vegetables = (
        {"eat": "", "avoid": ""} for _ in range(7)
    )
    groups = df['Food_groups'].tolist()

    # Process food group data and populate dictionaries
    for group in groups:
        record = df[df['Food_groups'] == group]
        if group == "Dry Fruits & Nuts":
            Nuts['eat'] = ', '.join(record['Eat freely (take)'].tolist())
            Nuts['avoid'] = ', '.join(record['Reduce eating'].tolist())
        elif group == "Fruits":
            Fruits['eat'] = ', '.join(record['Eat freely (take)'].tolist())
            Fruits['avoid'] = ', '.join(record['Reduce eating'].tolist())
        elif group == "Grains":
            Grains['eat'] = ', '.join(record['Eat freely (take)'].tolist())
            Grains['avoid'] = ', '.join(record['Reduce eating'].tolist())
        elif group == "Others":
            Others['eat'] = ', '.join(record['Eat freely (take)'].tolist())
            Others['avoid'] = ', '.join(record['Reduce eating'].tolist())
        elif group == "Seeds":
            Seeds['eat'] = ', '.join(record['Eat freely (take)'].tolist())
            Seeds['avoid'] = ', '.join(record['Reduce eating'].tolist())
        elif group == "Spices":
            Spices['eat'] = ', '.join(record['Eat freely (take)'].tolist())
            Spices['avoid'] = ', '.join(record['Reduce eating'].tolist())
        elif group == "Vegetables":
            Vegetables['eat'] = ', '.join(record['Eat freely (take)'].tolist())
            Vegetables['avoid'] = ', '.join(record['Reduce eating'].tolist())
        else:
            raise ValueError(f"Unexpected food group '{group}' encountered.")

    # Create a list with the data from dictionaries
    big_list = [
        Grains['eat'], Grains['avoid'],
        Vegetables['eat'], Vegetables['avoid'],
        Fruits['eat'], Fruits['avoid'],
        Nuts['eat'], Nuts['avoid'],
        Seeds['eat'], Seeds['avoid'],
        Spices['eat'], Spices['avoid'],
        Others['eat'], Others['avoid']
    ]

    # Merge big_list into the existing CSV file
    df2 = pd.read_csv(existing_csv)
    while len(df2.columns) < start_column + len(big_list):
        df2[f'Column_{len(df2.columns) + 1}'] = ''
    for i, value in enumerate(big_list):
        df2.iloc[0, start_column + i] = value
    df2.to_csv(output_csv, index=False)
    print(f"Data merged and saved to: {output_csv}")
    return df2

# Main function for command-line execution
if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 Food.py <Final_CSV> <Tokens_CSV>")
        sys.exit(1)
    # Paths for input and output directories
    base_dir = "/Users/rajathtalpady/Desktop/Iom_Bioworks/Food_list_Automation"
    input_dir = os.path.join(base_dir, "input")
    output_dir = os.path.join(base_dir, "output")
    os.makedirs(output_dir, exist_ok=True)

    # Read file names from command-line arguments
    final_csv = sys.argv[1]
    tokens_csv = sys.argv[2]

    # Construct file paths
    final_input_path = os.path.join(input_dir, final_csv)
    tokens_input_path = os.path.join(input_dir, tokens_csv)

    # Verify the existence of input files
    if not os.path.exists(final_input_path):
        print(f"Error: Final CSV file '{final_csv}' not found in the input folder.")
        sys.exit(1)
    if not os.path.exists(tokens_input_path):
        print(f"Error: Tokens CSV file '{tokens_csv}' not found in the input folder.")
        sys.exit(1)

    # Process food data
    final_output_file = f"{os.path.splitext(final_csv)[0]}_Processed.csv"
    final_output_path = os.path.join(output_dir, final_output_file)
    data = pd.read_csv(final_input_path)
    processed_data = process_food_data(data)

    # Apply post-processing to specific columns
    columns_to_postprocess = ["Eat freely (take)", "Reduce eating"]
    for column in columns_to_postprocess:
        if column in processed_data.columns:
            processed_data[column] = processed_data[column].apply(post_process_data)

    # Save the processed data
    processed_data.to_csv(final_output_path, index=False)
    print(f"Processed food data saved to: {final_output_path}")

    # Extract and merge data
    tokens_output_file = f"{os.path.splitext(tokens_csv)[0]}_Merged.csv"
    tokens_output_path = os.path.join(output_dir, tokens_output_file)
    extract_and_merge_data(final_output_path, tokens_input_path, tokens_output_path)
    print(f"Tokens data processing completed and saved to: {tokens_output_path}")
    print("All tasks completed successfully.")
    
# Command: python3 Token_food_final.py IOMID_Final.csv IOMID_Tokens.csv
# Example: python3 Token_food_final.py IOM026HXKR42B_Final.csv IOM026HXKR42B_Tokens.csv




