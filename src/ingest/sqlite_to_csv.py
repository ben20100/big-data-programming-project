#데이터 수집 스크립트
#데이터의 형태가 sqlite로 되어있어서 csv 파일 형식으로 변환함

import sqlite3
import pandas as pd
import os

DB_PATH = "data/database.sqlite"
OUTPUT_DIR = "data/csv"

os.makedirs(OUTPUT_DIR, exist_ok=True)
conn = sqlite3.connect(DB_PATH)

query = "SELECT name FROM sqlite_master WHERE type='table';"
tables = pd.read_sql(query, conn)

print(tables)

for table_name in tables['name']:
    df = pd.read_sql(f"SELECT * FROM {table_name}", conn)

    output_path = os.path.join(OUTPUT_DIR, f"{table_name}.csv")

    df.to_csv(output_path, index=False)

    print(f"저장 완료: {output_path}")

conn.close()
