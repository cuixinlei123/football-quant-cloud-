import csv
import time
import pandas as pd
import requests
from datetime import datetime

HEADERS = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def fetch_fbref_season(league_url):
    tables = pd.read_html(league_url)
    match_table = tables[1]
    match_table = match_table.dropna(subset=["Date"])
    return match_table

def main():
    run_time = datetime.now()
    print(f"===== 足球量化系统启动 {run_time} =====")

    # 英超2024‑2025赛季FBref地址
    url = "https://fbref.com/en/comps/9/2024-2025/schedule/2024-2025-Premier-League-Scores-and-Fixtures"
    print(f"正在抓取：{url}")

    df = fetch_fbref_season(url)

    # 导出CSV
    out_file = "football_result.csv"
    df.to_csv(out_file, index=False, encoding="utf-8-sig")

    print(f"✅ 抓取完毕，总场次：{len(df)}")
    print(f"✅ 文件输出：{out_file}")
    print("===== 执行结束 =====")

if __name__ == "__main__":
    main()
