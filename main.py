import csv
import re
import json
from datetime import datetime
from playwright.sync_api import sync_playwright

# ==============================
# V6 Playwright无头浏览器渲染，获取异步加载xG数据
# ==============================

def parse_understat_matches(league: str, season: str):
    url = f"https://understat.com/league/{league}/{season}"
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(user_agent="Mozilla/5.0 (X11; Linux x86_64) Chrome/124.0.0.0 Safari/537.36")
        page.goto(url, timeout=60000)
        page.wait_for_timeout(4000)
        html = page.content()
        browser.close()

    # 扫描全部JSON.parse
    pattern = r'JSON\.parse\(\s*\'(.*?)\'\s*\)'
    all_chunks = re.findall(pattern, html, re.DOTALL)

    for raw_chunk in all_chunks:
        try:
            decoded = bytes(raw_chunk, "utf-8").decode("unicode_escape")
            data = json.loads(decoded)
            if isinstance(data, list) and len(data) > 0 and "h" in data[0]:
                match_list = []
                for item in data:
                    match_list.append({
                        "match_date": item["datetime"],
                        "home_team": item["h"]["title"],
                        "away_team": item["a"]["title"],
                        "home_goals": item["goals"]["h"],
                        "away_goals": item["goals"]["a"],
                        "home_xg": item["xG"]["h"],
                        "away_xg": item["xG"]["a"],
                        "status": item["isResult"]
                    })
                return match_list
        except Exception:
            continue
    print("❌ 浏览器渲染后仍然找不到比赛数组")
    return []

def main():
    run_time = datetime.now()
    print(f"===== 足球量化系统启动 {run_time} =====")

    target_league = "EPL"
    target_season = "2024"
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
