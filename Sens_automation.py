import pandas as pd
import os
import sys

def main(input_file1, input_file2, output_file1, output_file2):
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
        index="Labels",               # Rows: "Labels"
        values=iom_id,                # Values: IOM ID column
        aggfunc="sum"                 # Aggregation function: sum
    ).round(2)

    # Reset the pivot table index
    pivot_table_reset = pivot_table.reset_index()

    # Rename the column dynamically
    pivot_table_reset.rename(columns={iom_id: f"SUM of {iom_id}"}, inplace=True)

    # Sort the pivot table by the dynamically named column
    pivot_table_reset = pivot_table_reset.sort_values(by=f"SUM of {iom_id}", ascending=False)

    # Save the pivot table to output_file2
    pivot_table_reset.to_csv(output_file2, index=False)

    # Print the outputs for verification
    print(f"Sens + {iom_id} Report:")
    print(df3)
    print(f"\n{iom_id} Pivot Table:")
    print(pivot_table_reset)

if __name__ == "__main__":
    # Check for correct number of arguments
    if len(sys.argv) < 3:
        print("Usage: python3 Sens_automation.py Reference.csv IOM_file1 IOM_file2 ... IOM_fileN")
        sys.exit(1)

    # First argument is the reference file (Reference.csv)
    reference_file = sys.argv[1]
    
    # Remaining arguments are IOM files
    iom_files = sys.argv[2:]

    # Set up directories
    base_dir = "/Users/rajathtalpady/Desktop/Iom_Bioworks/Sens_Automation"
    input_dir = os.path.join(base_dir, "input")
    output_dir = os.path.join(base_dir, "output")

    os.makedirs(output_dir, exist_ok=True)

    # Check if reference file exists
    reference_file_path = os.path.join(input_dir, reference_file)
    if not os.path.exists(reference_file_path):
        print(f"Error: Reference file '{reference_file}' not found.")
        sys.exit(1)

    # Process each IOM file passed as arguments
    for iom_file in iom_files:
        iom_file_path = os.path.join(input_dir, iom_file)
        if not os.path.exists(iom_file_path):
            print(f"Error: IOM file '{iom_file}' not found.")
            continue

        # Define output file paths
        sens_output = f"{os.path.splitext(iom_file)[0]}_SENS_Output.csv"
        pivot_output = f"{os.path.splitext(iom_file)[0]}_Pivot_Table.csv"
        sens_output_path = os.path.join(output_dir, sens_output)
        pivot_output_path = os.path.join(output_dir, pivot_output)

        # Call the main function to process the IOM file
        main(reference_file_path, iom_file_path, sens_output_path, pivot_output_path)

    print("SENS++ processing completed.")
