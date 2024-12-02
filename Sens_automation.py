import pandas as pd
import os
import sys

def main(input_file1, input_file2, output_file1, output_file2):
    
    df1 = pd.read_csv(input_file1)
    df2 = pd.read_csv(input_file2)
    
    iom_id = next((col for col in df2.columns if col.startswith("IOM")), None)
    if not iom_id:
        print("Error: No column starting with 'IOM' found in the input file.")
        return
    
    df2_top20 = df2.sort_values(by=iom_id, ascending=False).head(20)

    df3 = df2_top20.merge(
        df1[["#OTU ID", "Bacteria Tag 1 in Report", "Positive Impact"]],
        on="#OTU ID",
        how="inner"
    )
    
    df3.rename(columns={"Bacteria Tag 1 in Report": "Labels"}, inplace=True)
   
    df3.to_csv(output_file1, index=False)

    pivot_table = df3.pivot_table(
        index="Labels",               
        values=iom_id,                
        aggfunc="sum"                 
    ).round(2)
    
    pivot_table_reset = pivot_table.reset_index()

    pivot_table_reset.rename(columns={iom_id: f"SUM of {iom_id}"}, inplace=True)

    pivot_table_reset = pivot_table_reset.sort_values(by=f"SUM of {iom_id}", ascending=False)

    pivot_table_reset.to_csv(output_file2, index=False)

    print(f"Sens + {iom_id} Report:")
    print(df3)
    print(f"\n{iom_id} Pivot Table:")
    print(pivot_table_reset)

if __name__ == "__main__":
    
    if len(sys.argv) < 3:
        print("Usage: python3 Sens_automation.py Reference.csv IOM_file1 IOM_file2 ... IOM_fileN")
        sys.exit(1)

    reference_file = sys.argv[1]
    
    iom_files = sys.argv[2:]

    base_dir = "/Users/rajathtalpady/Desktop/Iom_Bioworks/Sens_Automation"
    input_dir = os.path.join(base_dir, "input")
    output_dir = os.path.join(base_dir, "output")

    os.makedirs(output_dir, exist_ok=True)

    reference_file_path = os.path.join(input_dir, reference_file)
    if not os.path.exists(reference_file_path):
        print(f"Error: Reference file '{reference_file}' not found.")
        sys.exit(1)

    for iom_file in iom_files:
        iom_file_path = os.path.join(input_dir, iom_file)
        if not os.path.exists(iom_file_path):
            print(f"Error: IOM file '{iom_file}' not found.")
            continue

        sens_output = f"{os.path.splitext(iom_file)[0]}_SENS_Output.csv"
        pivot_output = f"{os.path.splitext(iom_file)[0]}_Pivot_Table.csv"
        sens_output_path = os.path.join(output_dir, sens_output)
        pivot_output_path = os.path.join(output_dir, pivot_output)

        # Call the main function to process the IOM file
        main(reference_file_path, iom_file_path, sens_output_path, pivot_output_path)

    print("SENS++ processing completed.")
