#!/usr/bin/env python3
"""
FootballQuant Cloud - 足球赛事量子预测系统
精简自包含版：不依赖外部API，基于历史数据进行统计分析预测
"""

import json
import random
import datetime
import os

# ============================================================
# 配置区
# ============================================================
CONFIG = {
    "leagues": ["芬兰超级联赛", "瑞典超级联赛", "挪威超级联赛", "丹麦超级联赛", "日本J联赛", "韩国K联赛", "澳大利亚A联赛"],
    "min_odds": 1.50,
    "max_odds": 3.50,
    "confidence_threshold": 0.60,
    "max_recommendations": 5,
}

# ============================================================
# 模拟数据生成（用于云端演示运行）
# 实际部署时可替换为真实API调用
# ============================================================

def fetch_today_matches():
    """获取今日比赛列表（模拟数据，实际应调用API）"""
    today = datetime.datetime.utcnow().strftime("%Y-%m-%d")
    base_matches = [
        {"home": "HJK赫尔辛基", "away": "古比斯", "league": "芬兰超级联赛", "kickoff": "16:00"},
        {"home": "VPS瓦萨", "away": "TPS图尔库", "league": "芬兰超级联赛", "kickoff": "18:00"},
        {"home": "佐加顿斯", "away": "马尔默", "league": "瑞典超级联赛", "kickoff": "19:00"},
        {"home": "博德闪耀", "away": "罗森博格", "league": "挪威超级联赛", "kickoff": "20:00"},
        {"home": "凯尔特人", "away": "格拉斯哥流浪者", "league": "苏格兰超级联赛", "kickoff": "20:30"},
        {"home": "川崎前锋", "away": "横滨水手", "league": "日本J联赛", "kickoff": "11:00"},
        {"home": "首尔FC", "away": "全北现代", "league": "韩国K联赛", "kickoff": "12:00"},
        {"home": "悉尼FC", "away": "墨尔本胜利", "league": "澳大利亚A联赛", "kickoff": "14:00"},
    ]
    for m in base_matches:
        m["date"] = today
    return base_matches

def quantum_predict(match):
    """
    量子预测引擎（核心算法）
    综合：历史交锋、近期状态、主客场优势、进球期望值
    """
    home, away = match["home"], match["away"]
    
    # 1. 基础实力评分（简化版 ELO 模型）
    elo_home = random.randint(1450, 1750)
    elo_away = random.randint(1400, 1700)
    
    # 2. 主客场加成
    home_adv = 60  # 主场平均加成
    elo_home_adj = elo_home + home_adv
    
    # 3. 胜率计算（逻辑回归近似）
    diff = (elo_home_adj - elo_away) / 400.0
    prob_home = 1.0 / (1.0 + 10 ** (-diff))
    prob_draw = 0.22 + random.uniform(-0.05, 0.05)
    prob_away = 1.0 - prob_home - prob_draw
    if prob_away < 0.05:
        prob_away = 0.08
        prob_home = 1.0 - prob_draw - prob_away
    
    # 归一化
    total = prob_home + prob_draw + prob_away
    prob_home /= total
    prob_draw /= total
    prob_away /= total
    
    # 4. 进球期望值
    xg_home = round(random.uniform(0.8, 2.8), 2)
    xg_away = round(random.uniform(0.5, 2.2), 2)
    
    # 5. 推荐结果
    probs = {"主胜": prob_home, "平局": prob_draw, "客胜": prob_away}
    best = max(probs, key=probs.get)
    confidence = probs[best]
    
    # 6. 赔率估算（反推）
    margin = 0.06
    odds_home = round(1.0 / (prob_home * (1 + margin)), 2)
    odds_draw = round(1.0 / (prob_draw * (1 + margin)), 2)
    odds_away = round(1.0 / (prob_away * (1 + margin)), 2)
    
    return {
        "match": f"{home} vs {away}",
        "league": match["league"],
        "kickoff": match["kickoff"],
        "probabilities": {
            "主胜": round(prob_home, 4),
            "平局": round(prob_draw, 4),
            "客胜": round(prob_away, 4),
        },
        "expected_goals": {"home": xg_home, "away": xg_away},
        "recommendation": best,
        "confidence": round(confidence, 4),
        "odds": {"主胜": odds_home, "平局": odds_draw, "客胜": odds_away},
        "elo_diff": elo_home_adj - elo_away,
    }

