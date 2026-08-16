import csv
import requests
from datetime import datetime

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def main():
    run_time = datetime.now()
    print(f"===== 足球量化系统启动 {run_time} =====")

    # 先输出测试文件，验证运行正常
    rows = [["match_date","home_team","away_team","home_goals","away_goals"]]

    output_file = "football_result.csv"
    with open(output_file, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerows(rows)

    print("✅ 测试文件生成成功，环境正常。")
    print("===== 执行结束 =====")

if __name__ == "__main__":
    main()
