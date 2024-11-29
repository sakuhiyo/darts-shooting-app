import streamlit as st
import random

# ステータス入力
st.title("🎯 ダーツシューティング 🎯")
dex = st.number_input("【DEX】を入力してください（1～18）", min_value=1, max_value=18, value=10)
spd = st.number_input("【SPD】を入力してください（1～18）", min_value=1, max_value=18, value=10)

if st.button("ダーツを投げる！"):
    # 基本得点の計算
    base_roll = random.randint(1, 6)
    if base_roll <= 2:
        base_score = 10  # 外周
    elif base_roll <= 4:
        base_score = 15  # 中間
    else:
        base_score = 20  # 中心
    st.write(f"🎯 **基本得点: {base_score}点** (1d6の出目: {base_roll})")

    # DEX判定
    dex_roll = dex + random.randint(1, 10)
    dex_bonus = 0
    if dex_roll >= 15:
        dex_bonus = 5
    if dex_roll >= 20:
        dex_bonus = 10
        base_score = min(base_score + 10, 20)  # 1段階昇格
    if dex_roll >= 25:
        dex_bonus = 20
        base_score = min(base_score + 20, 20)  # 2段階昇格
    st.write(f"🔧 **DEX判定: {dex_roll}** → 命中精度ボーナス: +{dex_bonus}点")

    # SPD判定
    spd_roll = spd + random.randint(1, 10)
    multiplier = 1
    if spd_roll >= 15:
        multiplier = 2
    if spd_roll >= 20:
        multiplier = 3
    if spd_roll >= 25:
        multiplier = 5
    st.write(f"💨 **SPD判定: {spd_roll}** → スピード倍率: ×{multiplier}")

    # 組み合わせボーナス
    combo_bonus = 0
    if dex_roll >= 20 and spd_roll >= 20:
        combo_bonus = 10
    st.write(f"✨ **組み合わせボーナス: +{combo_bonus}点**" if combo_bonus > 0 else "✨ 組み合わせボーナスなし")

    # 最終得点
    final_score = base_score * multiplier + combo_bonus
    st.write(f"🏆 **最終得点: {final_score}点**")

    # 結果の表示
    st.success("ゲーム完了！次の投擲を試してください。")
