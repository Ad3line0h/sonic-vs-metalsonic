import random
import time
import os
import msvcrt
import readchar
import unicodedata

CLEAR = "cls" if os.name == "nt" else "clear"

# ──────────────────────────────────────────────
# 캐릭터 스탯
# ──────────────────────────────────────────────
sonic = {"name": "소닉", "hp": 250, "max_hp": 250, "atk": 35, "rings": 0}
metal = {"name": "메탈 소닉", "hp": 300, "max_hp": 300, "atk": 30,
         "overdrive_used": False}

# ──────────────────────────────────────────────
# 캐릭터 ASCII 도트
# ──────────────────────────────────────────────
SONIC = [
    " <(\\_/) ",
    " < ･ω･) ",
    "  (>o<) ",
    "  /   \\ ",
]
METAL = [
    " (\\_/) ",
    " (⩌ ⩌ > ",
    " >[#]< ",
    " /   \\ ",
]

STAGE_W = 40   # 무대 안쪽 가로 폭
CHAR_W = 7     # 캐릭터 한 줄의 폭


# ──────────────────────────────────────────────
# HP 막대 문자열 생성 (무대 안에 넣기 위해 print 대신 반환)
# ──────────────────────────────────────────────
def hp_bar(char):
    """캐릭터 HP를 막대 문자열로 만들어 반환한다."""
    bar_len = 14
    ratio = max(char["hp"], 0) / char["max_hp"]
    filled = int(bar_len * ratio)
    bar = "■" * filled + "□" * (bar_len - filled)
    return f"{char['name']:<7}[{bar}]{max(char['hp'], 0):>3}"


# ──────────────────────────────────────────────
# 무대 한 프레임 (HP·링 포함) 그리기
# ──────────────────────────────────────────────
def vlen(text):
    """문자열의 '실제 터미널 표시 폭'을 잰다. 한글·이모지는 2칸으로 계산."""
    width = 0
    for ch in text:
        # East Asian Width가 W(Wide)/F(Fullwidth)면 2칸, 나머지는 1칸
        if unicodedata.east_asian_width(ch) in ("W", "F"):
            width += 2
        else:
            width += 1
    return width


def pad_line(text, total):
    """text 뒤에 공백을 채워 표시 폭이 정확히 total칸이 되게 만든다."""
    pad = total - vlen(text)
    return text + " " * max(pad, 0)


def hp_bar(char):
    """캐릭터 HP를 막대 문자열로 만들어 반환한다."""
    bar_len = 14
    ratio = max(char["hp"], 0) / char["max_hp"]
    filled = int(bar_len * ratio)
    bar = "■" * filled + "□" * (bar_len - filled)
    return f"{char['name']} [{bar}] {max(char['hp'], 0)}"


def draw_stage(sonic_x, metal_x, effect=""):
    """HP·링이 박힌 닫힌 무대 한 프레임을 그린다."""
    os.system(CLEAR)
    top = "╔" + "═" * STAGE_W + "╗"
    bottom = "╚" + "═" * STAGE_W + "╝"

    print("  🌳 GREEN FOREST - RIVAL BATTLE 🌳")
    print(top)

    # 상단 UI 줄: pad_line으로 실제 폭을 맞춰 오른쪽 변을 정확히 닫는다
    print("║ " + pad_line(hp_bar(sonic), STAGE_W - 1) + "║")
    print("║ " + pad_line(hp_bar(metal), STAGE_W - 1) + "║")
    star = " ⭐SUPER!" if sonic["rings"] >= 100 else ""
    print("║ " + pad_line(f"💍 {sonic['rings']}/100{star}", STAGE_W - 1) + "║")
    print("║" + "─" * STAGE_W + "║")

    # 이펙트 줄 (effect도 폭 계산 후 가운데 정렬)
    pad = STAGE_W - vlen(effect)
    left = pad // 2
    print("║" + " " * left + effect + " " * (pad - left) + "║")

    # 캐릭터 4줄 (모두 1칸 문자)
    for i in range(4):
        row = [" "] * STAGE_W
        for j, ch in enumerate(SONIC[i]):
            if 0 <= sonic_x + j < STAGE_W:
                row[sonic_x + j] = ch
        for j, ch in enumerate(METAL[i]):
            if 0 <= metal_x + j < STAGE_W:
                row[metal_x + j] = ch
        print("║" + "".join(row) + "║")
    print(bottom)


# 기본 위치 상수
SONIC_HOME = 3
METAL_HOME = STAGE_W - CHAR_W - 3


def stage_idle(effect=""):
    """기본 대치 자세를 그린다."""
    draw_stage(SONIC_HOME, METAL_HOME, effect)


# ══════════════════════════════════════════════
# 무대 위 애니메이션들
# ══════════════════════════════════════════════
def anim_sonic_rush(effect_text="💥 CRASH!"):
    """소닉이 메탈 앞까지 돌진했다가 돌아온다."""
    target = METAL_HOME - 8
    for x in range(SONIC_HOME, target, 3):
        draw_stage(x, METAL_HOME)
        time.sleep(0.03)
    draw_stage(target, METAL_HOME, effect_text)
    time.sleep(0.35)
    for x in range(target, SONIC_HOME, -4):
        draw_stage(x, METAL_HOME)
        time.sleep(0.025)
    stage_idle()


