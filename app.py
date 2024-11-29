import streamlit as st
from datetime import datetime, timezone, timedelta
import random

# 日付システム
JST = timezone(timedelta(hours=9))
today = datetime.now(JST).date()

# セッション状態で日付とプレイ回数を保持
if "last_play_date" not in st.session_state:
    st.session_state["last_play_date"] = None
    st.session_state["play_count"] = 0

# 日付が変わった場合にリセット
if st.session_state["last_play_date"] != today:
    st.session_state["last_play_date"] = today
    st.session_state["play_count"] = 0

# ゲームルールの表示
st.title("🎯 ダーツシューティング 🎯")
st.subheader("ゲームルール")
st.write("""
1. **基本得点**: ダイス（1d6）を振って出目に応じた得点を計算します。  
   - 出目 1～2: 10点（外周）  
   - 出目 3～4: 15点（中間）  
   - 出目 5～6: 20点（中心）  
2. **命中精度（DEX判定）**: 【DEX】+1d10で判定し、得点を追加/昇格します。  
   - 難易度15: +5点  
   - 難易度20: 1段階昇格（例: 外周 → 中間、中間 → 中心）  
   - 難易度25: 2段階昇格（例: 外周 → 中間 → 中心）  
   - 既に中心（20点）の場合、+10点ずつ加点  
3. **スピード（SPD判定）**: 【SPD】+1d10で判定し、得点倍率を決定します。  
   - 難易度15: ×2  
   - 難易度20: ×3  
   - 難易度25: ×5  
4. **組み合わせボーナス**: 【DEX】と【SPD】の判定が両方20以上の場合、+10点。  
""")

# ステータス入力
st.sidebar.header("ステータス入力")
dex = st.sidebar.number_input("【DEX】を入力してください（1～18）", min_value=1, max_value=18, value=10)
spd = st.sidebar.number_input("【SPD】を入力してください（1～18）", min_value=1, max_value=18, value=10)

# プレイ回数の表示
st.write(f"本日プレイ済み回数: {st.session_state['play_count']}回")
st.write("1日に1回のみプレイ可能です。")

# プレイ処理
if st.session_state["play_count"] < 1 and st.button("プレイする"):
    # 基本得点の計算
    base_roll = random.randint(1, 6)
    if base_roll <= 2:
        base_score = 10  # 外周
        zone = "外周"
    elif base_roll <= 4:
        base_score = 15  # 中間
        zone = "中間"
    else:
        base_score = 20  # 中心
        zone = "中心"

    # 基礎得点を表示
    st.subheader("🎯 結果")
    st.write(f"出目: {base_roll} → 基礎得点: {base_score}点（{zone}）")

    # DEX判定
    dex_random = random.randint(1, 10)  # 1d10の結果
    dex_roll = dex + dex_random
    st.write(f"DEX判定: {dex} + 1d10({dex_random}) → {dex_roll}")
    if dex_roll >= 15 and dex_roll < 20:
        st.write("昇格なし: +5点を加算")
        base_score += 5
    elif dex_roll >= 20 and dex_roll < 25:
        if base_score < 20:  # 昇格可能
            base_score = min(base_score + 10, 20)  # 1段階昇格
        else:
            base_score += 10  # 中心で+10点
    elif dex_roll >= 25:
        if base_score < 20:  # 昇格可能
            base_score = min(base_score + 20, 20)  # 2段階昇格
        else:
            base_score += 10  # 中心で+10点

    # 昇格後得点のラベル付け
    if base_score == 10:
        final_zone = "外周"
    elif base_score == 15:
        final_zone = "中間"
    elif base_score == 20 or base_score == 25:  # 25も「中心」とする
        final_zone = "中心"
    elif base_score == 30:
        final_zone = "中心+"
    elif base_score == 40:
        final_zone = "中心++"
    else:
        final_zone = "不明"  # その他の値に対する保険

    st.write(f"昇格後得点: {base_score}点（{final_zone}）")

    # SPD判定
    spd_random = random.randint(1, 10)  # 1d10の結果
    spd_roll = spd + spd_random
    multiplier = 1
    if spd_roll >= 15:
        multiplier = 2
    if spd_roll >= 20:
        multiplier = 3
    if spd_roll >= 25:
        multiplier = 5
    st.write(f"SPD判定: {spd} + 1d10({spd_random}) → {spd_roll} → 倍率: ×{multiplier}")

    # 組み合わせボーナス
    combo_bonus = 0
    if dex_roll >= 20 and spd_roll >= 20:
        combo_bonus = 10
    st.write(f"組み合わせボーナス: +{combo_bonus}点")

    # 最終得点計算
    final_score = base_score * multiplier + combo_bonus
    st.write(f"最終得点: **{final_score}点**")

    # プレイ回数を増やす
    st.session_state["play_count"] += 1
    st.success("プレイしました！次の日までお待ちください。")
elif st.session_state["play_count"] >= 1:
    st.error("本日のプレイ回数を超えました。")
