import pandas as pd
import os
import sys

def find_tag(score):
    if score > 20:
        tag = 'Tag1'
        level = 'High'
    elif 10 < score <= 20:
        tag = 'Tag2'
        level = 'Medium'
    elif 0 < score <= 10:
        tag = 'Tag3'
        level = 'Low'
    else:
        level = 'Absent'
        tag = 'Absent'
    return tag, level

def assign_tags(df, tags_tab, text_tags_db):
    tag_list = []
    level_list = []
    texts = []
    tags = []

    for index, row in df.iterrows():
        score = row[df.columns[1]]
        label = row['Labels']
        
        tag, level = find_tag(score)
        tag_list.append(tag)
        level_list.append(level)

        if label in tags_tab['Label'].values:
            tagg = tags_tab[tag][tags_tab['Label'] == label].values[0]
        else:
            tagg = 'Absent'

        if label in text_tags_db['List Of Tags'].values:
            text = text_tags_db[tag][text_tags_db['List Of Tags'] == label].values[0]
        else:
            text = 'Not present'

        texts.append(text)
        tags.append(tagg)

    df['Indicator'] = tags
    df['Levels'] = level_list
    df['Text'] = texts
    return df

def main(input_file1, input_file2, text_tags_file, tags_table_file, output_file1, output_file2):
    # Load the input dataframes
    df1 = pd.read_csv(input_file1)
    df2 = pd.read_csv(input_file2)

    # Automatically detect the column name starting with "IOM"
    iom_id = next((col for col in df2.columns if col.startswith("IOM")), None)
    if not iom_id:
        print("Error: No column starting with 'IOM' found in the input file.")
        return

    # Get the top 20 rows of df2 based on the detected IOM ID column
    df2_top20 = df2.sort_values(by=iom_id, ascending=False).head(20)

    # Merge df2_top20 with df1 on the "#OTU ID" column
    df3 = df2_top20.merge(
        df1[["#OTU ID", "Bacteria Tag 1 in Report", "Positive Impact"]],
        on="#OTU ID",
        how="inner"
    )

    # Rename the "Bacteria Tag 1 in Report" column to "Labels"
    df3.rename(columns={"Bacteria Tag 1 in Report": "Labels"}, inplace=True)

    # Save the merged dataframe (df3) to output_file1
    df3.to_csv(output_file1, index=False)
    
    # Create a pivot table with "Labels" as index and sum of the IOM ID column
    pivot_table = df3.pivot_table(
        index="Labels",               
        values=iom_id,                
        aggfunc="sum"                 
    ).round(2).reset_index()

    # Rename the column dynamically
    pivot_table.rename(columns={iom_id: f"SUM of {iom_id}"}, inplace=True)

    # Sort the pivot table by the dynamically named column
    pivot_table = pivot_table.sort_values(by=f"SUM of {iom_id}", ascending=False)

    # Load tags-related data
    text_tags_db = pd.read_csv(text_tags_file)
    tags_tab = pd.read_csv(tags_table_file)

    # Assign tags and texts to the pivot table
    result_df = assign_tags(pivot_table, tags_tab, text_tags_db)

    # Save the final output
    result_df.to_csv(output_file2, index=False)

    print(f"Output saved to: {output_file2}")

if __name__ == "__main__":
    # Check for correct number of arguments
    if len(sys.argv) < 5:
        print("Usage: python3 Sens_automation.py IOM_file Reference.csv Text_for_tags.csv Tags_table_sens+.csv")
        sys.exit(1)

    # Input arguments
    iom_file = sys.argv[1]
    reference_file = sys.argv[2]
    text_tags_file = sys.argv[3]
    tags_table_file = sys.argv[4]

    # Set up directories
    base_dir = "/Users/rajathtalpady/Desktop/Iom_Bioworks/Sens_Automation"
    input_dir = os.path.join(base_dir, "input")
    output_dir = os.path.join(base_dir, "output")
    os.makedirs(output_dir, exist_ok=True)

    # Input and output file paths
    iom_file_path = os.path.join(input_dir, iom_file)
    reference_file_path = os.path.join(input_dir, reference_file)
    text_tags_file_path = os.path.join(input_dir, text_tags_file)
    tags_table_file_path = os.path.join(input_dir, tags_table_file)

    sens_output_name = f"{os.path.splitext(iom_file)[0]}_SENS.csv"
    final_file_name = f"{os.path.splitext(iom_file)[0]}_SENS_Final_Output.csv"
    sens_file_path = os.path.join(output_dir, sens_output_name)
    final_file_path = os.path.join(output_dir, final_file_name)

    # Run the main function
    main(reference_file_path, iom_file_path, text_tags_file_path, tags_table_file_path, sens_file_path, final_file_path)
    
    # Command: python3 Sens_automation.py IOM025FX210924.csv Reference.csv Text_for_tags.csv Tags_table_sens.csv