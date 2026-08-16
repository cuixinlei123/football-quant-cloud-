import csv
import time
import requests
from datetime import datetime

# ==============================
# 足球量化系统 V2：接入 Understat xG 数据源
# ==============================

HEADERS = {
    "User‑Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36"
}

def get_understat_league_matches(league: str, season: str):
    """
    league可选 : EPL, La_Liga, Bundesliga, Serie_A, Ligue_1
    season格式: "2025" 代表2025‑26赛季
    """
    url = f"https://understat.com/league/{league}/{season}"
    try:
        resp = requests.get(url, headers=HEADERS, timeout=25)
        resp.raise_for_status()
        return {"status":"ok","html":resp.text}
    except Exception as e:
        return {"status":"error","msg":str(e)}


def main():
    run_time = datetime.now()
    print(f"===== 足球量化系统启动 {run_time} =====")

    # 抓取配置，你可以在这里修改联赛、赛季
    target_league = "EPL"
    target_season = "2025"

    print(f"正在抓取 {target_league} {target_season} 赛季xG数据...")
    res = get_understat_league_matches(target_league, target_season)

    output_file = "football_result.csv"

    # 输出CSV表头
    rows = [
        ["run_datetime","league","season","status","info"]
    ]
    if res["status"] == "ok":
        rows.append([str(run_time), target_league, target_season, "success", "页面抓取成功，下一步解析JSON提取比赛"])
    else:
        rows.append([str(run_time), target_league, target_season, "fail", res["msg"]])

    with open(output_file, "w", newline="", encoding="utf‑8‑sig") as f:
        writer = csv.writer(f)
        writer.writerows(rows)

    print(f"✅ 抓取执行完成，输出文件：{output_file}")
    print("===== 运行结束 =====")

if __name__ == "__main__":
    main()
