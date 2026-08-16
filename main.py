import csv
import re
import json
import requests
from datetime import datetime

# ==============================
# 足球量化系统 V3 Understat完整解析
# ==============================
HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36"
}

def parse_understat_matches(league: str, season: str):
    url = f"https://understat.com/league/{league}/{season}"
    resp = requests.get(url, headers=HEADERS, timeout=30)
    html = resp.text
    # 提取隐藏JSON字符串
    pattern = r"datesData\s*=\s*JSON\.parse\('([^']+)'\)"
    match = re.search(pattern, html)
    if not match:
        return []
    raw = match.group(1).encode("utf-8").decode("unicode_escape")
    data = json.loads(raw)
    result = []
    for item in data:
        result.append({
            "match_date": item["datetime"],
            "home_team": item["h"]["title"],
            "away_team": item["a"]["title"],
            "home_goals": item["goals"]["h"],
            "away_goals": item["goals"]["a"],
            "home_xg": item["xG"]["h"],
            "away_xg": item["xG"]["a"],
            "status": item["isResult"]
        })
    return result

def main():
    run_time = datetime.now()
    print(f"===== 足球量化系统启动 {run_time} =====")

    target_league = "EPL"
    target_season = "2025"
    print(f"抓取 {target_league} {target_season} xG赛事数据...")
    match_list = parse_understat_matches(target_league, target_season)

    output_file = "football_result.csv"
    rows = [
        ["match_date","home_team","away_team","home_goals","away_goals","home_xg","away_xg","status"]
    ]
    for m in match_list:
        rows.append([
            m["match_date"],
            m["home_team"],
            m["away_team"],
            m["home_goals"],
            m["away_goals"],
            m["home_xg"],
            m["away_xg"],
            m["status"]
        ])

    with open(output_file, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerows(rows)

    print(f"✅ 抓取完成，一共 {len(match_list)} 场比赛，输出：{output_file}")
    print("===== 运行结束 =====")

if __name__ == "__main__":
    main()
