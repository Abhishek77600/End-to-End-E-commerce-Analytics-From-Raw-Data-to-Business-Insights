import sqlite3
import os

def run_sql_file(db_path, sql_file_path):
    """Execute SQL queries from a file"""
    conn = sqlite3.connect(db_path)

    with open(sql_file_path, 'r', encoding='utf-8') as f:
        sql_content = f.read()

    # Split by semicolon and execute each statement
    statements = [stmt.strip() for stmt in sql_content.split(';') if stmt.strip()]

    print(f"\n=== Running {os.path.basename(sql_file_path)} ===")

    for i, stmt in enumerate(statements, 1):
        if stmt:
            try:
                print(f"\n-- Query {i} --")
                cursor = conn.execute(stmt)
                if stmt.upper().startswith('SELECT'):
                    results = cursor.fetchall()
                    if results:
                        # Print column headers
                        headers = [desc[0] for desc in cursor.description]
                        print(' | '.join(headers))
                        print('-' * (sum(len(h) for h in headers) + len(headers) * 3 - 1))

                        # Print first 10 rows
                        for row in results[:10]:
                            print(' | '.join(str(cell) for cell in row))

                        if len(results) > 10:
                            print(f"... and {len(results) - 10} more rows")
                    else:
                        print("No results")
                else:
                    print("Query executed successfully")
            except Exception as e:
                print(f"Error executing query {i}: {e}")

    conn.close()

if __name__ == "__main__":
    db_path = "data/processed/ecommerce.db"
    sql_dir = "sql"

    if not os.path.exists(db_path):
        print("Database not found. Please run create_database.py first.")
        exit(1)

    sql_files = [
        "01_data_exploration.sql",
        "02_funnel_analysis.sql",
        "03_conversion_rates.sql",
        "04_cohort_analysis.sql",
        "05_revenue_segmentation.sql"
    ]

    for sql_file in sql_files:
        sql_path = os.path.join(sql_dir, sql_file)
        if os.path.exists(sql_path):
            run_sql_file(db_path, sql_path)
        else:
            print(f"SQL file not found: {sql_path}")

    print("\n=== SQL Analysis Complete ===")