def anim_metal_rush(effect_text="💥 SLAM!"):
    """메탈이 소닉 앞까지 돌진했다가 돌아온다."""
    target = SONIC_HOME + 8
    for x in range(METAL_HOME, target, -3):
        draw_stage(SONIC_HOME, x)
        time.sleep(0.03)
    draw_stage(SONIC_HOME, target, effect_text)
    time.sleep(0.35)
    for x in range(target, METAL_HOME, 4):
        draw_stage(SONIC_HOME, x)
        time.sleep(0.025)
    stage_idle()


def anim_charge(effect_label="⚡CHARGING⚡"):
    """제자리에서 에너지를 모으는 충전 연출."""
    for i in range(8):
        sym = "★" * (i + 1)
        stage_idle(f"{effect_label} {sym}")
        time.sleep(0.1)
    stage_idle("✨ BURST!! ✨")
    time.sleep(0.3)


def anim_shake(effect_text="HIT!"):
    """무대 전체가 좌우로 흔들리는 피격 연출."""
    for off in [0, 3, 0, 4, 1, 0]:
        os.system(CLEAR)
        print("\n" + " " * off + f"💥 {effect_text} 💥\n")
        draw_stage(SONIC_HOME + (off // 2), METAL_HOME - (off // 2))
        time.sleep(0.05)
    stage_idle()


# ──────────────────────────────────────────────
# 판단 시간 (선택지 뜨기 전 딜레이)
# ──────────────────────────────────────────────
def ready_pause(seconds=2.5):
    """선택지가 뜨기 전 판단 시간을 카운트다운으로 보여준다."""
    steps = int(seconds / 0.1)
    for i in range(steps, 0, -1):
        dots = "●" * i + "○" * (steps - i)
        print(f"\r🤔 상황 판단... {i * 0.1:3.1f}초  [{dots}]",
              end="", flush=True)
        time.sleep(0.1)
    print(f"\r⚔️  지금이다! 행동을 선택하라!{' ' * 30}")


# ──────────────────────────────────────────────
# 제한시간 내 즉시 스킬 선택
# ──────────────────────────────────────────────
def timed_skill_select(timeout=6.0):
    """제한시간 동안 1~5 키를 즉시 입력받는다. 초과 시 None."""
    print("\n[소닉의 턴] 키를 눌러 즉시 행동! (엔터 불필요)")
    print(" 1)스핀대시  2)회피  3)도발  4)호밍어택", end="")
    print("  5)⭐슈퍼화" if sonic["rings"] >= 100 else "")

    start = time.time()
    valid = ("1", "2", "3", "4", "5")
    while time.time() - start < timeout:
        remaining = timeout - (time.time() - start)
        if msvcrt.kbhit():
            key = readchar.readkey()
            if key in valid:
                print(f"\r✅ 선택: {key}번!{' ' * 25}")
                return key
        print(f"\r⏳ 남은 시간: {remaining:4.1f}초   ", end="", flush=True)
        time.sleep(0.02)
    print(f"\r⏰ 시간 초과! 머뭇거리다 빈틈을 보였다...{' ' * 10}")
    return None


# ──────────────────────────────────────────────
# 메탈의 다음 행동 예고
# ──────────────────────────────────────────────
def telegraph_metal():
    """메탈의 다음 스킬을 정하고 예고 문장과 카운터 키를 반환한다."""
    skills = {
        "스핀 대시": {"hint": "메탈이 몸을 만다... 정면 돌진! (2:회피로 흘려라)",
                   "counter": "2"},
        "스핀 점프": {"hint": "메탈이 솟구친다! (4:호밍 어택으로 받아쳐라)",
                   "counter": "4"},
        "블랙 실드": {"hint": "메탈이 실드를 두르려 한다! (1:스핀대시로 깨라)",
                   "counter": "1"},
    }
    name = random.choice(list(skills.keys()))
    print(f"\n⚠️  {skills[name]['hint']}")
    return name, skills[name]["counter"]


# ──────────────────────────────────────────────
# 플레이어 행동 처리
# ──────────────────────────────────────────────
def player_action(key, counter_key):
    """선택한 스킬을 수행한다. 카운터면 보너스. 회피 여부를 반환한다."""
    dodging = False
    is_counter = (key == counter_key)

    if key == "1":  # 스핀 대시
        bonus_txt = "💥 PERFECT!" if is_counter else "💥 CRASH!"
        anim_sonic_rush(bonus_txt)
        dmg = sonic["atk"] + random.randint(5, 15) + (20 if is_counter else 0)
        metal["hp"] -= dmg
        if is_counter:
            print("🎯 완벽한 타이밍! 실드를 깨부쉈다!")
        print(f"💥 스핀 대시! {dmg} 데미지!")
        sonic["rings"] = min(sonic["rings"] + random.randint(5, 15), 100)

    elif key == "2":  # 회피
        dodging = True
        stage_idle("🌀 DODGE!")
        time.sleep(0.4)
        print("🌀 소닉이 회피 태세를 취한다!")
        if is_counter:
            print("✨ 돌진을 흘려보낼 완벽한 자세!")

    elif key == "3":  # 도발
        stage_idle("😎 TAUNT~")
        time.sleep(0.4)
        bonus = random.randint(15, 30)
        sonic["rings"] = min(sonic["rings"] + bonus, 100)
        print(f"😎 도발! 여유롭게 링 {bonus}개 획득!")

    elif key == "4":  # 호밍 어택
        anim_sonic_rush("✦ HOMING!")
        if random.random() < 0.75 or is_counter:
            dmg = sonic["atk"] + random.randint(15, 25) + (20 if is_counter else 0)
            metal["hp"] -= dmg
            if is_counter:
                print("🎯 공중의 메탈을 정확히 포착했다!")
            print(f"💥 호밍 어택! {dmg} 데미지!")
        else:
            print("❌ 호밍 어택이 빗나갔다!")
        sonic["rings"] = min(sonic["rings"] + random.randint(5, 15), 100)

    elif key == "5" and sonic["rings"] >= 100:  # 슈퍼화
        anim_charge("⚡SUPER⚡")
        sonic["rings"] = 0
        dmg = sonic["atk"] * 3 + random.randint(20, 40)
        metal["hp"] -= dmg
        anim_shake("SUPER SONIC!")
        print(f"🌟 슈퍼 소닉 변신! 황금빛 폭발! {dmg} 데미지!")

    return dodging


# ──────────────────────────────────────────────
# 메탈의 공격 처리
# ──────────────────────────────────────────────
def metal_attack(skill, player_dodging):
    """예고한 스킬로 공격한다. 오버드라이브 조건도 검사한다."""
    hp_lost = 1 - (metal["hp"] / metal["max_hp"])

    if hp_lost >= 0.8 and not metal["overdrive_used"]:  # 궁극기
        metal["overdrive_used"] = True
        anim_charge("⚡OVERDRIVE⚡")
        dmg = metal["atk"] * 2 + random.randint(20, 35)
        if player_dodging:
            stage_idle("🌀 DODGED!")
            time.sleep(0.4)
            print("🌀 소닉이 종이 한 장 차이로 피했다!")
        else:
            sonic["hp"] -= dmg
            anim_shake("OVERDRIVE!")
            print(f"⚡ 오버드라이브 직격! {dmg} 데미지!")
        return

    if skill == "블랙 실드":  # 회복
        anim_charge("🛡️SHIELD🛡️")
        heal = random.randint(15, 25)
        metal["hp"] = min(metal["hp"] + heal, metal["max_hp"])
        print(f"🛡️  메탈이 실드로 {heal} 회복했다!")
        return

    dmg = metal["atk"] + random.randint(0, 12)
    if player_dodging:
        stage_idle("🌀 DODGED!")
        time.sleep(0.4)
        print(f"🌀 소닉이 메탈의 {skill}을(를) 회피했다!")
    else:
        anim_metal_rush()
        sonic["hp"] -= dmg
        print(f"🌀 메탈의 {skill}! 소닉에게 {dmg} 데미지!")


# ──────────────────────────────────────────────
# 승패 판정
# ──────────────────────────────────────────────
def check_winner():
    """HP가 0 이하인 쪽을 확인해 결과 메시지를 반환한다. 없으면 None."""
    if sonic["hp"] <= 0:
        return "💀 소닉이 쓰러졌다... 메탈 소닉의 승리!"
    if metal["hp"] <= 0:
        return "🏆 메탈 소닉 격파! 소닉의 승리!"
    return None


# ──────────────────────────────────────────────
# 메인 게임 루프
# ──────────────────────────────────────────────
def main():
    """무대 → 예고 → 판단시간 → 즉시선택 → 메탈 반격 순서로 진행한다."""
    turn = 1
    while True:
        # 1. 무대(대치 자세 + HP/링) 표시
        stage_idle()
        print(f"========== TURN {turn} ==========")

        # 2. 메탈이 다음 행동을 예고
        skill, counter_key = telegraph_metal()

        # 3. 2.5초 판단 시간 (상자 아래 한 칸 띄움)
        print()
        ready_pause(2.5)

        # 4. 제한시간 즉시 선택
        key = timed_skill_select(timeout=6.0)

        # 5. 행동 수행
        dodging = False
        if key is not None:
            dodging = player_action(key, counter_key)

        if check_winner():
            print("\n" + check_winner())
            break

        # 6. 메탈 반격
        time.sleep(0.6)
        metal_attack(skill, dodging)
        if check_winner():
            print("\n" + check_winner())
            break

        turn += 1
        time.sleep(1.0)  # 다음 턴 전 호흡
    print("\n게임 종료. 수고했어요!")


if __name__ == "__main__":
    main()