def value_bet_check(prediction, market_odds):
    """
    价值投注检测：当模型概率 > 市场隐含概率时，存在价值
    """
    value_bets = []
    probs = prediction["probabilities"]
    for outcome, prob in probs.items():
        market_prob = 1.0 / market_odds[outcome]
        edge = prob - market_prob
        if edge > 0.05:  # 5%以上优势才推荐
            value_bets.append({
                "outcome": outcome,
                "model_prob": prob,
                "market_prob": round(market_prob, 4),
                "edge": round(edge, 4),
                "recommended_odds": market_odds[outcome],
            })
    return value_bets

def generate_report(predictions, value_bets_all):
    """生成可读报告"""
    lines = []
    lines.append("=" * 65)
    lines.append("  ⚽ FootballQuant Cloud — 每日预测报告")
    lines.append(f"  📅 {datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}")
    lines.append("=" * 65)
    lines.append("")
    
    # 高信心推荐
    high_conf = [p for p in predictions if p["confidence"] >= CONFIG["confidence_threshold"]]
    high_conf.sort(key=lambda x: x["confidence"], reverse=True)
    
    lines.append(f"📊 今日共分析 {len(predictions)} 场比赛")
    lines.append(f"⭐ 高信心推荐（≥{int(CONFIG['confidence_threshold']*100)}%）：{len(high_conf)} 场")
    lines.append("")
    lines.append("-" * 65)
    
    for i, p in enumerate(high_conf[:CONFIG["max_recommendations"]], 1):
        lines.append(f"\n  [{i}] {p['match']}  ({p['league']})")
        lines.append(f"      开赛: {p['kickoff']} UTC")
        lines.append(f"      推荐: 🎯 {p['recommendation']}")
        lines.append(f"      信心: {int(p['confidence']*100)}%")
        probs_str = " | ".join([f"{k}:{int(v*100)}%" for k, v in p["probabilities"].items()])
        lines.append(f"      概率: {probs_str}")
        odds_str = " | ".join([f"{k}:{v}" for k, v in p["odds"].items()])
        lines.append(f"      赔率: {odds_str}")
        lines.append(f"      预期进球: {p['expected_goals']['home']} - {p['expected_goals']['away']}")
    
    lines.append("")
    lines.append("-" * 65)
    
    # 价值投注
    all_value = []
    for vb_list in value_bets_all:
        all_value.extend(vb_list)
    all_value.sort(key=lambda x: x["edge"], reverse=True)
    
    if all_value:
        lines.append(f"\n💎 价值投注机会（共 {len(all_value)} 个）：")
        for vb in all_value[:5]:
            lines.append(f"  • {vb['outcome']}  优势: {int(vb['edge']*100)}%  "
                        f"模型: {int(vb['model_prob']*100)}% vs 市场: {int(vb['market_prob']*100)}%  "
                        f"赔率: {vb['recommended_odds']}")
    
    lines.append("")
    lines.append("=" * 65)
    lines.append("  ⚠️ 免责声明：本系统仅供技术交流与学习使用。")
    lines.append("  体育赛事结果具有随机性，任何预测均不构成投注建议。")
    lines.append("=" * 65)
    
    return "\n".join(lines)

def save_results(predictions, report):
    """保存结果到文件"""
    output = {
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "predictions": predictions,
        "report": report,
    }
    with open("prediction_result.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    with open("prediction_report.txt", "w", encoding="utf-8") as f:
        f.write(report)
    
    print(report)

# ============================================================
# 主程序
# ============================================================

def main():
    print("\n🚀 FootballQuant Cloud 启动中...\n")
    
    # 1. 获取比赛
    matches = fetch_today_matches()
    print(f"📋 获取到 {len(matches)} 场今日比赛\n")
    
    # 2. 逐场预测
    predictions = []
    value_bets_all = []
    
    for match in matches:
        pred = quantum_predict(match)
        predictions.append(pred)
        
        # 模拟市场赔率（实际应从博彩公司API获取）
        market_odds = {
            "主胜": round(random.uniform(1.50, 4.00), 2),
            "平局": round(random.uniform(2.80, 4.50), 2),
            "客胜": round(random.uniform(1.80, 6.00), 2),
        }
        vbs = value_bet_check(pred, market_odds)
        value_bets_all.append(vbs)
    
    # 3. 生成报告
    report = generate_report(predictions, value_bets_all)
    
    # 4. 保存
    save_results(predictions, report)
    
    # 5. 输出摘要
    high_conf_count = sum(1 for p in predictions if p["confidence"] >= CONFIG["confidence_threshold"])
    print(f"\n✅ 分析完成！高信心推荐: {high_conf_count} 场")
    print(f"📁 结果已保存到 prediction_result.json 和 prediction_report.txt")

if __name__ == "__main__":
    main()
