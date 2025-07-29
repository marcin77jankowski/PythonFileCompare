import argparse
import pandas as pd


def parse_args():
    parser = argparse.ArgumentParser(description="Compare two CSV files with join and exclude columns.")
    parser.add_argument("file1", help="First CSV file")
    parser.add_argument("file2", help="Second CSV file")
    parser.add_argument("--type", help="File type as defined in config file")
    parser.add_argument("--join-cols", help="Comma-separated list of join columns")
    parser.add_argument("--exclude-cols", default="", help="Comma-separated list of columns to exclude from comparison")
    parser.add_argument("--sep", help="CSV separator")
    return parser.parse_args()


def compare_csv(file1, file2, join_cols, exclude_cols, sep=','):
    df1 = pd.read_csv(file1, sep=sep)
    df2 = pd.read_csv(file2, sep=sep)

    join_cols = [col.strip() for col in join_cols.split(",") if col.strip()]
    exclude_cols = [col.strip() for col in exclude_cols.split(",") if col.strip()]

    compare_cols = [col for col in df1.columns if col not in join_cols + exclude_cols]

    merged = pd.merge(df1, df2, on=join_cols, suffixes=("_1", "_2"), how="outer", indicator=True)

    total = len(merged)
    matched = 0
    unmatched = 0
    differences = []
    col_diff_counts = {col: 0 for col in compare_cols}
    col_differences = {col: [] for col in compare_cols}

    for _, row in merged.iterrows():
        if row["_merge"] == "both":
            same = True
            for col in compare_cols:
                if row[f"{col}_1"] != row[f"{col}_2"]:
                    col_diff_counts[col] += 1
                    if len(col_differences[col]) < 10:
                        col_differences[col].append({
                            "join": {jcol: row[jcol] for jcol in join_cols},
                            "value1": row[f"{col}_1"],
                            "value2": row[f"{col}_2"]
                        })
                    same = False
            if same:
                matched += 1
            else:
                diff = {col: (row[f"{col}_1"], row[f"{col}_2"]) for col in compare_cols if row[f"{col}_1"] != row[f"{col}_2"]}
                differences.append({"join": {col: row[col] for col in join_cols}, "diff": diff})
                unmatched += 1
        else:
            differences.append({"join": {col: row[col] for col in join_cols}, "status": row["_merge"]})
            unmatched += 1

    print(f"Total rows compared: {total}")
    print(f"Rows with all compared columns matching: {matched}")
    print(f"Rows with differences or unmatched: {unmatched}")

    print("\nColumn difference summary:")
    for col in compare_cols:
        if col_diff_counts[col] == 0:
            print(f"Column '{col}': always the same")
        else:
            print(f"Column '{col}': {col_diff_counts[col]} differences")

    if differences:
        print("\nDifferences (showing up to 10):")
        for item in differences[:10]:
            print(item)

    # Write up to 10 differences per column to file
    import json
    with open("column_differences.json", "w", encoding="utf-8") as f:
        json.dump(col_differences, f, ensure_ascii=False, indent=2)


def main():
    args = parse_args()
    import json
    config = None
    if args.type:
        with open("file_types_config.json", "r", encoding="utf-8") as f:
            config = json.load(f)
        if args.type not in config:
            print(f"File type '{args.type}' not found in config.")
            return
        type_cfg = config[args.type]
        join_cols = ",".join(type_cfg.get("join_cols", []))
        exclude_cols = ",".join(type_cfg.get("exclude_cols", []))
        sep = type_cfg.get("sep", ",")
    else:
        join_cols = args.join_cols
        exclude_cols = args.exclude_cols
        sep = args.sep if args.sep else ","
    compare_csv(args.file1, args.file2, join_cols, exclude_cols, sep)


if __name__ == "__main__":
    main()
