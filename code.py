import pandas as pd


# ---------- Create a sample messy dataset----------
def create_sample_csv(path="quality_check_data.csv"):
    data = {
        "order_id": [1, 2, 3, 4, 4, 5, None, 7],
        "customer_name": ["Riya", "Sameer", None, "Tanvi", "Tanvi", "Uday", "Vikas", "Riya"],
        "amount": ["1500", "2300", "abc", "1800", "1800", None, "2100", "-500"],
        "email": ["riya@mail.com", "sameer@mail", "aisha@mail.com", "tanvi@mail.com",
                   "tanvi@mail.com", "uday@mail.com", "vikas@mail.com", "riya@mail.com"]
    }
    df = pd.DataFrame(data)
    df.to_csv(path, index=False)
    print(f"Sample raw CSV created at: {path}")
    return path


def check_missing_values(df):
    print("\n--- MISSING VALUES ---")
    missing = df.isnull().sum()
    missing_pct = (df.isnull().mean() * 100).round(2)
    report = pd.DataFrame({"missing_count": missing, "missing_pct": missing_pct})
    print(report[report["missing_count"] > 0])
    return report


def check_duplicates(df):
    print("\n--- DUPLICATE ROWS ---")
    dup_count = df.duplicated().sum()
    print(f"Total duplicate rows: {dup_count}")
    if dup_count > 0:
        print(df[df.duplicated(keep=False)])
    return dup_count


def check_type_issues(df, numeric_columns=None):
    print("\n--- TYPE / VALUE ISSUES ---")
    issues = {}
    if numeric_columns:
        for col in numeric_columns:
            non_numeric = df[pd.to_numeric(df[col], errors="coerce").isna() & df[col].notna()]
            if len(non_numeric) > 0:
                print(f"Column '{col}' has {len(non_numeric)} non-numeric value(s): "
                      f"{non_numeric[col].tolist()}")
                issues[col] = non_numeric[col].tolist()
    return issues


def check_invalid_emails(df, email_column="email"):
    print("\n--- INVALID EMAIL FORMATS ---")
    if email_column not in df.columns:
        return []
    invalid = df[~df[email_column].astype(str).str.match(r"^[\w\.-]+@[\w\.-]+\.\w+$")]
    if len(invalid) > 0:
        print(f"Found {len(invalid)} invalid email(s):")
        print(invalid[[email_column]])
    return invalid[email_column].tolist() if len(invalid) > 0 else []


def check_negative_values(df, column):
    print(f"\n--- NEGATIVE VALUES IN '{column}' ---")
    numeric_col = pd.to_numeric(df[column], errors="coerce")
    negatives = df[numeric_col < 0]
    if len(negatives) > 0:
        print(f"Found {len(negatives)} negative value(s):")
        print(negatives)
    return negatives


def generate_report(df):
    print("=" * 50)
    print("DATA QUALITY REPORT")
    print("=" * 50)
    print(f"Total rows: {len(df)} | Total columns: {len(df.columns)}")

    check_missing_values(df)
    check_duplicates(df)
    check_type_issues(df, numeric_columns=["amount"])
    check_invalid_emails(df, email_column="email")
    check_negative_values(df, column="amount")

    print("\n" + "=" * 50)
    print("Data quality check completed.")
    print("=" * 50)

def run_checker():
    csv_path = create_sample_csv()
    df = pd.read_csv(csv_path)
    generate_report(df)

if __name__ == "__main__":
    run_checker()
