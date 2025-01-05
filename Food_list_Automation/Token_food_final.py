import os
import sys
import pandas as pd

def process_food_data(data):
    
    data['Food_group'] = data['Food_group'].replace(['Milk & Milk products', 'Milk & milk products', 'Meat'], 'Others')
    data['Food_group'] = data['Food_group'].str.strip().str.title()
    data.fillna('-',inplace=True)
    data['Rationale'] = data['Rationale'].replace({r'\bIncrease\b': 'Increases', r'\bDecrease\b': 'Decreases'}, regex=True)
    comm = []
    for comment in data['Rationale']:
        if len(comment)>1:
            cmt = comment.split(', ')
            #print(cmt)
            if len(cmt)>1:
                for i in range (1,len(cmt)+1):
                    if cmt[len(cmt)-i].startswith("Increases") or cmt[len(cmt)-i].startswith("Decreases"):
                        continue
                    elif cmt[0].startswith("Increases"): 
                        cmt[len(cmt)-i] = 'Increases '+str((cmt[len(cmt)-i]).strip())
                    elif cmt[0].startswith("Decreases"):
                        cmt[len(cmt)-i] = 'Decreases'+str((cmt[len(cmt)-i]).strip())
            cmt = ', '.join(cmt)

        else:
            cmt = '-'
        comm.append(cmt)
    data['Rationale'] = comm    
  
    output_rows = []
    food_groups = sorted(data['Food_group'].unique())

    for group in food_groups:
        group_data = data[data['Food_group'] == group]
        take_items = group_data[group_data['Final Call'] == 'Take']['Item'].tolist()
        avoid_items = group_data[group_data['Final Call'] == 'Avoid']['Item'].tolist()
        take_rationales = group_data[group_data['Final Call'] == 'Take']['Rationale'].dropna().unique().tolist()
        avoid_rationales = group_data[group_data['Final Call'] == 'Avoid']['Rationale'].dropna().unique().tolist()
        
        output_rows.append({
            "Food_groups": group,
            "Eat freely (take)": ", ".join(take_items) + (f"\n#{', '.join(take_rationales)}" if take_rationales else ""),
            "Reduce eating": ", ".join(avoid_items) + (f"\n#{', '.join(avoid_rationales)}" if avoid_rationales else "")                                                 
        })
    
    return pd.DataFrame(output_rows)

def post_process_data(text):
    if pd.isna(text) or '#' not in text:
        return text  # Return as is if no '#' or text is NaN

    # Split text into pre-# part and post-# part
    pre_hash, post_hash = text.split('#', 1)
    pre_hash = pre_hash.strip()
    post_hash = post_hash.strip()

    # Split the post-hash text by commas and process each part
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

    # Handle "Nutritional Balance" case
    if len(increases) == 0 and len(decreases) == 0 and not other:
        other = ["#Nutritional Balance"]  # Only add if it's the only content

    # Combine the parts back into a single string
    increases_part = f"#Increases: {', '.join(increases)}" if increases else ""
    decreases_part = f"#Decreases: {', '.join(decreases)}" if decreases else ""
    other_part = ', '.join(other)

    # Construct the final text
    components = []
    if increases_part:
        components.append(increases_part)  # Add increases part if present
    if decreases_part:
        components.append(decreases_part)  # Add decreases part on a new line
    if other_part:
        components.append(other_part)

    # Combine components with proper line breaks
    hash_part = '\n'.join(components).strip()

    # Return the final combined text
    return f"{pre_hash}\n{hash_part}" if hash_part else pre_hash


def extract_and_merge_data(input_csv, existing_csv, output_csv, start_column=62):
    
    # Sample data
    data = pd.read_csv(input_csv)
    
    # Create a DataFrame
    df = pd.DataFrame(data)
    
    # Initialize your dictionaries for storing values
    Nuts = {"eat": "", "avoid": ""}
    Fruits = {"eat": "", "avoid": ""}
    Grains = {"eat": "", "avoid": ""}
    Others = {"eat": "", "avoid": ""}
    Seeds = {"eat": "", "avoid": ""}
    Spices = {"eat": "", "avoid": ""}
    Vegetables = {"eat": "", "avoid": ""}

    # List to store the groups
    groups = df['Food_groups'].tolist()

    # Iterate over the groups and extract values for "Dry Fruits & Nuts"
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
 
                   
    # Create the big list from Nuts dictionary
    big_list = [Grains['eat'], Grains['avoid'],
                Vegetables['eat'], Vegetables['avoid'],
                Fruits['eat'], Fruits['avoid'],
                Nuts['eat'], Nuts['avoid'],
                Seeds['eat'], Seeds['avoid'],
                Spices['eat'],Spices['avoid'],
                Others['eat'], Others['avoid']]
    
    # Read the existing DataFrame (df2)
    df2 = pd.read_csv(existing_csv)
    
    # Ensure there are enough columns in df2
    while len(df2.columns) < start_column + len(big_list):
        df2[f'Column_{len(df2.columns) + 1}'] = ''
    
    # Merge big_list values into df2 at the appropriate starting column
    for i, value in enumerate(big_list):
        df2.iloc[0, start_column + i] = value
    
    # Save the new DataFrame to the output CSV
    df2.to_csv(output_csv, index=False)
    print(f"Data merged and saved to: {output_csv}")
    return df2


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 Food.py <Final_CSV> <Tokens_CSV>")
        sys.exit(1)
    
    base_dir = "/Users/rajathtalpady/Desktop/Iom_Bioworks/Food_list_Automation"
    input_dir = os.path.join(base_dir, "input")
    output_dir = os.path.join(base_dir, "output")
    os.makedirs(output_dir, exist_ok=True)
    
    final_csv = sys.argv[1]
    tokens_csv = sys.argv[2]
    
    final_input_path = os.path.join(input_dir, final_csv)
    tokens_input_path = os.path.join(input_dir, tokens_csv)
    
    if not os.path.exists(final_input_path):
        print(f"Error: Final CSV file '{final_csv}' not found in the input folder.")
        sys.exit(1)
    
    if not os.path.exists(tokens_input_path):
        print(f"Error: Tokens CSV file '{tokens_csv}' not found in the input folder.")
        sys.exit(1)
    
    # Process food data
    final_output_file = f"{os.path.splitext(final_csv)[0]}_Processed.csv"
    final_output_path = os.path.join(output_dir, final_output_file)
    
    # Load and process the input data
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




