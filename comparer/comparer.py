import pandas as pd


def compare(file1: str, file2: str):
    df1 = pd.read_excel(file1)
    df2 = pd.read_excel(file2)

    # Strip whitespace from all string columns
    for col in df1.select_dtypes(include=['object']).columns:
        df1[col] = df1[col].str.strip() if df1[col].dtype == 'object' else df1[col]
    for col in df2.select_dtypes(include=['object']).columns:
        df2[col] = df2[col].str.strip() if df2[col].dtype == 'object' else df2[col]

    # Create composite key column
    df1['_key'] = df1['UN'].astype(str) + '_' + df1['VariantCode'].astype(str)
    df2['_key'] = df2['UN'].astype(str) + '_' + df2['VariantCode'].astype(str)

    # Find what's in each
    keys1 = set(df1['_key'])
    keys2 = set(df2['_key'])

    common_keys = keys1 & keys2
    only_in_df1 = keys1 - keys2
    only_in_df2 = keys2 - keys1

    # Show deleted rows
    if only_in_df1:
        print("=== Deleted Rows (only in file 1) ===")
        print(df1[df1['_key'].isin(only_in_df1)].drop('_key', axis=1))

    # Show added rows
    if only_in_df2:
        print("\n=== Added Rows (only in file 2) ===")
        print(df2[df2['_key'].isin(only_in_df2)].drop('_key', axis=1))

    # Compare common rows
    if common_keys:
        print("\n=== Checking for changes in common rows ===")
        for key in common_keys:
            row1 = df1[df1['_key'] == key].drop('_key', axis=1).iloc[0]
            row2 = df2[df2['_key'] == key].drop('_key', axis=1).iloc[0]

            # Compare only common columns
            common_cols = row1.index.intersection(row2.index)
            changes = []
            for col in common_cols:
                if pd.isna(row1[col]) and pd.isna(row2[col]):
                    continue
                if row1[col] != row2[col]:
                    changes.append(f"{col}: '{row1[col]}' -> '{row2[col]}'")

            if changes:
                print(
                    f"\nUN={df1[df1['_key'] == key]['UN'].iloc[0]}, VariantCode={df1[df1['_key'] == key]['VariantCode'].iloc[0]}:")
                for change in changes:
                    print(f"  {change}")