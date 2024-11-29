import streamlit as st
import random

# ゲームのタイトル
st.title("🎯 ダーツシューティング 🎯")

# 簡易ルールの説明
st.subheader("ゲームルール")
st.write("""
1. **基本得点**: ダイス（1d6）を振って出目に応じた得点を計算します。  
   - 出目 1～2: 10点（外周）  
   - 出目 3～4: 15点（中間）  
   - 出目 5～6: 20点（中心）  
2. **命中精度（DEX判定）**: 【DEX】+1d10で判定し、得点を追加/昇格します。  
   - 難易度15: +5点  
   - 難易度20: 1段階昇格（例: 外周 → 中間）  
   - 難易度25: 2段階昇格（例: 外周 → 中心）  
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

# ダーツ投擲ボタン
if st.button("ダーツを投げる！"):
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
    st.subheader("🎯 基本得点")
    st.write(f"出目: {base_roll} → 得点: {base_score}点（{zone}）")

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
    st.subheader("🔧 DEX判定")
    st.write(f"計算式: {dex} + 1d10 → 判定結果: {dex_roll}")
    st.write(f"命中精度ボーナス: +{dex_bonus}点")

    # SPD判定
    spd_roll = spd + random.randint(1, 10)
    multiplier = 1
    if spd_roll >= 15:
        multiplier = 2
    if spd_roll >= 20:
        multiplier = 3
    if spd_roll >= 25:
        multiplier = 5
    st.subheader("💨 SPD判定")
    st.write(f"計算式: {spd} + 1d10 → 判定結果: {spd_roll}")
    st.write(f"スピード倍率: ×{multiplier}")

    # 組み合わせボーナス
    combo_bonus = 0
    if dex_roll >= 20 and spd_roll >= 20:
        combo_bonus = 10
    st.subheader("✨ 組み合わせボーナス")
    if combo_bonus > 0:
        st.write("【DEX】と【SPD】の両方が20以上のため、+10点のボーナスが追加されました！")
    else:
        st.write("組み合わせボーナスなし")

    # 最終得点
    final_score = base_score * multiplier + combo_bonus
    st.subheader("🏆 最終得点")
    st.write(f"計算式: ({base_score} × {multiplier}) + {combo_bonus} → **{final_score}点**")

    # 結果の表示
    st.success("ゲーム完了！次の投擲を試してください。")
