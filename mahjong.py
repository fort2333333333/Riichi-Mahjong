from itertools import combinations
import re
import streamlit as st
import random


def sim_meld(sim_meld_input):
    s_letter = ""
    for sim_letter in ["s","z","m","p"]:
        if sim_letter in sim_meld_input:
            s_letter = sim_letter
    s_number = ""
    sim_a = ""
    if "a" in sim_meld_input:
        sim_a = "a"
        sim_meld_input.replace("a","")
    if s_letter:
        for sim_number in sim_meld_input:
            if sim_number in "0123456789":
                s_number += sim_number
        s_number += s_letter
        s_number += sim_a
    return s_number


def meld_check(meld_check_meld):
    if len(meld_check_meld) == 3:
        if meld_check_meld[0][1] == meld_check_meld[1][1] == meld_check_meld[2][1]:
            meld_check_meld_number = [int(meld_check_meld[0][0]),int(meld_check_meld[1][0]),int(meld_check_meld[2][0])]
            meld_check_meld_number.sort()
            if meld_check_meld_number in [[1,2,3],[2,3,4],[3,4,5],[4,5,6],[5,6,7],[6,7,8],[7,8,9]]:
                if meld_check_meld[0][1] != "z":
                    return True
                else:
                    return False
            elif meld_check_meld_number[0] == meld_check_meld_number[1] == meld_check_meld_number[2]:
                return True
            else:
                return False
        else:
            return False
    elif len(meld_check_meld) == 4:
        if meld_check_meld[0] == meld_check_meld[1] == meld_check_meld[2] == meld_check_meld[3]:
            return True
        else:
            return False
    elif len(meld_check_meld) == 5:
        if meld_check_meld[0] == meld_check_meld[1] == meld_check_meld[2] == meld_check_meld[3] and meld_check_meld[4] == "a":
            return True
        else:
            return False
    else:
        return False


def cal_han(cal_han_user_input, cal_double, cal_lan, cal_output, cal_allow_mode):
    st_han_output = ""
    if cal_lan == 0:
        ron_tsumo = {"0": "和", "1": "自摸"}
    else:
        ron_tsumo = {"0": "Ron", "1": "Tsumo"}
    def print_total(print_total_total_tile, print_lan):
        re_st_han_output = ""
        match print_total_total_tile[0]:
            case "M":
                #print(f"一般和牌型 {ron_tsumo[info[0]]}：{ron_tsumo_tile}")
                re_st_han_output += f"{["一般和牌型","Standard Winning Hand"][print_lan]}  {ron_tsumo[info[0]]}：{ron_tsumo_tile}\n"
                #print("手牌：", end="")
                re_st_han_output += f"{["手牌：","Hand："][print_lan]}"
                for print_total_meld in print_total_total_tile[1]:
                    #print(print_total_meld, end=" ")
                    re_st_han_output += f"{sim_meld(print_total_meld)} "
                #print("\n副露：", end="")
                re_st_han_output += f"\n{["副露：","Meld："][print_lan]}"
                for print_total_meld in print_total_total_tile[2]:
                    #print(print_total_meld, end=" ")
                    re_st_han_output += f"{sim_meld(print_total_meld)} "
                if print_total_total_tile[2]:
                    #print()
                    re_st_han_output += "\n"
                else:
                    #print("(无)")
                    re_st_han_output += f"{["(无)","(None)"][print_lan]}\n"
            case "Q":
                #print(f"七对子 {ron_tsumo[info[0]]}：{ron_tsumo_tile}")
                re_st_han_output += f"{["七对子","Chiitoitsu Hand"][print_lan]}  {ron_tsumo[info[0]]}：{ron_tsumo_tile}\n"
                #print("手牌：", end="")
                re_st_han_output += f"{["手牌：","Hand："][print_lan]}"
                arranged_q = []
                for q_type in "mpsz":
                    for toitsu in print_total_total_tile[1]:
                        if toitsu[-1] == q_type:
                            arranged_q.append(toitsu)
                print_total_total_tile[1] = arranged_q
                for print_total_meld in print_total_total_tile[1]:
                    #print(print_total_meld, end=" ")
                    re_st_han_output += f"{sim_meld(print_total_meld)} "
                #print()
                re_st_han_output += "\n"
            case "G":
                #print(f"国士无双 {ron_tsumo[info[0]]}：{ron_tsumo_tile}")
                re_st_han_output += f"{["国士无双","Kokushi Muso Hand"][print_lan]}  {ron_tsumo[info[0]]}：{ron_tsumo_tile}\n"
                #print("手牌：", end="")
                re_st_han_output += f"{["手牌：","Hand："][print_lan]}"
                arranged_g = []
                for g_type in "mpsz":
                    for g_tile in print_total_total_tile[1]:
                        if g_tile[-1] == g_type:
                            arranged_g.append(g_tile)
                print_total_total_tile[1] = arranged_g
                for print_total_meld in print_total_total_tile[1]:
                    re_st_han_output += f"{print_total_meld} "
                    #print(print_total_meld, end=" ")
                #print()
        #print("-" * 50)
        st.text(re_st_han_output)

    # 获取手牌信息
    user_input = cal_han_user_input
    # 手牌（和的牌放最后），副露（面子间用"."隔开），其他信息，宝牌（宝牌+里宝牌（如果立直）+拔北宝牌（三麻）），场风+自风
    # 其他信息：（0：荣，1：自摸）（0：没立直，1：立直，2：双立直）（0：无一发，1：立一发）（0：无枪杠，1：枪杠，2：岭上开花）（0：无天和，1：天和，2:地和，3：海底摸月/河底捞鱼）
    # 例:2p3p4p5p6p7p4s5s5s6s7s6z6z3s,,01,1m6s,1z3z

    user_input.replace(" ", "")
    user_input = user_input.lower()

    # 将手牌信息拆解成hand(手牌),melded(副露),info(其他信息),dora(宝牌),wind(风向)五个变量
    #if user_input.count(",") == 4:
    hand, melded, info, dora, wind = user_input.split(",")
    #else:
        #return [False,0]
    red_dora = []

    # 处理hand(手牌):使用list存储手牌里每张牌
    hand = re.findall(r"[0-9][mpsz]", hand)
    for index, tile in enumerate(hand):
        if tile[0] == "0":
            hand[index] = "5" + tile[1]
            red_dora.append(tile)
    ron_tsumo_tile = hand[-1]

    # 处理hand(手牌):决定雀头
    possible_pair = []
    for tile in hand:
        if hand.count(tile) > 1:
            possible_pair.append(tile)
    possible_pair = set(possible_pair)
    possible_pair = list(possible_pair)  # 列表→集合→列表是为了去重
    if len(possible_pair) >= 7:
        chiitoi = True
    else:
        chiitoi = False

    # 处理hand(手牌):根据牌的种类(万索饼字)分组
    grouped_hand = [[], [], [], []]
    group_order = "mpsz"
    for tile in hand:
        grouped_hand[group_order.index(tile[1])].append(tile)

    # 处理hand(手牌):再次筛选雀头
    for index, pair in enumerate(possible_pair):
        s_hand = hand.copy()
        s_hand.remove(pair)
        s_hand.remove(pair)
        s_hand = "".join(s_hand)
        if s_hand.count("m") % 3 != 0 or s_hand.count("p") % 3 != 0 or s_hand.count("z") % 3 != 0 or s_hand.count(
                "s") % 3 != 0:
            possible_pair[index] = ""
    while "" in possible_pair:
        possible_pair.remove("")

    # 处理hand(手牌):筛选满足条件的面子
    all_combinations = [[], [], [], []]
    satisfied_meld = [[], [], [], []]
    for index, meld_type in enumerate(grouped_hand):
        all_combinations[index] = list(combinations(meld_type, 3))
    for index, meld_type in enumerate(all_combinations):
        for meld in meld_type:
            meld = list(meld)
            meld.sort()
            if meld_check(meld) and satisfied_meld[index].count(meld) < 4:
                satisfied_meld[index].append(meld)

    # 处理hand(手牌):组合所有满足条件的面子/雀头
    satisfied_hand = []
    for pair_index, pair in enumerate(possible_pair):
        satisfied_hand.append([[], [], [], [], [pair + pair]])
        for index, meld_type in enumerate(grouped_hand):
            for meld_type_combination in combinations(satisfied_meld[index], len(meld_type) // 3):
                meld_type_combination = sorted(meld_type_combination)
                if meld_type_combination:
                    if pair[1] == meld_type_combination[0][0][1]:
                        all_meld = [pair, pair]
                    else:
                        all_meld = []
                else:
                    all_meld = []
                for meld in meld_type_combination:
                    for tile in meld:
                        all_meld.append(tile)
                all_meld.sort()
                if all_meld == sorted(grouped_hand[index]):
                    meld_type_combination_string = ""
                    for meld in meld_type_combination:
                        for tile in meld:
                            meld_type_combination_string += tile
                    if meld_type_combination_string not in satisfied_hand[pair_index][index]:
                        satisfied_hand[pair_index][index].append(meld_type_combination_string)

    grouped_satisfied_hand = []
    for index, melds in enumerate(satisfied_hand):
        for i in range(4):
            if not melds[i]:
                satisfied_hand[index][i].append("")
    for melds in satisfied_hand:
        for m_meld in melds[0]:
            for s_meld in melds[1]:
                for p_meld in melds[2]:
                    for z_meld in melds[3]:
                        if len(m_meld + s_meld + p_meld + z_meld + melds[4][0]) == len(hand) * 2:
                            grouped_satisfied_hand.append(m_meld + s_meld + p_meld + z_meld + melds[4][0] + "M")

    if not grouped_satisfied_hand and len(hand) == 2 and possible_pair:
        grouped_satisfied_hand.append(possible_pair[0] * 2)

    if chiitoi:
        chiitoi_hand = ""
        for tile in sorted(hand):
            chiitoi_hand += tile
        grouped_satisfied_hand.append(chiitoi_hand + "Q")

    kokushi_check = ["1m", "9m", "1s", "9s", "1p", "9p", "1z", "2z", "3z", "4z", "5z", "6z", "7z"]
    kokushi_pair_check = ["1m", "9m", "1s", "9s", "1p", "9p", "1z", "2z", "3z", "4z", "5z", "6z", "7z"]
    kokushi_count_check = 0
    kokushi_pair_count_check = 0
    kokushi_hand = ""
    for tile in hand:
        if tile in kokushi_check:
            kokushi_check.remove(tile)
            kokushi_count_check += 1
        elif tile in kokushi_pair_check:
            kokushi_pair_count_check += 1
    if kokushi_count_check == 13 and kokushi_pair_count_check == 1:
        for tile in sorted(hand):
            kokushi_hand += tile
        grouped_satisfied_hand.append(kokushi_hand + "G")

    for index, possible_hand in enumerate(grouped_satisfied_hand):
        match possible_hand[-1]:
            case "M":
                grouped_satisfied_hand[index] = []
                for i in range(len(possible_hand) // 6):
                    grouped_satisfied_hand[index].append(possible_hand[i * 6:i * 6 + 6])
                else:
                    grouped_satisfied_hand[index].append(possible_hand[-5:-1])
                    grouped_satisfied_hand[index].append(possible_hand[-1])
            case "Q":
                grouped_satisfied_hand[index] = []
                for i in range(7):
                    grouped_satisfied_hand[index].append(possible_hand[i * 4:i * 4 + 4])
                else:
                    grouped_satisfied_hand[index].append(possible_hand[-1])
            case "G":
                grouped_satisfied_hand[index] = []
                for i in range(14):
                    grouped_satisfied_hand[index].append(possible_hand[i * 2:i * 2 + 2])
                else:
                    grouped_satisfied_hand[index].append(possible_hand[-1])
                pass

    # 处理melded(副露):使用list存储副露区的每个面子和每张牌
    if "." in melded:
        melded = melded.split(".")
    else:
        melded = [melded]
    for index, meld in enumerate(melded):
        if len(meld) == 9:
            melded[index] = re.findall(r"[0-9][mpsz]|a", meld)
        else:
            melded[index] = re.findall(r"[0-9][mpsz]", meld)
    for index, meld in enumerate(melded):
        for tile_index, tile in enumerate(meld):
            if tile[0] == "0":
                melded[index][tile_index] = "5" + tile[1]
                red_dora.append(tile)

    # 处理melded(副露):检查每个面子并存储
    menzen = True
    checked_melded = []
    for meld in melded:
        meld = sorted(meld)
        if meld_check(meld):
            checked_melded.append("".join(meld))
            if len(meld) != 5:
                menzen = False

    # 合并han(手牌)和melded(副露)并检查
    raw_total_tile = []
    for tile in hand:
        raw_total_tile.append(tile)
    for tile in checked_melded:
        raw_total_tile.append(tile[0:2])
        raw_total_tile.append(tile[2:4])
        raw_total_tile.append(tile[4:6])
        if len(tile) > 6:
            raw_total_tile.append(tile[6:8])
    raw_total_tile = sorted(raw_total_tile)

    all_total_tile = []
    checked_total_tile = []

    for index, checked_hand in enumerate(grouped_satisfied_hand):
        all_total_tile.append([])
        all_total_tile[index].append(checked_hand[-1])
        all_total_tile[index].append(checked_hand[:-1])
        all_total_tile[index].append(checked_melded)

    for total_tile in all_total_tile:
        match total_tile[0]:
            case "M":
                if len(total_tile[1]) + len(total_tile[2]) == 5:
                    checked_total_tile.append(total_tile)
            case "Q":
                if len(total_tile[1]) == 7 and len(total_tile[2]) == 0:
                    checked_total_tile.append(total_tile)
            case "G":
                if len(total_tile[1]) == 14 and len(total_tile[2]) == 0:
                    checked_total_tile.append(total_tile)

    if not checked_total_tile:
        #print("哥么这啥牌啊")
        if cal_output:
            raise Exception
        else:
            return [False,-1]

    # 处理info(其他信息):
    for i in range(5 - len(info)):
        info = info + "0"

    # 处理dora(宝牌):
    dora = re.findall(r"[1-9][mpsz]", dora)

    # 处理wind(风向):
    wind = re.findall(r"[1-4]z", wind)

    # 计番(役满)
    yakuman = []
    yakuman_han = []
    for index, total_tile in enumerate(checked_total_tile):
        yakuman.append([])
        yakuman_han.append(0)

        total_all_meld = []
        if total_tile[0] == "M":
            for meld in total_tile[1][:-1]:
                total_all_meld.append(meld[0:6])
            for meld in total_tile[2]:
                total_all_meld.append(meld[0:6])
        else:
            for meld in total_tile[1]:
                total_all_meld.append(meld[0:6])

        # 天和
        if info[4] == "1" and menzen and len(raw_total_tile) == 14 and info[0] == "1":
            if "天和" in st.session_state.allow_yaku or cal_allow_mode:
                yakuman[index].append(["天和", "役满"])
                yakuman_han[index] += 1

        # 地和
        if info[4] == "2" and menzen and len(raw_total_tile) == 14 and info[0] == "1":
            if "地和" in st.session_state.allow_yaku or cal_allow_mode:
                yakuman[index].append(["地和", "役满"])
                yakuman_han[index] += 1

        # 大三元
        if raw_total_tile.count("5z") >= 3 and raw_total_tile.count("6z") >= 3 and raw_total_tile.count("7z") >= 3:
            if "大三元" in st.session_state.allow_yaku or cal_allow_mode:
                yakuman[index].append(["大三元", "役满"])
                yakuman_han[index] += 1

        # 四暗刻/四暗刻单骑
        closed_tri = 0
        for meld in total_tile[1][:-1]:
            if meld[0:2] == meld[2:4] == meld[4:6]:
                closed_tri += 1
        for meld in total_tile[2]:
            if meld[-1] == "a":
                closed_tri += 1
        if closed_tri >= 4:
            if ron_tsumo_tile in total_tile[1][-1] or info[4] == "1":
                if cal_double:
                    if "四暗刻" in st.session_state.allow_yaku or cal_allow_mode:
                        yakuman[index].append(["四暗刻单骑", "双倍役满"])
                        yakuman_han[index] += 2
                else:
                    if "四暗刻" in st.session_state.allow_yaku or cal_allow_mode:
                        yakuman[index].append(["四暗刻单骑", "役满"])
                        yakuman_han[index] += 1
            elif info[0] == "1":
                if "四暗刻" in st.session_state.allow_yaku or cal_allow_mode:
                    yakuman[index].append(["四暗刻", "役满"])
                    yakuman_han[index] += 1

        # 字一色/大七星
        tsuuiisou_check = True
        for tile in raw_total_tile:
            if tile[-1] != "z":
                tsuuiisou_check = False
        if tsuuiisou_check:
            if total_tile[0] == "M":
                if "字一色" in st.session_state.allow_yaku or cal_allow_mode:
                    yakuman[index].append(["字一色", "役满"])
                    yakuman_han[index] += 1
            elif total_tile[0] == "Q":
                if "大七星" in st.session_state.allow_yaku or cal_allow_mode:
                    yakuman[index].append(["大七星", "双倍役满"])
                    yakuman_han[index] += 2
                elif "字一色" in st.session_state.allow_yaku or cal_allow_mode:
                    yakuman[index].append(["字一色", "役满"])
                    yakuman_han[index] += 1

        # 绿一色
        ryuuiisou_check = True
        for tile in raw_total_tile:
            if tile not in ["2s", "3s", "4s", "6s", "8s", "6z"]:
                ryuuiisou_check = False
        if ryuuiisou_check:
            if "绿一色" in st.session_state.allow_yaku or cal_allow_mode:
                yakuman[index].append(["绿一色", "役满"])
                yakuman_han[index] += 1

        # 清老头
        chinroutou_check = True
        for tile in raw_total_tile:
            if tile not in ["1s", "9s", "1p", "9p", "1m", "9m"]:
                chinroutou_check = False
        if chinroutou_check:
            if "清老头" in st.session_state.allow_yaku or cal_allow_mode:
                yakuman[index].append(["清老头", "役满"])
                yakuman_han[index] += 1

        # 国士无双/国士无双十三面
        if total_tile[0] == "G":
            if raw_total_tile.count(ron_tsumo_tile) == 2 or info[4] == "1":
                if cal_double:
                    if "国士无双" in st.session_state.allow_yaku or cal_allow_mode:
                        yakuman[index].append(["国士无双十三面", "双倍役满"])
                        yakuman_han[index] += 2
                else:
                    if "国士无双" in st.session_state.allow_yaku or cal_allow_mode:
                        yakuman[index].append(["国士无双十三面", "役满"])
                        yakuman_han[index] += 1
            else:
                if "国士无双" in st.session_state.allow_yaku or cal_allow_mode:
                    yakuman[index].append(["国士无双", "役满"])
                    yakuman_han[index] += 1

        # 小四喜/大四喜
        suushii_tri = 0
        suushii_pair = 0
        for tile in ["1z", "2z", "3z", "4z"]:
            if raw_total_tile.count(tile) == 2:
                suushii_pair += 1
            elif raw_total_tile.count(tile) >= 3:
                suushii_tri += 1
        if suushii_tri == 3 and suushii_pair == 1:
            if "小四喜" in st.session_state.allow_yaku or cal_allow_mode:
                yakuman[index].append(["小四喜", "役满"])
                yakuman_han[index] += 1
        elif suushii_tri == 4:
            if cal_double:
                if "小四喜" in st.session_state.allow_yaku or cal_allow_mode:
                    yakuman[index].append(["大四喜", "双倍役满"])
                    yakuman_han[index] += 2
            else:
                if "小四喜" in st.session_state.allow_yaku or cal_allow_mode:
                    yakuman[index].append(["大四喜", "役满"])
                    yakuman_han[index] += 1

        # 四杠子
        if len(raw_total_tile) == 18:
            if "四杠子" in st.session_state.allow_yaku or cal_allow_mode:
                yakuman[index].append(["四杠子", "役满"])
                yakuman_han[index] += 1

        # 九莲宝灯
        type_count = [0, 0, 0, 0]
        chinitsu_type = False
        chuuren_check = False
        pure_chuuren = False
        for tile in raw_total_tile:
            type_count[["m", "s", "p", "z"].index(tile[1])] += 1
        if type_count.count(0) == 3 and type_count[3] == 0:
            chinitsu_type = raw_total_tile[0][1]
        chuuren = [str(i) + str(chinitsu_type) for i in range(1, 10)]
        for i in ["1", "1", "9", "9"]:
            chuuren.append(i + str(chinitsu_type))
        for tile in [str(i) + str(chinitsu_type) for i in range(1, 10)]:
            chuuren.append(tile)
            chuuren.sort()
            if chuuren == raw_total_tile:
                chuuren_check = True
                if tile == ron_tsumo_tile:
                    pure_chuuren = True
            else:
                chuuren.remove(tile)
        if not menzen:
            chuuren_check = False
        if chuuren_check:
            if pure_chuuren or info[4] == "1":
                if cal_double:
                    if "九莲宝灯" in st.session_state.allow_yaku or cal_allow_mode:
                        yakuman[index].append(["纯正九莲宝灯", "双倍役满"])
                        yakuman_han[index] += 2
                else:
                    if "九莲宝灯" in st.session_state.allow_yaku or cal_allow_mode:
                        yakuman[index].append(["纯正九莲宝灯", "役满"])
                        yakuman_han[index] += 1
            else:
                if "九莲宝灯" in st.session_state.allow_yaku or cal_allow_mode:
                    yakuman[index].append(["九莲宝灯", "役满"])
                    yakuman_han[index] += 1
        
        # 大车轮
        if raw_total_tile == ["2p","2p","3p","3p","4p","4p","5p","5p","6p","6p","7p","7p","8p","8p"]:
            if "大车轮" in st.session_state.allow_yaku and cal_allow_mode != 1:
                yakuman[index].append(["大车轮", "役满"])
                yakuman_han[index] += 1
        
        # 大数邻
        if raw_total_tile == ["2m","2m","3m","3m","4m","4m","5m","5m","6m","6m","7m","7m","8m","8m"]:
            if "大数邻" in st.session_state.allow_yaku and cal_allow_mode != 1:
                yakuman[index].append(["大数邻", "役满"])
                yakuman_han[index] += 1

        # 大竹林
        if raw_total_tile == ["2s","2s","3s","3s","4s","4s","5s","5s","6s","6s","7s","7s","8s","8s"]:
            if "大竹林" in st.session_state.allow_yaku and cal_allow_mode != 1:
                yakuman[index].append(["大竹林", "役满"])
                yakuman_han[index] += 1

        # 石上三年
        if info[3] == "1" or info[3] == "2":
            pass
        elif info[4] == "3" and info[1] == "2" and menzen:
            if "石上三年" in st.session_state.allow_yaku and cal_allow_mode != 1:
                yakuman[index].append(["石上三年", "役满"])
                yakuman_han[index] += 1

        # 黑一色
        kuroiiso_check = True
        for tile in raw_total_tile:
            if tile not in ["2p", "4p", "8p", "1z", "2z", "3z", "4z"]:
                kuroiiso_check = False
        if kuroiiso_check:
            if "黑一色" in st.session_state.allow_yaku and cal_allow_mode != 1:
                yakuman[index].append(["黑一色", "役满"])
                yakuman_han[index] += 1

        # 红孔雀
        redkongque_check = True
        for tile in raw_total_tile:
            if tile not in ["1s","5s","7s","9s","7z"]:
                redkongque_check = False
        if redkongque_check:
            if "红孔雀" in st.session_state.allow_yaku and cal_allow_mode != 1:
                yakuman[index].append(["红孔雀", "役满"])
                yakuman_han[index] += 1

        #四连刻
        silianke_check = False
        silianke_check_ke = []
        silianke_check_se = []
        for meld in total_all_meld:
            if meld[0:2] == meld[2:4]:
                silianke_check_ke.append(int(meld[0]))
                silianke_check_se.append(meld[1])
        if silianke_check_se.count("m") >= 4 or silianke_check_se.count("s") >= 4 or silianke_check_se.count("p") >= 4:
            if silianke_check_ke in [[1,2,3,4],[2,3,4,5],[3,4,5,6],[4,5,6,7],[5,6,7,8],[6,7,8,9]]:
                if "四连刻" in st.session_state.allow_yaku and cal_allow_mode != 1:
                    yakuman[index].append(["四连刻", "役满"])
                    yakuman_han[index] += 1

    if cal_lan == 0:
        chinese_number = {1: "一", 2: "双", 3: "三", 4: "四", 5: "五", 6: "六", 7: "七", 8: "八", 9: "九"}
    else:
        chinese_number = {1: "Single", 2: "Double", 3: "Triple", 4: "Quadruple", 5: "Quintuple", 6: "Sextuple", 7: "Septuple", 8: "Octuple", 9: "Nonuple"}

    if max(yakuman_han) != 0:
        max_index = yakuman_han.index(max(yakuman_han))
        if cal_output:
            print_total(checked_total_tile[max_index], cal_lan)
        fu_cal = ["役满，无需算符", "Yakuman, No Need For Fu Calculation"][lan]
        if True:
            eng_yakuman = {"国士无双": "Kokushi Muso", "国士无双十三面": "Kokushi Muso Juusanmen",
                           "纯正九莲宝灯": "Junsei Churen Poto",
                           "九莲宝灯": "Churen Poto", "四暗刻": "Suu Ankou", "四暗刻单骑": "Suu Ankou Tanki",
                           "大三元": "Dai Sanjen", "小四喜": "Sho Suushi", "大四喜": "Dai Suushi",
                           "字一色": "Tsuuiiso", "绿一色": "Ryuuiiso", "清老头": "Chinrooto",
                           "四杠子": "Suu Kantsu", "天和": "Tenho", "地和": "Chiho", "役满": "Yakuman",
                           "双倍役满": "Double Yakuman", "大七星": "Dai Shichisei", "大竹林": "Dai Chikurin", 
                           "大车轮": "Dai Sharin", "大数邻": "Dai Kazurin", "石上三年": "Ishino Uenimo San Nen",
                           "黑一色": "Kuro Iiso", "红孔雀": "Beni Kujaku", "四连刻": "Shi Renko"}
            if len(yakuman[max_index]) > 1:
                for yaku in yakuman[max_index]:
                    #print(yaku[0] + " " + yaku[1])
                    if cal_lan == 0:
                        st_han_output += f"{yaku[0]} {yaku[1]}\n"
                    else:
                        st_han_output += f"{eng_yakuman[yaku[0]]} - {eng_yakuman[yaku[1]]}\n"
                #print(chinese_number[yakuman_han[max_index]] + "倍役满" + "!" * yakuman_han[max_index])
                st_han_output += f"{chinese_number[yakuman_han[max_index]]}{["倍役满"," Yakuman"][cal_lan]}{"!" * yakuman_han[max_index]}\n"
            else:
                #print(yakuman[max_index][0][0])
                if cal_lan == 0:
                    st_han_output += f"{yakuman[max_index][0][0]}\n"
                else:
                    st_han_output += f"{eng_yakuman[yakuman[max_index][0][0]]}\n"
                #print(yakuman[max_index][0][1] + "!" * yakuman_han[max_index])
                if cal_lan == 0:
                    st_han_output += f"{yakuman[max_index][0][1]}{"!" * yakuman_han[max_index]}\n"
                else:
                    st_han_output += f"{eng_yakuman[yakuman[max_index][0][1]]}{"!" * yakuman_han[max_index]}\n"
            if cal_output:
                st.text(st_han_output)
            st_han_output = ""
            #print(f"庄家：{48000 * yakuman_han[max_index]}", end="")
            st_han_output += f"{["庄家","Dealer"][cal_lan]}：{48000 * yakuman_han[max_index]}"
            if info[0] == "1":
                #print(f"/{48000 * yakuman_han[max_index] // 3 * 2}({48000 * yakuman_han[max_index] // 3})")
                st_han_output += f"/{48000 * yakuman_han[max_index] // 3 * 2}({48000 * yakuman_han[max_index] // 3})\n"
            else:
                #print()
                st_han_output += "\n"
            #print(f"子家：{32000 * yakuman_han[max_index]}", end="")
            st_han_output += f"{["子家","Non-Dealer"][cal_lan]}：{32000 * yakuman_han[max_index]}"
            if info[0] == "1":
                #print(f"/{32000 * yakuman_han[max_index] // 2 + 32000 * yakuman_han[max_index] // 4}({32000 * yakuman_han[max_index] // 2},{32000 * yakuman_han[max_index] // 4})")
                st_han_output += f"/{32000 * yakuman_han[max_index] // 2 + 32000 * yakuman_han[max_index] // 4}({32000 * yakuman_han[max_index] // 2},{32000 * yakuman_han[max_index] // 4})\n"
            else:
                #print()
                st_han_output += "\n"
            if cal_output:
                st.text(st_han_output)
                with st.expander(["符数计算", "Fu Calculation"][lan]):
                    st.text(fu_cal)
            if yakuman_han[max_index] == 1:
                return_title = f"{["役满","Yakuman"][cal_lan]}"
            else:
                return_title = f"{chinese_number[yakuman_han[max_index]]}{["倍役满"," Yakuman"][cal_lan]}"
            return_title = [return_title, yakuman_han[max_index]*100+len(yakuman[max_index])]
            return return_title

    # 计番(普通役)
    non_yakuman = []
    non_yakuman_han = []
    for index, total_tile in enumerate(checked_total_tile):
        non_yakuman.append([])
        non_yakuman_han.append(0)
        non_yakuman_judge = []

        total_all_meld = []
        if total_tile[0] == "M":
            for meld in total_tile[1][:-1]:
                total_all_meld.append(meld[0:6])
            for meld in total_tile[2]:
                total_all_meld.append(meld[0:6])
        else:
            for meld in total_tile[1]:
                total_all_meld.append(meld[0:6])

        # 立直/双立直
        if info[1] == "1" and menzen:
            if "立直" in st.session_state.allow_yaku or cal_allow_mode:
                non_yakuman[index].append(["立直", "1番"])
                non_yakuman_han[index] += 1
        elif info[1] == "2" and menzen:
            if "双立直" in st.session_state.allow_yaku or cal_allow_mode:
                non_yakuman[index].append(["双立直", "2番"])
                non_yakuman_han[index] += 2
            elif "立直" in st.session_state.allow_yaku or cal_allow_mode:
                non_yakuman[index].append(["立直", "1番"])
                non_yakuman_han[index] += 1
            non_yakuman_judge.append("双立直")

        # 段幺九
        tanyao_check = True
        for tile in raw_total_tile:
            if tile in ["1m", "9m", "1s", "9s", "1p", "9p", "1z", "2z", "3z", "4z", "5z", "6z", "7z"]:
                tanyao_check = False
        if tanyao_check:
            if "段幺九" in st.session_state.allow_yaku or cal_allow_mode:
                non_yakuman[index].append(["段幺九", "1番"])
                non_yakuman_han[index] += 1

        # 门前清自摸和
        if info[0] == "1" and menzen:
            if "门前清自摸和" in st.session_state.allow_yaku or cal_allow_mode:
                non_yakuman[index].append(["门前清自摸和", "1番"])
                non_yakuman_han[index] += 1

        # 役牌：自风牌
        if raw_total_tile.count(wind[1]) >= 3:
            if "役牌：自风牌" in st.session_state.allow_yaku or cal_allow_mode:
                non_yakuman[index].append(["役牌：自风牌", "1番"])
                non_yakuman_han[index] += 1

        # 役牌：场风牌
        if raw_total_tile.count(wind[0]) >= 3:
            if "役牌：场风牌" in st.session_state.allow_yaku or cal_allow_mode:
                non_yakuman[index].append(["役牌：场风牌", "1番"])
                non_yakuman_han[index] += 1

        # 役牌：三元牌
        if raw_total_tile.count("5z") >= 3:
            if "役牌：白" in st.session_state.allow_yaku or cal_allow_mode:
                non_yakuman[index].append(["役牌：白", "1番"])
                non_yakuman_han[index] += 1
        if raw_total_tile.count("6z") >= 3:
            if "役牌：发" in st.session_state.allow_yaku or cal_allow_mode:
                non_yakuman[index].append(["役牌：发", "1番"])
                non_yakuman_han[index] += 1
        if raw_total_tile.count("7z") >= 3:
            if "役牌：中" in st.session_state.allow_yaku or cal_allow_mode:
                non_yakuman[index].append(["役牌：中", "1番"])
                non_yakuman_han[index] += 1

        # 平和
        pinfu_check = 0
        pinfu_last_tile_check = False
        if menzen:
            for meld in total_tile[1][:-1]:
                if meld[0:2] != meld[2:4]:
                    pinfu_check += 1
                    if meld not in ["1s2s3s", "1m2m3m", "1p2p3p", "7s8s9s", "7m8m9m", "7p8p9p"]:
                        if ron_tsumo_tile == meld[0:2] or ron_tsumo_tile == meld[4:6]:
                            pinfu_last_tile_check = True
                    else:
                        if meld in ["1s2s3s", "1m2m3m", "1p2p3p"]:
                            if ron_tsumo_tile == meld[0:2]:
                                pinfu_last_tile_check = True
                        else:
                            if ron_tsumo_tile == meld[4:6]:
                                pinfu_last_tile_check = True
        if total_tile[1][-1][0:2] not in wind and total_tile[1][-1][0:2] not in ["5z", "6z", "7z"]:
            pinfu_check += 1
        if pinfu_check == 5 and pinfu_last_tile_check:
            if "平和" in st.session_state.allow_yaku or cal_allow_mode:
                non_yakuman[index].append(["平和", "1番"])
                non_yakuman_han[index] += 1

        # 一杯口/二杯口
        peikou = 0
        if total_tile[0] == "M":
            for meld in total_tile[1][:-1]:
                if meld[0:2] != meld[2:4] and total_tile[1].count(meld) >= 2:
                    peikou += 1
        if peikou >= 4 and menzen:
            if "二杯口" in st.session_state.allow_yaku or cal_allow_mode:
                non_yakuman[index].append(["二杯口", "3番"])
                non_yakuman_han[index] += 3
            elif "一杯口" in st.session_state.allow_yaku or cal_allow_mode:
                non_yakuman[index].append(["一杯口", "1番"])
                non_yakuman_han[index] += 1
        elif peikou >= 2 and menzen:
            if "一杯口" in st.session_state.allow_yaku or cal_allow_mode:
                non_yakuman[index].append(["一杯口", "1番"])
                non_yakuman_han[index] += 1
       
        # 岭上开花
        if info[3] == "2" and info[0] == "1":
            if "岭上开花" in st.session_state.allow_yaku or cal_allow_mode:
                non_yakuman[index].append(["岭上开花", "1番"])
                non_yakuman_han[index] += 1
            non_yakuman_judge.append("岭上开花")

        # 一发
        if "岭上开花" not in non_yakuman_judge and info[1] != "0" and info[2] == "1" and menzen:
            if "一发" in st.session_state.allow_yaku or cal_allow_mode:
                non_yakuman[index].append(["一发", "1番"])
                non_yakuman_han[index] += 1
            non_yakuman_judge.append("一发")

        # 枪杠
        if info[3] == "1" and info[0] == "0":
            if "枪杠" in st.session_state.allow_yaku or cal_allow_mode:
                non_yakuman[index].append(["枪杠", "1番"])
                non_yakuman_han[index] += 1
            non_yakuman_judge.append("枪杠")

        # 海底摸月/河底捞鱼
        if "一发" in non_yakuman_judge and "双立直" in non_yakuman_judge:
            pass
        elif "岭上开花" in non_yakuman_judge or "枪杠" in non_yakuman_judge:
            pass
        else:
            if info[4] == "3" and info[0] == "0":
                if "河底捞鱼" in st.session_state.allow_yaku or cal_allow_mode:
                    non_yakuman[index].append(["河底捞鱼", "1番"])
                    non_yakuman_han[index] += 1
            elif info[4] == "3" and info[0] == "1":
                if "海底摸月" in st.session_state.allow_yaku or cal_allow_mode:
                    non_yakuman[index].append(["海底摸月", "1番"])
                    non_yakuman_han[index] += 1

        # 三色同刻
        sanshokudoukou = False
        if "1m1m1m" in total_all_meld and "1p1p1p" in total_all_meld and "1s1s1s" in total_all_meld:
            sanshokudoukou = True
        elif "2m2m2m" in total_all_meld and "2p2p2p" in total_all_meld and "2s2s2s" in total_all_meld:
            sanshokudoukou = True
        elif "3m3m3m" in total_all_meld and "3p3p3p" in total_all_meld and "3s3s3s" in total_all_meld:
            sanshokudoukou = True
        elif "4m4m4m" in total_all_meld and "4p4p4p" in total_all_meld and "4s4s4s" in total_all_meld:
            sanshokudoukou = True
        elif "5m5m5m" in total_all_meld and "5p5p5p" in total_all_meld and "5s5s5s" in total_all_meld:
            sanshokudoukou = True
        elif "6m6m6m" in total_all_meld and "6p6p6p" in total_all_meld and "6s6s6s" in total_all_meld:
            sanshokudoukou = True
        elif "7m7m7m" in total_all_meld and "7p7p7p" in total_all_meld and "7s7s7s" in total_all_meld:
            sanshokudoukou = True
        elif "8m8m8m" in total_all_meld and "8p8p8p" in total_all_meld and "8s8s8s" in total_all_meld:
            sanshokudoukou = True
        elif "9m9m9m" in total_all_meld and "9p9p9p" in total_all_meld and "9s9s9s" in total_all_meld:
            sanshokudoukou = True
        if sanshokudoukou:
            if "三色同刻" in st.session_state.allow_yaku or cal_allow_mode:
                non_yakuman[index].append(["三色同刻", "2番"])
                non_yakuman_han[index] += 2

        # 三杠子
        if len(raw_total_tile) >= 17:
            if "三杠子" in st.session_state.allow_yaku or cal_allow_mode:
                non_yakuman[index].append(["三杠子", "2番"])
                non_yakuman_han[index] += 2

        # 对对和
        if total_tile[0] == "M":
            if total_all_meld[0][0:2] == total_all_meld[0][2:4] and total_all_meld[1][0:2] == total_all_meld[1][2:4]:
                if total_all_meld[2][0:2] == total_all_meld[2][2:4] and total_all_meld[3][0:2] == total_all_meld[3][
                                                                                                  2:4]:
                    if "对对和" in st.session_state.allow_yaku or cal_allow_mode:
                        non_yakuman[index].append(["对对和", "2番"])
                        non_yakuman_han[index] += 2

        # 三暗刻
        san_closed_tri = 0
        san_closed_tri_check = raw_total_tile.copy()
        for meld in total_tile[1][:-1]:
            if meld[0:2] == meld[2:4] == meld[4:6]:
                san_closed_tri += 1
                san_closed_tri_check.remove(meld[0:2])
                san_closed_tri_check.remove(meld[2:4])
                san_closed_tri_check.remove(meld[4:6])
        for meld in total_tile[2]:
            if meld[-1] == "a":
                san_closed_tri += 1
                for i in range(4):
                    san_closed_tri_check.remove(meld[0:2])
        if san_closed_tri == 3 and info[0] == "1":
            if "三暗刻" in st.session_state.allow_yaku or cal_allow_mode:
                non_yakuman[index].append(["三暗刻", "2番"])
                non_yakuman_han[index] += 2
        elif san_closed_tri == 3 and ron_tsumo_tile in san_closed_tri_check:
            if "三暗刻" in st.session_state.allow_yaku or cal_allow_mode:
                non_yakuman[index].append(["三暗刻", "2番"])
                non_yakuman_han[index] += 2
        elif san_closed_tri >= 4:
            if "三暗刻" in st.session_state.allow_yaku or cal_allow_mode:
                non_yakuman[index].append(["三暗刻", "2番"])
                non_yakuman_han[index] += 2

        # 小三元
        shousangen = False
        if raw_total_tile.count("5z") >= 3 and raw_total_tile.count("6z") >= 3 and raw_total_tile.count("7z") >= 2:
            shousangen = True
        elif raw_total_tile.count("5z") >= 3 and raw_total_tile.count("6z") >= 2 and raw_total_tile.count("7z") >= 3:
            shousangen = True
        elif raw_total_tile.count("5z") >= 2 and raw_total_tile.count("6z") >= 3 and raw_total_tile.count("7z") >= 3:
            shousangen = True
        if shousangen:
            if "小三元" in st.session_state.allow_yaku or cal_allow_mode:
                non_yakuman[index].append(["小三元", "2番"])
                non_yakuman_han[index] += 2

        # 混老头/纯全带幺九/混全带幺九
        honroutou = True
        honchantaiyaochuu = 0
        junchantaiyaochuu = 0
        for tile in raw_total_tile:
            if tile not in ["1m", "9m", "1s", "9s", "1p", "9p", "1z", "2z", "3z", "4z", "5z", "6z", "7z"]:
                honroutou = False
        if honroutou:
            if "混老头" in st.session_state.allow_yaku or cal_allow_mode:
                non_yakuman[index].append(["混老头", "2番"])
                non_yakuman_han[index] += 2
            elif ("混全带幺九" in st.session_state.allow_yaku or cal_allow_mode) and total_tile[0] == "M":
                if not menzen:
                    non_yakuman[index].append(["混全带幺九", "1番"])
                    non_yakuman_han[index] += 1
                else:
                    non_yakuman[index].append(["混全带幺九", "2番"])
                    non_yakuman_han[index] += 2
        elif total_tile[0] == "M":
            for meld in total_tile[1]:
                for tile in ["1m", "9m", "1s", "9s", "1p", "9p"]:
                    if tile in meld:
                        junchantaiyaochuu += 1
                        break
            for meld in total_tile[2]:
                for tile in ["1m", "9m", "1s", "9s", "1p", "9p"]:
                    if tile in meld:
                        junchantaiyaochuu += 1
                        break
            if junchantaiyaochuu >= 5 and not menzen:
                if "纯全带幺九" in st.session_state.allow_yaku or cal_allow_mode:
                    non_yakuman[index].append(["纯全带幺九", "2番"])
                    non_yakuman_han[index] += 2
                elif "混全带幺九" in st.session_state.allow_yaku or cal_allow_mode:
                    non_yakuman[index].append(["混全带幺九", "1番"])
                    non_yakuman_han[index] += 1
            elif junchantaiyaochuu >= 5 and menzen:
                if "纯全带幺九" in st.session_state.allow_yaku or cal_allow_mode:
                    non_yakuman[index].append(["纯全带幺九", "3番"])
                    non_yakuman_han[index] += 3
                elif "混全带幺九" in st.session_state.allow_yaku or cal_allow_mode:
                    non_yakuman[index].append(["混全带幺九", "2番"])
                    non_yakuman_han[index] += 2
            else:
                for meld in total_tile[1]:
                    for tile in ["1m", "9m", "1s", "9s", "1p", "9p", "1z", "2z", "3z", "4z", "5z", "6z", "7z"]:
                        if tile in meld:
                            honchantaiyaochuu += 1
                            break
                for meld in total_tile[2]:
                    for tile in ["1m", "9m", "1s", "9s", "1p", "9p", "1z", "2z", "3z", "4z", "5z", "6z", "7z"]:
                        if tile in meld:
                            honchantaiyaochuu += 1
                            break
                if honchantaiyaochuu >= 5 and not menzen:
                    if "混全带幺九" in st.session_state.allow_yaku or cal_allow_mode:
                        non_yakuman[index].append(["混全带幺九", "1番"])
                        non_yakuman_han[index] += 1
                elif honchantaiyaochuu >= 5 and menzen:
                    if "混全带幺九" in st.session_state.allow_yaku or cal_allow_mode:
                        non_yakuman[index].append(["混全带幺九", "2番"])
                        non_yakuman_han[index] += 2

        # 七对子
        if total_tile[0] == "Q":
            if "七对子" in st.session_state.allow_yaku or cal_allow_mode:
                non_yakuman[index].append(["七对子", "2番"])
                non_yakuman_han[index] += 2

        # 一气通贯
        ittsu = False
        if total_tile[0] == "M":
            if "1m2m3m" in total_all_meld and "4m5m6m" in total_all_meld and "7m8m9m" in total_all_meld:
                ittsu = True
            elif "1s2s3s" in total_all_meld and "4s5s6s" in total_all_meld and "7s8s9s" in total_all_meld:
                ittsu = True
            elif "1p2p3p" in total_all_meld and "4p5p6p" in total_all_meld and "7p8p9p" in total_all_meld:
                ittsu = True
            if ittsu and not menzen:
                if "一气通贯" in st.session_state.allow_yaku or cal_allow_mode:
                    non_yakuman[index].append(["一气通贯", "1番"])
                    non_yakuman_han[index] += 1
            elif ittsu and menzen:
                if "一气通贯" in st.session_state.allow_yaku or cal_allow_mode:
                    non_yakuman[index].append(["一气通贯", "2番"])
                    non_yakuman_han[index] += 2

        # 三色同顺
        sanshokudoujun = False
        if "1m2m3m" in total_all_meld and "1p2p3p" in total_all_meld and "1s2s3s" in total_all_meld:
            sanshokudoujun = True
        elif "2m3m4m" in total_all_meld and "2p3p4p" in total_all_meld and "2s3s4s" in total_all_meld:
            sanshokudoujun = True
        elif "3m4m5m" in total_all_meld and "3p4p5p" in total_all_meld and "3s4s5s" in total_all_meld:
            sanshokudoujun = True
        elif "4m5m6m" in total_all_meld and "4p5p6p" in total_all_meld and "4s5s6s" in total_all_meld:
            sanshokudoujun = True
        elif "5m6m7m" in total_all_meld and "5p6p7p" in total_all_meld and "5s6s7s" in total_all_meld:
            sanshokudoujun = True
        elif "6m7m8m" in total_all_meld and "6p7p8p" in total_all_meld and "6s7s8s" in total_all_meld:
            sanshokudoujun = True
        elif "7m8m9m" in total_all_meld and "7p8p9p" in total_all_meld and "7s8s9s" in total_all_meld:
            sanshokudoujun = True
        if sanshokudoujun and not menzen:
            if "三色同顺" in st.session_state.allow_yaku or cal_allow_mode:
                non_yakuman[index].append(["三色同顺", "1番"])
                non_yakuman_han[index] += 1
        elif sanshokudoujun and menzen:
            if "三色同顺" in st.session_state.allow_yaku or cal_allow_mode:
                non_yakuman[index].append(["三色同顺", "2番"])
                non_yakuman_han[index] += 2

        # 清一色/混一色
        honitsu_type = ""
        honitsu = True
        if chinitsu_type and not menzen:
            if "清一色" in st.session_state.allow_yaku or cal_allow_mode:
                non_yakuman[index].append(["清一色", "5番"])
                non_yakuman_han[index] += 5
            elif "混一色" in st.session_state.allow_yaku or cal_allow_mode:
                if "混一色" in st.session_state.allow_yaku or cal_allow_mode:
                    non_yakuman[index].append(["混一色", "2番"])
                    non_yakuman_han[index] += 2
        elif chinitsu_type and menzen:
            if "清一色" in st.session_state.allow_yaku or cal_allow_mode:
                non_yakuman[index].append(["清一色", "6番"])
                non_yakuman_han[index] += 6
            elif "混一色" in st.session_state.allow_yaku or cal_allow_mode:
                if "混一色" in st.session_state.allow_yaku or cal_allow_mode:
                    non_yakuman[index].append(["混一色", "3番"])
                    non_yakuman_han[index] += 3
        else:
            for tile in raw_total_tile:
                if honitsu_type == "" and tile[1] != "z":
                    honitsu_type = tile[1]
                if tile[1] != "z" and tile[1] != honitsu_type:
                    honitsu = False
            if honitsu and not menzen:
                if "混一色" in st.session_state.allow_yaku or cal_allow_mode:
                    non_yakuman[index].append(["混一色", "2番"])
                    non_yakuman_han[index] += 2
            elif honitsu and menzen:
                if "混一色" in st.session_state.allow_yaku or cal_allow_mode:
                    non_yakuman[index].append(["混一色", "3番"])
                    non_yakuman_han[index] += 3

        # 宝牌/里宝牌
        if non_yakuman_han[index] != 0:
            dora_count = 0
            for tile in dora:
                if tile == "4z" and "8z" in dora:
                    dora_count += dora.count("8z")
                dora_count += raw_total_tile.count(tile)
            if dora_count:
                if ["立直", "1番"] in non_yakuman[index]:
                    non_yakuman[index].append(["宝牌/里宝牌", f"{dora_count}番"])
                else:
                    non_yakuman[index].append(["宝牌", f"{dora_count}番"])
            non_yakuman_han[index] += dora_count

    if max(non_yakuman_han) == 0:
        #print("哥么你这牌有役吗")
        if cal_output:
            for j in range(5):
                st.error(["哥么你役去哪了？？？","Where Is Your Han Bro???"][cal_lan])
        return_title = ["无役", "No Yaku"][cal_lan]
        return_title = [return_title,0]
        return return_title
    else:
        max_index = non_yakuman_han.index(max(non_yakuman_han))

        # 红宝牌
        if red_dora:
            non_yakuman[max_index].append(["红宝牌", f"{len(red_dora)}番"])
            non_yakuman_han[max_index] += len(red_dora)

        # 拔北宝牌
        if "8z" in dora:
            eightz_count = dora.count("8z")
            non_yakuman[max_index].append(["拔北宝牌", f"{eightz_count}番"])
            non_yakuman_han[max_index] += dora.count("8z")

        if dora_count == 0 and ["立直", "1番"] in non_yakuman[max_index] or ["双立直", "2番"] in non_yakuman[max_index]:
            non_yakuman[max_index].append(["里宝牌", f"{dora_count}番"])

        head = ""
        fu = 20

        if non_yakuman_han[max_index] >= 5:
            fu_cal = ["番数≥5，无需算符","Han≥5, No Need For Fu Calculation"][lan]
        if non_yakuman_han[max_index] >= 13:
            head = "累计役满!!!!!"
        elif non_yakuman_han[max_index] >= 11:
            head = "三倍满!!!!"
        elif non_yakuman_han[max_index] >= 8:
            head = "倍满!!!"
        elif non_yakuman_han[max_index] >= 6:
            head = "跳满!!"
        elif non_yakuman_han[max_index] >= 5:
            head = "满贯!"
        else:  # 计符
            fu_cal = ["番数<5，需要算符:\n","Han<5, Fu Calculation is needed:\n"][lan]
            if checked_total_tile[max_index][0] == "Q":
                fu = 25
                fu_cal += ["- 七对子，固定25符\n","- Chiitoitsu Is Always 25 Fu\n"][lan]
            elif checked_total_tile[max_index][0] == "G":
                fu = 25
                fu_cal += ["- 国士无双，固定25符\n","- Kokushi Muso Is Always 25 Fu\n"][lan]
            else:
                # 面子
                fu_cal += ["- 一般和牌型，底符20符\n","- Standard Hand Base 20 Fu\n"][lan]
                for meld in checked_total_tile[max_index][1][:-1]:
                    add_fu = 0
                    if meld[0:2] == meld[2:4]:
                        if info[0] == "1" or ron_tsumo_tile != meld[0:2]:
                            add_fu = 2
                        elif raw_total_tile.count(ron_tsumo_tile) > 3:
                            add_fu = 2
                        else:
                            add_fu = 1
                    if add_fu:
                        fu_cal += f"- {sim_meld(meld)}："
                        if meld[0:2] in ["1m", "9m", "1s", "9s", "1p", "9p", "1z", "2z", "3z", "4z", "5z", "6z", "7z"]:
                            fu += 4 * add_fu
                            match 4*add_fu:
                                case 4:
                                    fu_cal += ["幺九明刻，+4符\n","Exposed Honor Triple, + 4 Fu\n"][lan]
                                case 8:
                                    fu_cal += ["幺九暗刻，+8符\n", "Closed Honor Triple, + 8 Fu\n"][lan]
                        else:
                            fu += 2 * add_fu
                            match 2 * add_fu:
                                case 2:
                                    fu_cal += ["非幺九明刻，+2符\n", "Exposed Simple Triple, + 2 Fu\n"][lan]
                                case 4:
                                    fu_cal += ["非幺九暗刻，+4符\n", "Closed Simple Triple, + 4 Fu\n"][lan]


                for meld in checked_total_tile[max_index][2]:
                    add_fu = 0
                    if meld[0:2] == meld[2:4]:
                        match len(meld):
                            case 6:
                                add_fu = 1
                            case 8:
                                add_fu = 4
                            case 9:
                                add_fu = 8
                    if add_fu:
                        fu_cal += f"- {sim_meld(meld)}: "
                        if meld[0:2] in ["1m", "9m", "1s", "9s", "1p", "9p", "1z", "2z", "3z", "4z", "5z", "6z", "7z"]:
                            fu += 4 * add_fu
                            match 4 * add_fu:
                                case 4:
                                    fu_cal += ["幺九明刻，+4符\n", "Exposed Honor Triple, + 4 Fu\n"][lan]
                                case 8:
                                    fu_cal += ["幺九暗刻，+8符\n", "Closed Honor Triple, + 8 Fu\n"][lan]
                                case 16:
                                    fu_cal += ["幺九明杠，+16符\n", "Exposed Honor Kan, + 16 Fu\n"][lan]
                                case 32:
                                    fu_cal += ["幺九暗杠，+32符\n", "Closed Honor Kan, + 32 Fu\n"][lan]
                        else:
                            fu += 2 * add_fu
                            match 2 * add_fu:
                                case 2:
                                    fu_cal += ["非幺九明刻，+2符\n", "Exposed Simple Triple, + 2 Fu\n"][lan]
                                case 4:
                                    fu_cal += ["非幺九暗刻，+4符\n", "Closed Simple Triple, + 4 Fu\n"][lan]
                                case 8:
                                    fu_cal += ["非幺九明杠，+8符\n", "Exposed Simple Kan, + 8 Fu\n"][lan]
                                case 16:
                                    fu_cal += ["非幺九暗杠，+16符\n", "Closed Simple Kan, + 16 Fu\n"][lan]

                # 雀头
                if wind[0] in checked_total_tile[max_index][1][-1]:
                    fu += 2
                    fu_cal += f"- {sim_meld(checked_total_tile[max_index][1][-1])}："
                    fu_cal += ["场风牌雀头，+2符\n","Round Wind Pair, + 2 Fu\n"][lan]
                if wind[1] in checked_total_tile[max_index][1][-1]:
                    fu += 2
                    fu_cal += f"- {sim_meld(checked_total_tile[max_index][1][-1])}："
                    fu_cal += ["自风牌雀头，+2符\n","Seat Wind Pair, + 2 Fu\n"][lan]
                if "5z" in checked_total_tile[max_index][1][-1] or "6z" in checked_total_tile[max_index][1][
                    -1] or "7z" in \
                        checked_total_tile[max_index][1][-1]:
                    fu_cal += f"- {sim_meld(checked_total_tile[max_index][1][-1])}："
                    fu_cal += ["三元牌雀头，+2符\n","Dragon Pair, + 2 Fu\n"][lan]
                    fu += 2

                # 听牌
                add_fu_last_tile_check = True
                ten_add_fu = False
                for meld in checked_total_tile[max_index][1][:-1]:
                    if meld[0:2] != meld[2:4]:
                        if meld not in ["1s2s3s", "1m2m3m", "1p2p3p", "7s8s9s", "7m8m9m", "7p8p9p"]:
                            if ron_tsumo_tile == meld[0:2] or ron_tsumo_tile == meld[4:6]:
                                add_fu_last_tile_check = False
                        else:
                            if meld in ["1s2s3s", "1m2m3m", "1p2p3p"]:
                                if ron_tsumo_tile == meld[0:2]:
                                    add_fu_last_tile_check = False
                            else:
                                if ron_tsumo_tile == meld[4:6]:
                                    add_fu_last_tile_check = False
                if add_fu_last_tile_check:
                    for meld in checked_total_tile[max_index][1][:-1]:
                        if meld[0:2] != meld[2:4] and ron_tsumo_tile in meld:
                            if ron_tsumo_tile == meld[2:4]:
                                ten_add_fu = True
                                fu_cal += ["- 坎张听牌，+2符\n","- Closed Wait, + 2 Fu\n"][lan]
                                break
                            elif meld in ["1s2s3s", "1m2m3m", "1p2p3p"]:
                                if ron_tsumo_tile == meld[4:6]:
                                    ten_add_fu = True
                                    fu_cal += ["- 边张听牌，+2符\n","- Edge Wait, + 2 Fu\n"][lan]
                                    break
                            elif meld in ["7s8s9s", "7m8m9m", "7p8p9p"]:
                                if ron_tsumo_tile == meld[0:2]:
                                    ten_add_fu = True
                                    fu_cal += ["- 边张听牌，+2符\n","- Edge Wait, + 2 Fu\n"][lan]
                                    break
                        if ron_tsumo_tile in checked_total_tile[max_index][1][-1]:
                            ten_add_fu = True
                            fu_cal += ["- 单骑听牌，+2符\n","- Single Wait, + 2 Fu\n"][lan]
                            break
                if ten_add_fu:
                    fu += 2

                # 和牌状态
                if info[0] == "1" and ["平和", "1番"] not in non_yakuman[max_index]:
                    fu += 2
                    fu_cal += ["- 无平和自摸，+2符\n","- No Pinfu Tsumo, + 2 Fu\n"][lan]
                if menzen and info[0] == "0":
                    fu += 10
                    fu_cal += ["- 门前清荣和，+10符\n", "- Menzen Ron, + 10 Fu\n"][lan]

            if not menzen and fu < 30:
                fu_cal += [f"{fu}符，副露和牌不满30符时固定为30符：",f"{fu} Fu, Open Hand Below 30 Fu Always Round Up To 30 Fu: "][lan]
                fu = 30
            elif fu != 25 and fu - fu // 10 * 10 != 0:
                fu_cal += \
                [f"{fu}符，符数向上取整至{fu // 10 * 10 + 10}符：", f"{fu} Fu, Round Up To {fu // 10 * 10 + 10} Fu: "][lan]
                fu = fu // 10 * 10 + 10
            elif fu != 25:
                fu_cal += [f"{fu}符，符数向上取整至{fu}符：", f"{fu} Fu, Round Up To {fu} Fu: "][lan]
            else:
                fu_cal += ["所以是：","Therefore: "][lan]

            fu_cal += [f"{fu}符\n",f"{fu} Fu\n"][lan]

            if non_yakuman_han[max_index] == 3 and fu >= 70:
                head = "满贯!"
                fu_cal += ["3番70符及以上算作满贯","3 Han 70 Fu Or Above Is Mangan"][lan]
            elif non_yakuman_han[max_index] == 4 and fu >= 40:
                head = "满贯!"
                fu_cal += ["4番20符及以上算作满贯", "4 Han 40 Fu Or Above Is Mangan"][lan]

        if head == "":
            head = f"{fu}符"

        if cal_output:
            print_total(checked_total_tile[max_index], cal_lan)

        eng_yaku = {"立直": "Riichi", "双立直": "Daburiichi", "段幺九": "Tanyao", "门前清自摸和": "Menzen Tsumo",
                "役牌：自风牌": "Jikaze", "役牌：场风牌": "Bakaze", "役牌：白": "Haku", "役牌：发": "Hatsu",
                "役牌：中": "Chun", "平和": "Pinfu", "一杯口": "Iipeikou", "二杯口": "Ryanpeikou",
                "一发": "Ippatsu", "岭上开花": "Rinshan Kaiho", "This code is": "designed by Fort233", "枪杠": "Chankan", "海底摸月": "Haitei",
                "河底捞鱼": "Houtei", "三色同刻": "Sanshoku Douko", "三杠子": "San Kantsu", "对对和": "Toitoi",
                "三暗刻": "San Ankou", "小三元": "Shou Sangen", "混老头": "Honroutou", "纯全带幺九": "Junchantaiyao",
                "混全带幺九": "Honchantaiyao", "七对子": "Chiitoitsu", "一气通贯": "Ittsuu", "三色同顺": "Sanshoku Doujun",
                "清一色": "Chinitsu", "混一色": "Honitsu", "宝牌": "Dora", "里宝牌": "Ura Dora",
                "红宝牌": "Red Dora", "拔北宝牌": "Kita Dora", "宝牌/里宝牌": "Dora/Ura Dora"}
        eng_head = {"满贯!": "Mangan!","跳满!!": "Haneman!!","倍满!!!": "Baiman!!!","三倍满!!!!": "Sanbaiman!!!!","累计役满!!!!!":"Kazoe Yakuman!!!!!"}

        for yaku in non_yakuman[max_index]:
            #print(yaku[0] + " " + yaku[1])
            if cal_lan == 0:
                st_han_output += f"{yaku[0]} {yaku[1]}\n"
            else:
                st_han_output += f"{eng_yaku[yaku[0]]} - {yaku[1][:-1]} Han\n"
        #print(f"{non_yakuman_han[max_index]}番 {head}")
        if cal_lan == 0:
            st_han_output += f"{non_yakuman_han[max_index]}番 {head}\n"
        else:
            if head[-1] == "符":
                st_han_output += f"{non_yakuman_han[max_index]} Han  {head[:-1]} Fu\n"
            else:
                st_han_output += f"{non_yakuman_han[max_index]} Han  {eng_head[head]}\n"
        if cal_output:
            st.text(st_han_output)
        st_han_output = ""

        if head[-1] == "符":
            if cal_lan == 0:
                return_title = f"{non_yakuman_han[max_index]}番 {head}"
            else:
                return_title = f"{non_yakuman_han[max_index]} Han  {head[:-1]} Fu"
        else:
            if cal_lan == 0:
                return_title = f"{non_yakuman_han[max_index]}番 {head.replace("!","")}"
            else:
                return_title = f"{non_yakuman_han[max_index]} Han  {eng_head[head].replace("!","")}"

        ko_point = {(1, 30): (1000, 300, 500), (1, 40): (1300, 400, 700), (1, 50): (1600, 400, 800),
                    (1, 60): (2000, 500, 1000), (1, 70): (2300, 600, 1200), (1, 80): (2600, 700, 1300),
                    (1, 90): (2900, 800, 1500), (1, 100): (3200, 800, 1600), (1, 110): (3600, 900, 1800),
                    (2, 20): (1300, 400, 700), (2, 25): (1600, 400, 800), (2, 30): (2000, 500, 1000),
                    (2, 40): (2600, 700, 1300), (2, 50): (3200, 800, 1600), (2, 60): (3900, 1000, 2000),
                    (2, 70): (4500, 1200, 2300), (2, 80): (5200, 1300, 2600), (2, 90): (5800, 1500, 2900),
                    (2, 100): (6400, 1600, 3200), (2, 110): (7100, 1800, 3600), (3, 20): (2600, 700, 1300),
                    (3, 25): (3200, 800, 1600), (3, 30): (3900, 1000, 2000), (3, 40): (5200, 1300, 2600),
                    (3, 50): (6400, 1600, 3200), (3, 60): (7700, 2000, 3900), (4, 20): (5200, 1300, 2600),
                    (4, 25): (6400, 1600, 3200), (4, 30): (7700, 2000, 3900)}
        oya_point = {(1, 30): (1500, 500, 500), (1, 40): (2000, 700, 700), (1, 50): (2400, 800, 800),
                     (1, 60): (2900, 1000, 1000), (1, 70): (3400, 1200, 1200), (1, 80): (3900, 1300, 1300),
                     (1, 90): (4400, 1500, 1500), (1, 100): (4800, 1600, 1600), (1, 110): (5300, 1800, 1800),
                     (2, 20): (2000, 700, 700), (2, 25): (2400, 800, 800), (2, 30): (2900, 1000, 1000),
                     (2, 40): (3900, 1300, 1300), (2, 50): (4800, 1600, 1600), (2, 60): (5800, 2000, 2000),
                     (2, 70): (6800, 2300, 2300), (2, 80): (7700, 2600, 2600), (2, 90): (8700, 2900, 2900),
                     (2, 100): (9600, 3200, 3200), (2, 110): (10600, 3600, 3600), (3, 20): (3900, 1300, 1300),
                     (3, 25): (4800, 1600, 1600), (3, 30): (5800, 2000, 2000), (3, 40): (7700, 2600, 2600),
                     (3, 50): (9600, 3200, 3200), (3, 60): (11600, 3900, 3900), (4, 20): (7700, 2600, 2600),
                     (4, 25): (9600, 3200, 3200), (4, 30): (11600, 3900, 3900)}
        point_mangan = {"满贯!": (8000, 2000, 4000), "跳满!!": (12000, 3000, 6000), "倍满!!!": (16000, 4000, 8000),
                        "三倍满!!!!": (24000, 6000, 12000), "累计役满!!!!!": (32000, 8000, 16000)}

        #print("-" * 50)
        #print("庄家：", end="")
        try:
            if head[-1] == "符":
                checkforerror = oya_point[(non_yakuman_han[max_index], int(head[:-1]))]
            st_han_output += f"{["庄家","Dealer"][cal_lan]}："
            if info[0] == "1":
                if head[-1] == "符":
                    #print(f"{oya_point[(non_yakuman_han[max_index], int(head[:-1]))][1] * 3}/{oya_point[(non_yakuman_han[max_index], int(head[:-1]))][1] * 2}({oya_point[(non_yakuman_han[max_index], int(head[:-1]))][1]})")
                    st_han_output += f"{oya_point[(non_yakuman_han[max_index], int(head[:-1]))][1] * 3}/{oya_point[(non_yakuman_han[max_index], int(head[:-1]))][1] * 2}({oya_point[(non_yakuman_han[max_index], int(head[:-1]))][1]})\n"
                else:
                    #print(f"{int(point_mangan[head][0] * 1.5)}/{point_mangan[head][2] * 2}({point_mangan[head][2]})")
                    st_han_output += f"{int(point_mangan[head][0] * 1.5)}/{point_mangan[head][2] * 2}({point_mangan[head][2]})\n"
            elif info[0] == "0":
                if head[-1] == "符":
                    #print(oya_point[(non_yakuman_han[max_index], int(head[:-1]))][0])
                    st_han_output += f"{oya_point[(non_yakuman_han[max_index], int(head[:-1]))][0]}\n"
                else:
                    #print(int(point_mangan[head][0] * 1.5))
                    st_han_output += f"{int(point_mangan[head][0] * 1.5)}\n"
            #print("子家：", end="")
            st_han_output += f"{["子家","Non-Dealer"][cal_lan]}："
            if info[0] == "1":
                if head[-1] == "符":
                    #print(f"{ko_point[(non_yakuman_han[max_index], int(head[:-1]))][2] + ko_point[(non_yakuman_han[max_index], int(head[:-1]))][1] * 2}/{ko_point[(non_yakuman_han[max_index], int(head[:-1]))][2] + ko_point[(non_yakuman_han[max_index], int(head[:-1]))][1]}({ko_point[(non_yakuman_han[max_index], int(head[:-1]))][2]},{ko_point[(non_yakuman_han[max_index], int(head[:-1]))][1]})")
                    st_han_output += f"{ko_point[(non_yakuman_han[max_index], int(head[:-1]))][2] + ko_point[(non_yakuman_han[max_index], int(head[:-1]))][1] * 2}/{ko_point[(non_yakuman_han[max_index], int(head[:-1]))][2] + ko_point[(non_yakuman_han[max_index], int(head[:-1]))][1]}({ko_point[(non_yakuman_han[max_index], int(head[:-1]))][2]},{ko_point[(non_yakuman_han[max_index], int(head[:-1]))][1]})\n"
                else:
                    #print(f"{point_mangan[head][2] + point_mangan[head][1] * 2}/{point_mangan[head][2] + point_mangan[head][1]}({point_mangan[head][2]},{point_mangan[head][1]})")
                    st_han_output += f"{point_mangan[head][2] + point_mangan[head][1] * 2}/{point_mangan[head][2] + point_mangan[head][1]}({point_mangan[head][2]},{point_mangan[head][1]})\n"
            elif info[0] == "0":
                if head[-1] == "符":
                    #print(ko_point[(non_yakuman_han[max_index], int(head[:-1]))][0])
                    st_han_output += f"{ko_point[(non_yakuman_han[max_index], int(head[:-1]))][0]}"
                else:
                    #print(int(point_mangan[head][0]))
                    st_han_output += f"{int(point_mangan[head][0])}"
        except Exception:
            st_han_output += ["""庄家：未知点数
子家：未知点数""", """Dealer：Unknown Points
Non-Dealer：Unknown Points"""][lan]
        if cal_output:
            st.text(st_han_output)
            with st.expander(["符数计算", "Fu Calculation"][lan]):
                st.text(fu_cal)
        return_title = [return_title, non_yakuman_han[max_index]]
        return return_title

def ful_hand(hand_ipt):
    try:
        new_hand_ipt = ""
        hand_letter_index = []
        for letter in hand_ipt:
            if letter in ["m", "p", "s", "z"]:
                hand_letter_index.append(letter)
            else:
                hand_letter_index.append("")
        for index, letter in enumerate(hand_ipt):
            if letter == "a" or letter == "w":
                new_hand_ipt += letter
            elif letter not in ["m", "p", "s", "z"] and hand_ipt[index + 1] not in ["m", "p", "s", "z"]:
                new_hand_ipt += letter
                for l_index, l_letter in enumerate(hand_letter_index):
                    if l_letter in ["m", "p", "s", "z"] and l_index > index:
                        new_hand_ipt += l_letter
                        break
            else:
                new_hand_ipt += letter
        return new_hand_ipt
    except Exception:
        return ""


if "allow_yaku" not in st.session_state:
    st.session_state.allow_yaku = ["立直", "双立直", "段幺九", "门前清自摸和",
                "役牌：自风牌", "役牌：场风牌", "役牌：白", "役牌：发",
                "役牌：中", "平和", "一杯口", "二杯口",
                "一发", "岭上开花", "枪杠", "海底摸月",
                "河底捞鱼", "三色同刻", "三杠子", "对对和",
                "三暗刻", "小三元", "混老头", "纯全带幺九",
                "混全带幺九", "七对子", "一气通贯", "三色同顺",
                "清一色", "混一色",
                "国士无双", 
                "九莲宝灯", "四暗刻",
                "大三元", "小四喜",
                "字一色", "绿一色", "清老头",
                "四杠子", "天和", "地和"]
if "double_yakuman_open" not in st.session_state:
    st.session_state.double_yakuman_open = True

with st.sidebar:
    st.title("立直麻将计算器/ Riichi Mahjong Calculator")
    lan = ["简体中文","English"].index(st.selectbox("语言/Language", ["简体中文","English"]))
    st.text(["若使用手机/平板，使用横屏获得更佳体验 OwO","If using phone/tablet, switch to landscape mode for better experience OwO"][lan])
    page = st.selectbox(["功能导航","Function Navigate"][lan],[f"{["点数计算机", "Point Calculator"][lan]}", f"{["点数追踪", "Point Tracker"][lan]}", ["听牌计算机","Tenpai Calculator"][lan], ["清一色听牌练习","Chinitsu Tenpai Practice"][lan], ["反馈","Feedback"][lan]])
page = [f"{["点数计算机", "Point Calculator"][lan]}", f"{["点数追踪", "Point Tracker"][lan]}", ["听牌计算机","Tenpai Calculator"][lan], ["清一色听牌练习","Chinitsu Tenpai Practice"][lan], ["反馈","Feedback"][lan]].index(page) + 1
if page == 1:
    col125, col126 = st.columns([5,1])
    with col125:
        st.title(f"{["点数计算机", "Point Calcuator"][lan]}")
    with col126:
        st.text("")
        st.text("")
        @st.dialog(["役种设置","Yaku Setting"][lan])
        def yaku_set():

            set_yakuman, set_yaku, set_old_yaku = st.tabs(["役满","一般役","古役"])
            with set_yakuman:
                st.session_state.double_yakuman_open = st.toggle(f"{['国士无双十三面，纯正九莲宝灯，四暗刻单骑，大四喜计为双倍役满', 'Kokushi Muso Juusanmen, Junsei Churen Poto, Suu Ankou Tanki, Dai Suushi are double yakuman'][lan]}", value=st.session_state.double_yakuman_open)
                # 国士无双
                if st.toggle("国士无双/国士无双十三面", value = "国士无双" in st.session_state.allow_yaku, help = "所有幺九牌各一张+任意一张幺九牌"):
                    if "国士无双" not in st.session_state.allow_yaku:
                        st.session_state.allow_yaku.append("国士无双")
                else:
                    if "国士无双" in st.session_state.allow_yaku:
                        st.session_state.allow_yaku.remove("国士无双")
                # 九莲宝灯
                if st.toggle("九莲宝灯/纯正九莲宝灯", value = "九莲宝灯" in st.session_state.allow_yaku, help = "1112345678999+任意数牌构成的清一色"):
                    if "九莲宝灯" not in st.session_state.allow_yaku:
                        st.session_state.allow_yaku.append("九莲宝灯")
                else:
                    if "九莲宝灯" in st.session_state.allow_yaku:
                        st.session_state.allow_yaku.remove("九莲宝灯")
                # 四暗刻
                if st.toggle("四暗刻/四暗刻单骑", value = "四暗刻" in st.session_state.allow_yaku, help = "4组没有碰的刻子"):
                    if "四暗刻" not in st.session_state.allow_yaku:
                        st.session_state.allow_yaku.append("四暗刻")
                else:
                    if "四暗刻" in st.session_state.allow_yaku:
                        st.session_state.allow_yaku.remove("四暗刻")
                # 大三元
                if st.toggle("大三元", value = "大三元" in st.session_state.allow_yaku, help = "白发中的刻子"):
                    if "大三元" not in st.session_state.allow_yaku:
                        st.session_state.allow_yaku.append("大三元")
                else:
                    if "大三元" in st.session_state.allow_yaku:
                        st.session_state.allow_yaku.remove("大三元")
                # 小四喜
                if st.toggle("小四喜/大四喜", value = "小四喜" in st.session_state.allow_yaku, help = "四种四喜牌且至少三种四喜牌的刻子"):
                    if "小四喜" not in st.session_state.allow_yaku:
                        st.session_state.allow_yaku.append("小四喜")
                else:
                    if "小四喜" in st.session_state.allow_yaku:
                        st.session_state.allow_yaku.remove("小四喜")
                # 字一色
                if st.toggle("字一色", value = "字一色" in st.session_state.allow_yaku, help = "全是字牌"):
                    if "字一色" not in st.session_state.allow_yaku:
                        st.session_state.allow_yaku.append("字一色")
                else:
                    if "字一色" in st.session_state.allow_yaku:
                        st.session_state.allow_yaku.remove("字一色")
                # 绿一色
                if st.toggle("绿一色", value = "绿一色" in st.session_state.allow_yaku, help = "全是绿牌(23468索和发)"):
                    if "绿一色" not in st.session_state.allow_yaku:
                        st.session_state.allow_yaku.append("绿一色")
                else:
                    if "绿一色" in st.session_state.allow_yaku:
                        st.session_state.allow_yaku.remove("绿一色")
                # 清老头
                if st.toggle("清老头", value = "清老头" in st.session_state.allow_yaku, help = "全是老头牌(1或9)"):
                    if "清老头" not in st.session_state.allow_yaku:
                        st.session_state.allow_yaku.append("清老头")
                else:
                    if "清老头" in st.session_state.allow_yaku:
                        st.session_state.allow_yaku.remove("清老头")
                # 四杠子
                if st.toggle("四杠子", value = "四杠子" in st.session_state.allow_yaku, help = "开杠四次"):
                    if "四杠子" not in st.session_state.allow_yaku:
                        st.session_state.allow_yaku.append("四杠子")
                else:
                    if "四杠子" in st.session_state.allow_yaku:
                        st.session_state.allow_yaku.remove("四杠子")
                # 天和
                if st.toggle("天和", value = "天和" in st.session_state.allow_yaku, help = "庄家第一巡自摸"):
                    if "天和" not in st.session_state.allow_yaku:
                        st.session_state.allow_yaku.append("天和")
                else:
                    if "天和" in st.session_state.allow_yaku:
                        st.session_state.allow_yaku.remove("天和")
                # 地和
                if st.toggle("地和", value = "地和" in st.session_state.allow_yaku, help = "闲家第一巡自摸且无人鸣牌"):
                    if "地和" not in st.session_state.allow_yaku:
                        st.session_state.allow_yaku.append("地和")
                else:
                    if "地和" in st.session_state.allow_yaku:
                        st.session_state.allow_yaku.remove("地和")
            with set_yaku:
                # 立直
                if st.toggle("立直", value = "立直" in st.session_state.allow_yaku, help = "立直后和牌"):
                    if "立直" not in st.session_state.allow_yaku:
                        st.session_state.allow_yaku.append("立直")
                else:
                    if "立直" in st.session_state.allow_yaku:
                        st.session_state.allow_yaku.remove("立直")
                # 双立直
                if st.toggle("双立直", value = "双立直" in st.session_state.allow_yaku, help = "无人鸣牌时第一巡立直"):
                    if "双立直" not in st.session_state.allow_yaku:
                        st.session_state.allow_yaku.append("双立直")
                else:
                    if "双立直" in st.session_state.allow_yaku:
                        st.session_state.allow_yaku.remove("双立直")
                # 段幺九
                if st.toggle("段幺九", value = "段幺九" in st.session_state.allow_yaku, help = "没有幺九牌"):
                    if "段幺九" not in st.session_state.allow_yaku:
                        st.session_state.allow_yaku.append("段幺九")
                else:
                    if "段幺九" in st.session_state.allow_yaku:
                        st.session_state.allow_yaku.remove("段幺九")
                # 门前清自摸和
                if st.toggle("门前清自摸和", value = "门前清自摸和" in st.session_state.allow_yaku, help = "无副露时自摸和牌"):
                    if "门前清自摸和" not in st.session_state.allow_yaku:
                        st.session_state.allow_yaku.append("门前清自摸和")
                else:
                    if "门前清自摸和" in st.session_state.allow_yaku:
                        st.session_state.allow_yaku.remove("门前清自摸和")
                # 役牌：自风牌
                if st.toggle("役牌：自风牌", value = "役牌：自风牌" in st.session_state.allow_yaku, help = "自风牌刻子"):
                    if "役牌：自风牌" not in st.session_state.allow_yaku:
                        st.session_state.allow_yaku.append("役牌：自风牌")
                else:
                    if "役牌：自风牌" in st.session_state.allow_yaku:
                        st.session_state.allow_yaku.remove("役牌：自风牌")
                # 役牌：场风牌
                if st.toggle("役牌：场风牌", value = "役牌：场风牌" in st.session_state.allow_yaku, help = "场风牌刻子"):
                    if "役牌：场风牌" not in st.session_state.allow_yaku:
                        st.session_state.allow_yaku.append("役牌：场风牌")
                else:
                    if "役牌：场风牌" in st.session_state.allow_yaku:
                        st.session_state.allow_yaku.remove("役牌：场风牌")
                # 役牌：白
                if st.toggle("役牌：白", value = "役牌：白" in st.session_state.allow_yaku, help = "白刻子"):
                    if "役牌：白" not in st.session_state.allow_yaku:
                        st.session_state.allow_yaku.append("役牌：白")
                else:
                    if "役牌：白" in st.session_state.allow_yaku:
                        st.session_state.allow_yaku.remove("役牌：白")
                # 役牌：发
                if st.toggle("役牌：发", value = "役牌：发" in st.session_state.allow_yaku, help = "发刻子"):
                    if "役牌：发" not in st.session_state.allow_yaku:
                        st.session_state.allow_yaku.append("役牌：发")
                else:
                    if "役牌：发" in st.session_state.allow_yaku:
                        st.session_state.allow_yaku.remove("役牌：发")
                # 役牌：中
                if st.toggle("役牌：中", value = "役牌：中" in st.session_state.allow_yaku, help = "中刻子"):
                    if "役牌：中" not in st.session_state.allow_yaku:
                        st.session_state.allow_yaku.append("役牌：中")
                else:
                    if "役牌：中" in st.session_state.allow_yaku:
                        st.session_state.allow_yaku.remove("役牌：中")
                # 平和
                if st.toggle("平和", value = "平和" in st.session_state.allow_yaku, help = "4顺子+不是役牌的雀头+2面听"):
                    if "平和" not in st.session_state.allow_yaku:
                        st.session_state.allow_yaku.append("平和")
                else:
                    if "平和" in st.session_state.allow_yaku:
                        st.session_state.allow_yaku.remove("平和")
                # 一杯口
                if st.toggle("一杯口", value = "一杯口" in st.session_state.allow_yaku, help = "两组一样的顺子"):
                    if "一杯口" not in st.session_state.allow_yaku:
                        st.session_state.allow_yaku.append("一杯口")
                else:
                    if "一杯口" in st.session_state.allow_yaku:
                        st.session_state.allow_yaku.remove("一杯口")
                # 二杯口
                if st.toggle("二杯口", value = "二杯口" in st.session_state.allow_yaku, help = "两组一杯口"):
                    if "二杯口" not in st.session_state.allow_yaku:
                        st.session_state.allow_yaku.append("二杯口")
                else:
                    if "二杯口" in st.session_state.allow_yaku:
                        st.session_state.allow_yaku.remove("二杯口")
                # 一发
                if st.toggle("一发", value = "一发" in st.session_state.allow_yaku, help = "无人鸣牌时立直后一巡内和牌"):
                    if "一发" not in st.session_state.allow_yaku:
                        st.session_state.allow_yaku.append("一发")
                else:
                    if "一发" in st.session_state.allow_yaku:
                        st.session_state.allow_yaku.remove("一发")
                # 岭上开花
                if st.toggle("岭上开花", value = "岭上开花" in st.session_state.allow_yaku, help = "摸岭上牌和牌"):
                    if "岭上开花" not in st.session_state.allow_yaku:
                        st.session_state.allow_yaku.append("岭上开花")
                else:
                    if "岭上开花" in st.session_state.allow_yaku:
                        st.session_state.allow_yaku.remove("岭上开花")
                # 枪杠
                if st.toggle("枪杠", value = "枪杠" in st.session_state.allow_yaku, help = "荣和加杠"):
                    if "枪杠" not in st.session_state.allow_yaku:
                        st.session_state.allow_yaku.append("枪杠")
                else:
                    if "枪杠" in st.session_state.allow_yaku:
                        st.session_state.allow_yaku.remove("枪杠")
                # 海底摸月
                if st.toggle("海底摸月", value = "海底摸月" in st.session_state.allow_yaku, help = "最后一张牌自摸和牌"):
                    if "海底摸月" not in st.session_state.allow_yaku:
                        st.session_state.allow_yaku.append("海底摸月")
                else:
                    if "海底摸月" in st.session_state.allow_yaku:
                        st.session_state.allow_yaku.remove("海底摸月")
                # 河底捞鱼
                if st.toggle("河底捞鱼", value = "河底捞鱼" in st.session_state.allow_yaku, help = "最后一张牌荣和"):
                    if "河底捞鱼" not in st.session_state.allow_yaku:
                        st.session_state.allow_yaku.append("河底捞鱼")
                else:
                    if "河底捞鱼" in st.session_state.allow_yaku:
                        st.session_state.allow_yaku.remove("河底捞鱼")
                # 三色同刻
                if st.toggle("三色同刻", value = "三色同刻" in st.session_state.allow_yaku, help = "三组同数字的刻子"):
                    if "三色同刻" not in st.session_state.allow_yaku:
                        st.session_state.allow_yaku.append("三色同刻")
                else:
                    if "三色同刻" in st.session_state.allow_yaku:
                        st.session_state.allow_yaku.remove("三色同刻")
                # 三杠子
                if st.toggle("三杠子", value = "三杠子" in st.session_state.allow_yaku, help = "开杠三次"):
                    if "三杠子" not in st.session_state.allow_yaku:
                        st.session_state.allow_yaku.append("三杠子")
                else:
                    if "三杠子" in st.session_state.allow_yaku:
                        st.session_state.allow_yaku.remove("三杠子")
                # 对对和
                if st.toggle("对对和", value = "对对和" in st.session_state.allow_yaku, help = "全是刻子"):
                    if "对对和" not in st.session_state.allow_yaku:
                        st.session_state.allow_yaku.append("对对和")
                else:
                    if "对对和" in st.session_state.allow_yaku:
                        st.session_state.allow_yaku.remove("对对和")
                # 三暗刻
                if st.toggle("三暗刻", value = "三暗刻" in st.session_state.allow_yaku, help = "三组没有碰的刻子"):
                    if "三暗刻" not in st.session_state.allow_yaku:
                        st.session_state.allow_yaku.append("三暗刻")
                else:
                    if "三暗刻" in st.session_state.allow_yaku:
                        st.session_state.allow_yaku.remove("三暗刻")
                # 小三元
                if st.toggle("小三元", value = "小三元" in st.session_state.allow_yaku, help = "2组白发中的刻子+1组白发中的对子"):
                    if "小三元" not in st.session_state.allow_yaku:
                        st.session_state.allow_yaku.append("小三元")
                else:
                    if "小三元" in st.session_state.allow_yaku:
                        st.session_state.allow_yaku.remove("小三元")
                # 混老头
                if st.toggle("混老头", value = "混老头" in st.session_state.allow_yaku, help = "全是幺九牌"):
                    if "混老头" not in st.session_state.allow_yaku:
                        st.session_state.allow_yaku.append("混老头")
                else:
                    if "混老头" in st.session_state.allow_yaku:
                        st.session_state.allow_yaku.remove("混老头")
                # 纯全带幺九
                if st.toggle("纯全带幺九", value = "纯全带幺九" in st.session_state.allow_yaku, help = "所有面子都包含老头牌"):
                    if "纯全带幺九" not in st.session_state.allow_yaku:
                        st.session_state.allow_yaku.append("纯全带幺九")
                else:
                    if "纯全带幺九" in st.session_state.allow_yaku:
                        st.session_state.allow_yaku.remove("纯全带幺九")
                # 混全带幺九
                if st.toggle("混全带幺九", value = "混全带幺九" in st.session_state.allow_yaku, help = "所有面子都包含幺九牌"):
                    if "混全带幺九" not in st.session_state.allow_yaku:
                        st.session_state.allow_yaku.append("混全带幺九")
                else:
                    if "混全带幺九" in st.session_state.allow_yaku:
                        st.session_state.allow_yaku.remove("混全带幺九")
                # 七对子
                if st.toggle("七对子", value = "七对子" in st.session_state.allow_yaku, help = "7组对子"):
                    if "七对子" not in st.session_state.allow_yaku:
                        st.session_state.allow_yaku.append("七对子")
                else:
                    if "七对子" in st.session_state.allow_yaku:
                        st.session_state.allow_yaku.remove("七对子")
                # 一气通贯
                if st.toggle("一气通贯", value = "一气通贯" in st.session_state.allow_yaku, help = "同种数牌的123,456,789顺子"):
                    if "一气通贯" not in st.session_state.allow_yaku:
                        st.session_state.allow_yaku.append("一气通贯")
                else:
                    if "一气通贯" in st.session_state.allow_yaku:
                        st.session_state.allow_yaku.remove("一气通贯")
                # 三色同顺
                if st.toggle("三色同顺", value = "三色同顺" in st.session_state.allow_yaku, help = "三种数牌有相同数字的顺子"):
                    if "三色同顺" not in st.session_state.allow_yaku:
                        st.session_state.allow_yaku.append("三色同顺")
                else:
                    if "三色同顺" in st.session_state.allow_yaku:
                        st.session_state.allow_yaku.remove("三色同顺")
                # 清一色
                if st.toggle("清一色", value = "清一色" in st.session_state.allow_yaku, help = "只包含一种数牌"):
                    if "清一色" not in st.session_state.allow_yaku:
                        st.session_state.allow_yaku.append("清一色")
                else:
                    if "清一色" in st.session_state.allow_yaku:
                        st.session_state.allow_yaku.remove("清一色")
                # 混一色
                if st.toggle("混一色", value = "混一色" in st.session_state.allow_yaku, help = "只包含一组数牌+字牌"):
                    if "混一色" not in st.session_state.allow_yaku:
                        st.session_state.allow_yaku.append("混一色")
                else:
                    if "混一色" in st.session_state.allow_yaku:
                        st.session_state.allow_yaku.remove("混一色")
            with set_old_yaku:
                # 大七星
                if st.toggle("大七星", value = "大七星" in st.session_state.allow_yaku, help = "七种字牌组成的七对子"):
                    if "大七星" not in st.session_state.allow_yaku:
                        st.session_state.allow_yaku.append("大七星")
                else:
                    if "大七星" in st.session_state.allow_yaku:
                        st.session_state.allow_yaku.remove("大七星")
                # 大竹林
                if st.toggle("大竹林", value = "大竹林" in st.session_state.allow_yaku, help = "22334455667788索"):
                    if "大竹林" not in st.session_state.allow_yaku:
                        st.session_state.allow_yaku.append("大竹林")
                else:
                    if "大竹林" in st.session_state.allow_yaku:
                        st.session_state.allow_yaku.remove("大竹林")
                # 大车轮
                if st.toggle("大车轮", value = "大车轮" in st.session_state.allow_yaku, help = "22334455667788饼"):
                    if "大车轮" not in st.session_state.allow_yaku:
                        st.session_state.allow_yaku.append("大车轮")
                else:
                    if "大车轮" in st.session_state.allow_yaku:
                        st.session_state.allow_yaku.remove("大车轮")
                # 大数邻
                if st.toggle("大数邻", value = "大数邻" in st.session_state.allow_yaku, help = "22334455667788万"):
                    if "大数邻" not in st.session_state.allow_yaku:
                        st.session_state.allow_yaku.append("大数邻")
                else:
                    if "大数邻" in st.session_state.allow_yaku:
                        st.session_state.allow_yaku.remove("大数邻")
                # 石上三年
                if st.toggle("石上三年", value = "石上三年" in st.session_state.allow_yaku, help = "双立直+海底"):
                    if "石上三年" not in st.session_state.allow_yaku:
                        st.session_state.allow_yaku.append("石上三年")
                else:
                    if "石上三年" in st.session_state.allow_yaku:
                        st.session_state.allow_yaku.remove("石上三年")
                # 四连刻
                if st.toggle("四连刻", value = "四连刻" in st.session_state.allow_yaku, help = "同种数牌连续数字的四个刻子"):
                    if "四连刻" not in st.session_state.allow_yaku:
                        st.session_state.allow_yaku.append("四连刻")
                else:
                    if "四连刻" in st.session_state.allow_yaku:
                        st.session_state.allow_yaku.remove("四连刻")
                # 黑一色
                if st.toggle("黑一色", value = "黑一色" in st.session_state.allow_yaku, help = "全是黑牌(248饼和风牌)"):
                    if "黑一色" not in st.session_state.allow_yaku:
                        st.session_state.allow_yaku.append("黑一色")
                else:
                    if "黑一色" in st.session_state.allow_yaku:
                        st.session_state.allow_yaku.remove("黑一色")
                # 红孔雀
                if st.toggle("红孔雀", value = "红孔雀" in st.session_state.allow_yaku, help = "只包含1579索和中"):
                    if "红孔雀" not in st.session_state.allow_yaku:
                        st.session_state.allow_yaku.append("红孔雀")
                else:
                    if "红孔雀" in st.session_state.allow_yaku:
                        st.session_state.allow_yaku.remove("红孔雀")

            if st.button(["保存","Save"][lan]):
                st.rerun()
            if st.button(["重置设置","Reset"][lan]):
                st.session_state.allow_yaku = ["立直", "双立直", "段幺九", "门前清自摸和",
                "役牌：自风牌", "役牌：场风牌", "役牌：白", "役牌：发",
                "役牌：中", "平和", "一杯口", "二杯口",
                "一发", "岭上开花", "枪杠", "海底摸月",
                "河底捞鱼", "三色同刻", "三杠子", "对对和",
                "三暗刻", "小三元", "混老头", "纯全带幺九",
                "混全带幺九", "七对子", "一气通贯", "三色同顺",
                "清一色", "混一色",
                "国士无双", 
                "九莲宝灯", "四暗刻",
                "大三元", "小四喜",
                "字一色", "绿一色", "清老头",
                "四杠子", "天和", "地和"]
                st.session_state.double_yakuman_open = True
                st.rerun()

        if st.button(["役种设置","Yaku Setting"][lan]):
            yaku_set()
    ipt1 = ful_hand(st.text_input(f"{["手牌（和的牌填最后）", "Hand（Put the winning tile at the end）"][lan]}",help=["例:123406789s11122z (和的牌是2z)","Example:123456789s11122z (2z is the winning tile)"][lan]).lower().replace(" ",""))
    col11, col12, col13, col14 = st.columns(4)
    with col11:
        ipt2 = ful_hand(st.text_input(f"{["副露1", "Meld1"][lan]}",help=["例:123s","Example:123s"][lan]).lower().replace(" ",""))
    with col12:
        ipt3 = ful_hand(st.text_input(f"{["副露2", "Meld2"][lan]}",help=["例:444s","Example:444s"][lan]).lower().replace(" ",""))
    with col13:
        ipt4 = ful_hand(st.text_input(f"{["副露3", "Meld3"][lan]}",help=["例:6666s","Example:6666s"][lan]).lower().replace(" ",""))
    with col14:
        ipt5 = ful_hand(st.text_input(f"{["副露4", "Meld4"][lan]}",help=["例:8888sa","Example:8888sa"][lan]).lower().replace(" ",""))
    with st.expander(["如何输入手牌","How To Input Tiles"][lan]):
        st.image("https://blog-imgs-136.fc2.com/k/o/n/konoyonohana/mahjong01.png")
        if lan == 0:
            st.text("多张同花色的牌可以只写一次字母，例如123m123s123p111z11m")
            st.text("在副露区填写暗杠时，在杠子后面加一个a，例如3s3s3s3sa或3333sa")
        elif lan == 1:
            st.text("Tiles with same suit can write the letter only once, for example 123m123s123p111z11m")
            st.text("For closed kan in the meld area, add \"a\" at the end, for example 3s3s3s3sa or 3333sa")
    ipt6 = st.selectbox(f"{["自摸/荣", "Tsumo/Ron"][lan]}",[["自摸","荣"],["Tsumo","Ron"]][lan])
    if ipt6 == "Tsumo":
        ipt6 = "自摸"
    elif ipt6 == "Ron":
        ipt6 = "荣"
    ipt7 = st.multiselect(f"{["和牌状态", "Winning Conditions"][lan]}",[["立直","双立直","一发","枪杠","岭上开花","天和","地和","海底"],["Riichi", "Daburu Riichi", "Ippatsu", "Chankan", "Rinshan Kaiho", "Tenho", "Chiho", "Haitei"]][lan])
    if lan == 1:
        ipt7_tran = {"Riichi": "立直", "Daburu Riichi": "双立直", "Ippatsu": "一发", "Chankan": "枪杠",
                         "Rinshan Kaiho": "岭上开花", "Tenho": "天和", "Chiho": "地和", "Haitei": "海底"}
        ipt7_chn = []
        for eng in ipt7:
            ipt7_chn.append(ipt7_tran[eng])
        ipt7 = ipt7_chn.copy()

    col31, col32 = st.columns(2)
    with col31:
        ipt8 = st.text_input(f"{["宝牌指示牌（如果立直了请把里宝牌也加上）", "Dora Indicator（If Riichi, Include Ura-Dora）"][lan]}",help=["例:2z0p (宝牌是南和红5饼)","Example:2z0p (Dora is 2z and 0p)"][lan])
    with col32:
        ipt12 = st.slider(f"{["拔北宝牌", "Kita Dora"][lan]}", min_value=0, max_value=4, step=1)
    col21, col22 = st.columns(2)
    with col21:
        ipt9 = st.selectbox(f"{["场风", "Round Wind"][lan]}",[["东","南","西","北"],["East","South","West","North"]][lan])
        if lan == 1:
            ipt910_tran = {"East": "东", "South": "南", "West": "西", "North": "北"}
            ipt9 = ipt910_tran[ipt9]
    with col22:
        ipt10 = st.selectbox(f"{["自风", "Seat Wind"][lan]}",[["东","南","西","北"],["East","South","West","North"]][lan])
        if lan == 1:
            ipt10 = ipt910_tran[ipt10]
    ipt11 = st.session_state.double_yakuman_open
    try:
    #if True:
        cal_ipt = ""
        cal_ipt += ipt1
        cal_ipt += ","
        if ipt2:
            cal_ipt += ipt2
            cal_ipt += "."
        if ipt3:
            cal_ipt += ipt3
            cal_ipt += "."
        if ipt4:
            cal_ipt += ipt4
            cal_ipt += "."
        if ipt5:
            cal_ipt += ipt5
            cal_ipt += "."
        while cal_ipt[-1] == ".":
            cal_ipt = cal_ipt[:-1]
        cal_ipt += ","

        if ipt6 == "自摸":
            cal_ipt += "1"
        else:
            cal_ipt += "0"

        if "双立直" in ipt7:
            cal_ipt += "2"
        elif "立直" in ipt7:
            cal_ipt += "1"
        else:
            cal_ipt += "0"

        if "一发" in ipt7:
            cal_ipt += "1"
        else:
            cal_ipt += "0"

        if "枪杠" in ipt7:
            cal_ipt += "1"
        elif "岭上开花" in ipt7:
            cal_ipt += "2"
        else:
            cal_ipt += "0"

        if "天和" in ipt7:
            cal_ipt += "1,"
        elif "地和" in ipt7:
            cal_ipt += "2,"
        elif "海底" in ipt7:
            cal_ipt += "3,"
        else:
            cal_ipt += "0,"

        dora_list = {"1s": "2s", "2s": "3s", "3s": "4s", "4s": "5s", "5s": "6s", "0s": "6s", "6s": "7s", "7s": "8s",
                "8s": "9s", "9s": "1s",
                "1p": "2p", "2p": "3p", "3p": "4p", "4p": "5p", "5p": "6p", "0p": "6p", "6p": "7p", "7p": "8p",
                "8p": "9p", "9p": "1p",
                "1m": "2m", "2m": "3m", "3m": "4m", "4m": "5m", "5m": "6m", "0m": "6m", "6m": "7m", "7m": "8m",
                "8m": "9m", "9m": "1m",
                "1z": "2z", "2z": "3z", "3z": "4z", "4z": "1z", "5z": "6z", "6z": "7z", "7z": "5z", "8z": "8z"}
        ipt8 = re.findall(r"[0-9][mpsz]", ipt8)
        for i in ipt8:
            cal_ipt += dora_list[i]
        cal_ipt += f"{"8z"*ipt12}"
        cal_ipt += ","

        cal_ipt += {"东":"1z","南":"2z","西":"3z","北":"4z"}[ipt9]
        cal_ipt += {"东":"1z","南":"2z","西":"3z","北":"4z"}[ipt10]

        if "w" not in ipt1:
            cal_han(cal_ipt, ipt11, lan, True, 0)
        else:
            ALL_W_TILE = ["1m","2m","3m","4m","5m","6m","7m","8m","9m",
                    "1s","2s","3s","4s","5s","6s","7s","8s","9s",
                    "1p","2p","3p","4p","5p","6p","7p","8p","9p",
                    "1z","2z","3z","4z","5z","6z","7z"]
            cal_ipt.replace("w","")
            w_han_list = []
            for w_tile in ALL_W_TILE:
                w_han_list.append(cal_han(w_tile + cal_ipt, ipt11, lan, False, 0)[1])
            w_max_index = w_han_list.index(max(w_han_list))
            cal_ipt = ALL_W_TILE[w_max_index] + cal_ipt
            if max(w_han_list) != -1:
                st.text([f"万象牌是{ALL_W_TILE[w_max_index]}",f"Wild Card Is {ALL_W_TILE[w_max_index]}"][lan])
            cal_han(cal_ipt, ipt11, lan, True, 0)

    except Exception:
        st.text(["计算结果会自动输出，若无输出请重新检查输入 AwA","Results are generated automatically. If nothing appears, please double-check your input AwA"][lan])

elif page == 2:
    han_fu_co_point = {"1番30符": (1000, 300, 500), "1番40符": (1300, 400, 700), "1番50符": (1600, 400, 800),
                       "1番60符": (2000, 500, 1000), "1番70符": (2300, 600, 1200), "1番80符": (2600, 700, 1300),
                       "1番90符": (2900, 800, 1500),
                       "1番100符": (3200, 800, 1600), "1番110符": (3600, 900, 1800), "2番20符": (1300, 400, 700),
                       "2番25符": (1600, 400, 800),
                       "2番30": (2000, 500, 1000), "2番40符": (2600, 700, 1300), "2番50符": (3200, 800, 1600),
                       "2番60符": (3900, 1000, 2000),
                       "2番70符": (4500, 1200, 2300), "2番80符": (5200, 1300, 2600), "2番90符": (5800, 1500, 2900),
                       "2番100符": (6400, 1600, 3200),
                       "2番110": (7100, 1800, 3600), "3番20符": (2600, 700, 1300), "3番25符": (3200, 800, 1600),
                       "3番30符": (3900, 1000, 2000),
                       "3番40符": (5200, 1300, 2600), "3番50符": (6400, 1600, 3200), "3番60符": (7700, 2000, 3900),
                       "4番20符": (5200, 1300, 2600),
                       "4番25符": (6400, 1600, 3200), "4番30符": (7700, 2000, 3900), "满贯": (8000, 2000, 4000),
                       "跳满": (12000, 6000, 3000),
                       "倍满": (16000, 8000, 4000), "三倍满": (24000, 12000, 6000), "累计役满": (32000, 16000, 8000),
                       "役满": (32000, 16000, 8000),
                       "双倍役满": (64000, 32000, 16000), "三倍役满": (96000, 48000, 24000),
                       "四倍役满": (128000, 64000, 32000),
                       "五倍役满": (160000, 80000, 40000), "六倍役满": (192000, 96000, 48000)}
    han_fu_oya_point = {
        "1番30符": (1500, 500, 500), "1番40符": (2000, 700, 700), "1番50符": (2400, 800, 800),
        "1番60符": (2900, 1000, 1000),
        "1番70符": (3400, 1200, 1200), "1番80符": (3900, 1300, 1300), "1番90符": (4400, 1500, 1500),
        "1番100符": (4800, 1600, 1600), "1番110符": (5300, 1800, 1800), "2番20符": (2000, 700, 700),
        "2番25符": (2400, 800, 800), "2番30": (2900, 1000, 1000), "2番40符": (3900, 1300, 1300),
        "2番50符": (4800, 1600, 1600), "2番60符": (5800, 2000, 2000), "2番70符": (6800, 2300, 2300),
        "2番80符": (7700, 2600, 2600), "2番90符": (8700, 2900, 2900), "2番100符": (9600, 3200, 3200),
        "2番110": (10600, 3600, 3600), "3番20符": (3900, 1300, 1300), "3番25符": (4800, 1600, 1600),
        "3番30符": (5800, 2000, 2000), "3番40符": (7700, 2600, 2600), "3番50符": (9600, 3200, 3200),
        "3番60符": (11600, 3900, 3900), "4番20符": (7700, 2600, 2600), "4番25符": (9600, 3200, 3200),
        "4番30符": (11600, 3900, 3900), "满贯": (12000, 4000, 4000), "跳满": (18000, 6000, 6000),
        "倍满": (24000, 8000, 8000), "三倍满": (36000, 12000, 12000), "累计役满": (48000, 16000, 16000),
        "役满": (48000, 16000, 16000), "双倍役满": (96000, 32000, 32000), "三倍役满": (144000, 48000, 48000),
        "四倍役满": (192000, 64000, 64000), "五倍役满": (240000, 80000, 80000), "六倍役满": (288000, 96000, 96000)}
    st.title(f"{["点数追踪","Point Tracker"][lan]}")
    trackermode1, trackermode2 = st.columns(2)
    with trackermode1:
        trackermode = st.selectbox(["人数","Player Number"][lan],[["四人麻将","三人麻将"],["4 Players","3 Players"]][lan])
        st.text("")
    if trackermode == "四人麻将" or trackermode == "4 Players":
        error_message = ""
        if 'player_list4' not in st.session_state:
            st.session_state.player_list4 = []
        if "start4" not in st.session_state:
            st.session_state.start4 = False
        if "point_history4" not in st.session_state:
            st.session_state.point_history4 = []
        if st.session_state.start4 == False:
            col51, col52 = st.columns([4,1])
            with col51:
                insert_player = st.chat_input(["添加玩家","Insert Player"][lan])
                if insert_player and insert_player not in st.session_state.player_list4 and len(st.session_state.player_list4) <= 4: 
                    insert_player = insert_player[0:6]
                    st.session_state.player_list4.append(insert_player)
            with col52:
                if st.button(["移除玩家","Remove Player"][lan]):
                    try:
                        st.session_state.player_list4.pop()
                    except Exception:
                        pass
        player_col1, player_col2, player_col3, player_col4 = st.columns(4)
        with player_col1:
            if len(st.session_state.player_list4) >= 1:
                st.markdown(f"<h2 style='text-align: center;'>{st.session_state.player_list4[0]}</h2>", unsafe_allow_html=True)
                if st.session_state.start4 == True:
                    st.markdown(f"<h3 style='text-align: center;'>{st.session_state.point_list4[0]}</h3>",unsafe_allow_html=True)
        with player_col2:
            if len(st.session_state.player_list4) >= 2:
                st.markdown(f"<h2 style='text-align: center;'>{st.session_state.player_list4[1]}</h2>", unsafe_allow_html=True)
                if st.session_state.start4 == True:
                    st.markdown(f"<h3 style='text-align: center;'>{st.session_state.point_list4[1]}</h3>",unsafe_allow_html=True)
        with player_col3:
            if len(st.session_state.player_list4) >= 3:
                st.markdown(f"<h2 style='text-align: center;'>{st.session_state.player_list4[2]}</h2>", unsafe_allow_html=True)
                if st.session_state.start4 == True:
                    st.markdown(f"<h3 style='text-align: center;'>{st.session_state.point_list4[2]}</h3>",unsafe_allow_html=True)
        with player_col4:
            if len(st.session_state.player_list4) >= 4:
                st.markdown(f"<h2 style='text-align: center;'>{st.session_state.player_list4[3]}</h2>", unsafe_allow_html=True)
                if st.session_state.start4 == True:
                    st.markdown(f"<h3 style='text-align: center;'>{st.session_state.point_list4[3]}</h3>",unsafe_allow_html=True)
        if len(st.session_state.player_list4) == 4:
            if st.session_state.start4 == False:
                start_point = st.number_input(["起始点数","Starting Points"][lan], min_value = 0, max_value = 50000, value = 25000)
                stick = st.number_input(["本场棒","Honba Stick"][lan], min_value = 100, max_value = 500, value = 300)
                st.session_state.stick4 = stick
                notin = st.number_input(["没听罚符","Noten Penalty"][lan], min_value = 500, max_value = 2000, value = 1000)
                st.session_state.notin4 = notin
                if st.button(["开始对局","Start The Game"][lan]):
                    st.session_state.start4 = True
                    st.session_state.point_list4 = [start_point, start_point, start_point, start_point, 0]
                    st.session_state.point_history4.append(st.session_state.point_list4.copy())
                    st.rerun()
            else:
                st.markdown("<br>", unsafe_allow_html=True)
                col41, col43, col44, col45, col46 = st.columns([2,1,1,1,1])
                with col41:
                    t_zhuang = st.select_slider(["庄家","Dealer"][lan],options=st.session_state.player_list4, value = st.session_state.player_list4[0])
                with col43:
                    if st.button(f"{st.session_state.player_list4[0]}\n{["立直","Riichi"][lan]}"):
                        st.session_state.point_list4[0] -= 1000
                        st.session_state.point_list4[4] += 1000
                        st.session_state.point_history4.append(st.session_state.point_list4.copy())
                        st.rerun()
                with col44:
                    if st.button(f"{st.session_state.player_list4[1]}\n{["立直","Riichi"][lan]}"):
                        st.session_state.point_list4[1] -= 1000
                        st.session_state.point_list4[4] += 1000
                        st.session_state.point_history4.append(st.session_state.point_list4.copy())
                        st.rerun()
                with col45:
                    if st.button(f"{st.session_state.player_list4[2]}\n{["立直","Riichi"][lan]}"):
                        st.session_state.point_list4[2] -= 1000
                        st.session_state.point_list4[4] += 1000
                        st.session_state.point_history4.append(st.session_state.point_list4.copy())
                        st.rerun()
                with col46:
                    if st.button(f"{st.session_state.player_list4[3]}\n{["立直","Riichi"][lan]}"):
                        st.session_state.point_list4[3] -= 1000
                        st.session_state.point_list4[4] += 1000
                        st.session_state.point_history4.append(st.session_state.point_list4.copy())
                        st.rerun()
                col71, col72 = st.columns([2,9])
                with col72:
                    benchang4 = st.slider(["本场数","Honba Count"][lan],min_value = 0, max_value = 15)
                with col71:
                    st.text(f"{["立直棒","Riichi"][lan]}：{st.session_state.point_list4[4]}")
                    st.text(f"{["本场棒","Honba Stick"][lan]}：{st.session_state.stick4*benchang4}")
                col51, col52, col53, col54 = st.columns([2, 3, 3, 3])
                with col52:
                    winner4 = st.select_slider(["和牌","Winner"][lan],options=st.session_state.player_list4, value = st.session_state.player_list4[0])
                with col53:
                    loser_list4 = st.session_state.player_list4.copy()
                    if lan == 0:
                        loser_list4.append("自摸")
                    else:
                        loser_list4.append("Tsumo")
                    loser4 = st.select_slider(["放铳","Ron Discarder"][lan],options=loser_list4, value = st.session_state.player_list4[0])
                    if loser4 == "Tsumo":
                        loser4 = "自摸"
                with col54:
                    if lan == 0:
                        han_fu_list = ["1番30符","1番40符","1番50符","1番60符","1番70符","1番80符","1番90符","1番100符","1番110符",
                                   "2番20符","2番25符","2番30符","2番40符","2番50符","2番60符","2番70符","2番80符","2番90符","2番100符","2番110符",
                                   "3番20符","3番25符","3番30符","3番40符","3番50符","3番60符","4番20符","4番25符","4番30符","满贯","跳满","倍满",
                                   "三倍满","累计役满","役满","双倍役满","三倍役满","四倍役满","五倍役满","六倍役满"]
                    else:
                        han_fu_list = ["1 Han 30 Fu", "1 Han 40 Fu", "1 Han 50 Fu", "1 Han 60 Fu", "1 Han 70 Fu", "1 Han 80 Fu", "1 Han 90 Fu", "1 Han 100 Fu", "1 Han 110 Fu",
                                    "2 Han 20 Fu", "2 Han 25 Fu", "2 Han 30 Fu", "2 Han 40 Fu", "2 Han 50 Fu", "2 Han 60 Fu", "2 Han 70 Fu", "2 Han 80 Fu", "2 Han 90 Fu", "2 Han 100 Fu", "2 Han 110 Fu",
                                    "3 Han 20 Fu", "3 Han 25 Fu", "3 Han 30 Fu", "3 Han 40 Fu", "3 Han 50 Fu", "3 Han 60 Fu",
                                    "4 Han 20 Fu", "4 Han 25 Fu", "4 Han 30 Fu",
                                    "Mangan", "Haneman", "Baiman", "Sanbaiman", "Kazoe Yakuman", "Yakuman",
                                    "Double Yakuman", "Triple Yakuman", "Quadruple Yakuman", "Quintuple Yakuman", "Sextuple Yakuman"]
                    han_fu_tran = {"1 Han 30 Fu": "1番30符", "1 Han 40 Fu": "1番40符", "1 Han 50 Fu": "1番50符",
                        "1 Han 60 Fu": "1番60符", "1 Han 70 Fu": "1番70符", "1 Han 80 Fu": "1番80符",
                        "1 Han 90 Fu": "1番90符", "1 Han 100 Fu": "1番100符", "1 Han 110 Fu": "1番110符",
                        "2 Han 20 Fu": "2番20符", "2 Han 25 Fu": "2番25符", "2 Han 30 Fu": "2番30符",
                        "2 Han 40 Fu": "2番40符", "2 Han 50 Fu": "2番50符", "2 Han 60 Fu": "2番60符",
                        "2 Han 70 Fu": "2番70符", "2 Han 80 Fu": "2番80符", "2 Han 90 Fu": "2番90符",
                        "2 Han 100 Fu": "2番100符", "2 Han 110 Fu": "2番110符", "3 Han 20 Fu": "3番20符",
                        "3 Han 25 Fu": "3番25符", "3 Han 30 Fu": "3番30符", "3 Han 40 Fu": "3番40符",
                        "3 Han 50 Fu": "3番50符", "3 Han 60 Fu": "3番60符", "4 Han 20 Fu": "4番20符",
                        "4 Han 25 Fu": "4番25符", "4 Han 30 Fu": "4番30符", "Mangan": "满贯",
                        "Haneman": "跳满", "Baiman": "倍满", "Sanbaiman": "三倍满",
                        "Kazoe Yakuman": "累计役满", "Yakuman": "役满", "Double Yakuman": "双倍役满",
                        "Triple Yakuman": "三倍役满", "Quadruple Yakuman": "四倍役满", "Quintuple Yakuman": "五倍役满",
                        "Sextuple Yakuman": "六倍役满"}
                    win_han = st.selectbox(["番数/符数","Han/Fu"][lan], options=han_fu_list)
                    if lan == 1:
                        win_han = han_fu_tran[win_han]
                with col51:
                    if st.button(["和牌","Win"][lan]):
                        if winner4 != loser4:
                            st.session_state.point_list4[st.session_state.player_list4.index(winner4)] += st.session_state.point_list4[4]
                            st.session_state.point_list4[4] = 0
                            if winner4 == t_zhuang:
                                if loser4 == "自摸":
                                    zm_loser4 = st.session_state.player_list4.copy()
                                    zm_loser4.remove(winner4)
                                    for player in zm_loser4:
                                        st.session_state.point_list4[st.session_state.player_list4.index(player)] -= (han_fu_oya_point[win_han][1] + st.session_state.stick4*benchang4//3)
                                    st.session_state.point_list4[st.session_state.player_list4.index(winner4)] += (
                                            han_fu_oya_point[win_han][1] * 3 + st.session_state.stick4 * benchang4)
                                else:
                                    st.session_state.point_list4[st.session_state.player_list4.index(loser4)] -= (han_fu_oya_point[win_han][0] + st.session_state.stick4*benchang4)
                                    st.session_state.point_list4[st.session_state.player_list4.index(winner4)] += (han_fu_oya_point[win_han][0] + st.session_state.stick4*benchang4)
                            elif winner4 != t_zhuang:
                                if loser4 == "自摸":
                                    zm_loser4 = st.session_state.player_list4.copy()
                                    zm_loser4.remove(winner4)
                                    for player in zm_loser4:
                                        if player == t_zhuang:
                                            st.session_state.point_list4[st.session_state.player_list4.index(player)] -= (han_fu_co_point[win_han][2] + st.session_state.stick4*benchang4//3)
                                        else:
                                            st.session_state.point_list4[st.session_state.player_list4.index(player)] -= (han_fu_co_point[win_han][1] + st.session_state.stick4*benchang4//3)
                                    st.session_state.point_list4[st.session_state.player_list4.index(winner4)] += (
                                            han_fu_co_point[win_han][1] * 2 + han_fu_co_point[win_han][2] + st.session_state.stick4 * benchang4)
                                else:
                                    st.session_state.point_list4[st.session_state.player_list4.index(loser4)] -= (han_fu_co_point[win_han][0] + st.session_state.stick4*benchang4)
                                    st.session_state.point_list4[st.session_state.player_list4.index(winner4)] += (han_fu_co_point[win_han][0] + st.session_state.stick4*benchang4)
                            st.session_state.point_history4.append(st.session_state.point_list4.copy())
                            st.rerun()
                        else:
                            error_message=["不能荣和自己啊","You Can't Ron Yourself!!!"][lan]
                col61, col62 = st.columns([2,9])
                with col62:
                    tin_le = st.multiselect(["听牌","Tenpai"][lan], options=st.session_state.player_list4)
                with col61:
                    if st.button(["荒牌流局","Draw"][lan]):
                        for player in tin_le:
                            if len(tin_le) != 2:
                                st.session_state.point_list4[st.session_state.player_list4.index(player)] += st.session_state.notin4*(4-len(tin_le))
                            else:
                                st.session_state.point_list4[st.session_state.player_list4.index(player)] += st.session_state.notin4
                        for player in st.session_state.player_list4:
                            if tin_le and player not in tin_le:
                                if len(tin_le) != 2:
                                    st.session_state.point_list4[st.session_state.player_list4.index(player)] -= st.session_state.notin4 * (len(tin_le))
                                else:
                                    st.session_state.point_list4[st.session_state.player_list4.index(player)] -= st.session_state.notin4
                        st.session_state.point_history4.append(st.session_state.point_list4.copy())
                        st.rerun()
                col91, col92, col93 = st.columns([2,3,3])
                if "tz4" not in st.session_state:
                    st.session_state.tz4 = [1, 1]
                with col91:
                    if st.button(["抛🎲","Roll 🎲"][lan]):
                        st.session_state.tz4 = [random.randint(1, 6), random.randint(1, 6)]
                with col92:
                    st.markdown(f"<h2 style='text-align: center;'>[{st.session_state.tz4[0]}]</h2>",unsafe_allow_html=True)
                with col93:
                    st.markdown(f"<h2 style='text-align: center;'>[{st.session_state.tz4[1]}]</h2>",unsafe_allow_html=True)
                col81, col83, col82 = st.columns([1,3,1])
                with col81:
                    if st.button(["撤回操作","Undo"][lan]):
                        if len(st.session_state.point_history4) > 1:
                            st.session_state.point_history4.pop()
                            st.session_state.point_list4 = st.session_state.point_history4[-1].copy()
                            #print(st.session_state.point_history4)
                            #print(st.session_state.point_history4[-1])
                            st.rerun()
                        else:
                            error_message = ["没东西可以撤回了","There Is Nothing To Undo!!!"][lan]
                with col82:
                    if st.button(["结束对局","End The Game"][lan]):
                        st.session_state.start4 = False
                        st.session_state.point_history4 = []
                        st.rerun()
                @st.dialog(["手动修改","Manual Edit Point"][lan])
                def edit_4m():
                    edit0 = st.number_input(st.session_state.player_list4[0],value=st.session_state.point_list4[0])
                    edit1 = st.number_input(st.session_state.player_list4[1], value=st.session_state.point_list4[1])
                    edit2 = st.number_input(st.session_state.player_list4[2], value=st.session_state.point_list4[2])
                    edit3 = st.number_input(st.session_state.player_list4[3], value=st.session_state.point_list4[3])
                    if st.button(["修改","Edit"][lan]):
                        st.session_state.point_list4 = [edit0, edit1, edit2, edit3, st.session_state.point_list4[4]]
                        st.session_state.point_history4.append(st.session_state.point_list4.copy())
                        st.rerun()
                with col83:
                    if st.button(["手动修改","Manual Edit Point"][lan]):
                        edit_4m()
                if error_message:
                    st.error(error_message)
                    error_message = ""
        else:
            with trackermode2:
                st.text("")
                st.text("")
                st.text("")
                st.text(["(添加4个玩家以开始)","(Insert 4 Players to Continue)"][lan])
    else:
        error_message_3 = ""
        if 'player_list3' not in st.session_state:
            st.session_state.player_list3 = []
        if "start3" not in st.session_state:
            st.session_state.start3 = False
        if "point_history3" not in st.session_state:
            st.session_state.point_history3 = []
        if st.session_state.start3 == False:
            col351, col352 = st.columns([4, 1])
            with col351:
                insert_player_3 = st.chat_input(["添加玩家", "Insert Player"][lan],key="30")
                if insert_player_3 and insert_player_3 not in st.session_state.player_list3 and len(
                        st.session_state.player_list3) <= 3: st.session_state.player_list3.append(insert_player_3)
            with col352:
                if st.button(["移除玩家", "Remove Player"][lan],key="31"):
                    try:
                        st.session_state.player_list3.pop()
                    except Exception:
                        pass
        player_col31, player_col32, player_col33 = st.columns(3)
        with player_col31:
            if len(st.session_state.player_list3) >= 1:
                st.markdown(f"<h2 style='text-align: center;'>{st.session_state.player_list3[0]}</h2>",
                            unsafe_allow_html=True)
                if st.session_state.start3 == True:
                    st.markdown(f"<h3 style='text-align: center;'>{st.session_state.point_list3[0]}</h3>",
                                unsafe_allow_html=True)
        with player_col32:
            if len(st.session_state.player_list3) >= 2:
                st.markdown(f"<h2 style='text-align: center;'>{st.session_state.player_list3[1]}</h2>",
                            unsafe_allow_html=True)
                if st.session_state.start3 == True:
                    st.markdown(f"<h3 style='text-align: center;'>{st.session_state.point_list3[1]}</h3>",
                                unsafe_allow_html=True)
        with player_col33:
            if len(st.session_state.player_list3) >= 3:
                st.markdown(f"<h2 style='text-align: center;'>{st.session_state.player_list3[2]}</h2>",
                            unsafe_allow_html=True)
                if st.session_state.start3 == True:
                    st.markdown(f"<h3 style='text-align: center;'>{st.session_state.point_list3[2]}</h3>",
                                unsafe_allow_html=True)
        if len(st.session_state.player_list3) == 3:
            if st.session_state.start3 == False:
                start_point_3 = st.number_input(["起始点数", "Starting Points"][lan], min_value=0, max_value=50000,
                                              value=35000, key = "32")
                stick_3 = st.number_input(["本场棒", "Honba Stick"][lan], min_value=100, max_value=500, value=300, key = "33")
                st.session_state.stick3 = stick_3
                notin_3 = st.number_input(["没听罚符", "Noten Penalty"][lan], min_value=500, max_value=2000, value=1000, key = "34")
                st.session_state.notin3 = notin_3
                if st.button(["开始对局", "Start The Game"][lan], key = "35"):
                    st.session_state.start3 = True
                    st.session_state.point_list3 = [start_point_3, start_point_3, start_point_3, start_point_3, 0]
                    st.session_state.point_history3.append(st.session_state.point_list3.copy())
                    st.rerun()
            else:
                st.markdown("<br>", unsafe_allow_html=True)
                col341, col343, col344, col345 = st.columns([2, 1, 1, 1])
                with col341:
                    t_zhuang_3 = st.select_slider(["庄家", "Dealer"][lan], options=st.session_state.player_list3, value=st.session_state.player_list3[0], key = "36")
                with col343:
                    if st.button(f"{st.session_state.player_list3[0]}\n{["立直", "Riichi"][lan]}", key = "37"):
                        st.session_state.point_list3[0] -= 1000
                        st.session_state.point_list3[4] += 1000
                        st.session_state.point_history3.append(st.session_state.point_list3.copy())
                        st.rerun()
                with col344:
                    if st.button(f"{st.session_state.player_list3[1]}\n{["立直", "Riichi"][lan]}", key = "38"):
                        st.session_state.point_list3[1] -= 1000
                        st.session_state.point_list3[4] += 1000
                        st.session_state.point_history3.append(st.session_state.point_list3.copy())
                        st.rerun()
                with col345:
                    if st.button(f"{st.session_state.player_list3[2]}\n{["立直", "Riichi"][lan]}", key = "39"):
                        st.session_state.point_list3[2] -= 1000
                        st.session_state.point_list3[4] += 1000
                        st.session_state.point_history3.append(st.session_state.point_list3.copy())
                        st.rerun()
                col371, col372 = st.columns([2, 9])
                with col372:
                    benchang3 = st.slider(["本场数", "Honba Count"][lan], min_value=0, max_value=15, key = "40")
                with col371:
                    st.text(f"{["立直棒", "Riichi"][lan]}：{st.session_state.point_list3[4]}")
                    st.text(f"{["本场棒", "Honba Stick"][lan]}：{st.session_state.stick3 * benchang3}")
                col351, col352, col353, col354 = st.columns([2, 3, 3, 3])
                with col352:
                    winner3 = st.select_slider(["和牌", "Winner"][lan], options=st.session_state.player_list3,
                                               value=st.session_state.player_list3[0], key = "41")
                with col353:
                    loser_list3 = st.session_state.player_list3.copy()
                    if lan == 0:
                        loser_list3.append("自摸")
                    else:
                        loser_list3.append("Tsumo")
                    loser3 = st.select_slider(["放铳", "Ron Discarder"][lan], options=loser_list3,
                                              value=st.session_state.player_list3[0], key = "42")
                    if loser3 == "Tsumo":
                        loser3 = "自摸"
                with col354:
                    if lan == 0:
                        han_fu_list = ["1番30符", "1番40符", "1番50符", "1番60符", "1番70符", "1番80符", "1番90符",
                                       "1番100符", "1番110符",
                                       "2番20符", "2番25符", "2番30符", "2番40符", "2番50符", "2番60符", "2番70符",
                                       "2番80符", "2番90符", "2番100符", "2番110符",
                                       "3番20符", "3番25符", "3番30符", "3番40符", "3番50符", "3番60符", "4番20符",
                                       "4番25符", "4番30符", "满贯", "跳满", "倍满",
                                       "三倍满", "累计役满", "役满", "双倍役满", "三倍役满", "四倍役满", "五倍役满",
                                       "六倍役满"]
                    else:
                        han_fu_list = ["1 Han 30 Fu", "1 Han 40 Fu", "1 Han 50 Fu", "1 Han 60 Fu", "1 Han 70 Fu",
                                       "1 Han 80 Fu", "1 Han 90 Fu", "1 Han 100 Fu", "1 Han 110 Fu",
                                       "2 Han 20 Fu", "2 Han 25 Fu", "2 Han 30 Fu", "2 Han 40 Fu", "2 Han 50 Fu",
                                       "2 Han 60 Fu", "2 Han 70 Fu", "2 Han 80 Fu", "2 Han 90 Fu", "2 Han 100 Fu",
                                       "2 Han 110 Fu",
                                       "3 Han 20 Fu", "3 Han 25 Fu", "3 Han 30 Fu", "3 Han 40 Fu", "3 Han 50 Fu",
                                       "3 Han 60 Fu",
                                       "4 Han 20 Fu", "4 Han 25 Fu", "4 Han 30 Fu",
                                       "Mangan", "Haneman", "Baiman", "Sanbaiman", "Kazoe Yakuman", "Yakuman",
                                       "Double Yakuman", "Triple Yakuman", "Quadruple Yakuman", "Quintuple Yakuman",
                                       "Sextuple Yakuman"]
                    han_fu_tran = {"1 Han 30 Fu": "1番30符", "1 Han 40 Fu": "1番40符", "1 Han 50 Fu": "1番50符",
                                   "1 Han 60 Fu": "1番60符", "1 Han 70 Fu": "1番70符", "1 Han 80 Fu": "1番80符",
                                   "1 Han 90 Fu": "1番90符", "1 Han 100 Fu": "1番100符", "1 Han 110 Fu": "1番110符",
                                   "2 Han 20 Fu": "2番20符", "2 Han 25 Fu": "2番25符", "2 Han 30 Fu": "2番30符",
                                   "2 Han 40 Fu": "2番40符", "2 Han 50 Fu": "2番50符", "2 Han 60 Fu": "2番60符",
                                   "2 Han 70 Fu": "2番70符", "2 Han 80 Fu": "2番80符", "2 Han 90 Fu": "2番90符",
                                   "2 Han 100 Fu": "2番100符", "2 Han 110 Fu": "2番110符", "3 Han 20 Fu": "3番20符",
                                   "3 Han 25 Fu": "3番25符", "3 Han 30 Fu": "3番30符", "3 Han 40 Fu": "3番40符",
                                   "3 Han 50 Fu": "3番50符", "3 Han 60 Fu": "3番60符", "4 Han 20 Fu": "4番20符",
                                   "4 Han 25 Fu": "4番25符", "4 Han 30 Fu": "4番30符", "Mangan": "满贯",
                                   "Haneman": "跳满", "Baiman": "倍满", "Sanbaiman": "三倍满",
                                   "Kazoe Yakuman": "累计役满", "Yakuman": "役满", "Double Yakuman": "双倍役满",
                                   "Triple Yakuman": "三倍役满", "Quadruple Yakuman": "四倍役满",
                                   "Quintuple Yakuman": "五倍役满",
                                   "Sextuple Yakuman": "六倍役满"}
                    win_han3 = st.selectbox(["番数/符数", "Han/Fu"][lan], options=han_fu_list, key = "44")
                    if lan == 1:
                        win_han3 = han_fu_tran[win_han3]
                with col351:
                    if st.button(["和牌", "Win"][lan], key = "43"):
                        if winner3 != loser3:
                            st.session_state.point_list3[st.session_state.player_list3.index(winner3)] += \
                            st.session_state.point_list3[4]
                            st.session_state.point_list3[4] = 0
                            if winner3 == t_zhuang_3:
                                if loser3 == "自摸":
                                    zm_loser3 = st.session_state.player_list3.copy()
                                    zm_loser3.remove(winner3)
                                    for player in zm_loser3:
                                        st.session_state.point_list3[st.session_state.player_list3.index(player)] -= (
                                                    han_fu_oya_point[win_han3][
                                                        1] + st.session_state.stick3 * benchang3 // 3)
                                    st.session_state.point_list3[st.session_state.player_list3.index(winner3)] += (
                                            han_fu_oya_point[win_han3][1] * 2 + st.session_state.stick3 * benchang3)
                                else:
                                    st.session_state.point_list3[st.session_state.player_list3.index(loser3)] -= (
                                                han_fu_oya_point[win_han3][0] + st.session_state.stick3 * benchang3)
                                    st.session_state.point_list3[st.session_state.player_list3.index(winner3)] += (
                                                han_fu_oya_point[win_han3][0] + st.session_state.stick3 * benchang3)
                            elif winner3 != t_zhuang_3:
                                if loser3 == "自摸":
                                    zm_loser3 = st.session_state.player_list3.copy()
                                    zm_loser3.remove(winner3)
                                    for player in zm_loser3:
                                        if player == t_zhuang_3:
                                            st.session_state.point_list3[
                                                st.session_state.player_list3.index(player)] -= (
                                                        han_fu_co_point[win_han3][
                                                            2] + st.session_state.stick3 * benchang3 // 3)
                                        else:
                                            st.session_state.point_list3[
                                                st.session_state.player_list3.index(player)] -= (
                                                        han_fu_co_point[win_han3][
                                                            1] + st.session_state.stick3 * benchang3 // 3)
                                    st.session_state.point_list3[st.session_state.player_list3.index(winner3)] += (
                                            han_fu_co_point[win_han3][1] + han_fu_co_point[win_han3][2] + st.session_state.stick3 * benchang3)
                                else:
                                    st.session_state.point_list3[st.session_state.player_list3.index(loser3)] -= (
                                                han_fu_co_point[win_han3][0] + st.session_state.stick3 * benchang3)
                                    st.session_state.point_list3[st.session_state.player_list3.index(winner3)] += (
                                                han_fu_co_point[win_han3][0] + st.session_state.stick3 * benchang3)
                            st.session_state.point_history3.append(st.session_state.point_list3.copy())
                            st.rerun()
                        else:
                            error_message_3 = ["不能荣和自己啊", "You Can't Ron Yourself!!!"][lan]
                col361, col362 = st.columns([2, 9])
                with col362:
                    tin_le3 = st.multiselect(["听牌", "Tenpai"][lan], options=st.session_state.player_list3, key = "45")
                with col361:
                    if st.button(["荒牌流局", "Draw"][lan], key = "46"):
                        if len(tin_le3) != 3:
                            for player in st.session_state.player_list3:
                                if player in tin_le3:
                                    if len(tin_le3) == 2:
                                        st.session_state.point_list3[st.session_state.player_list3.index(player)] += st.session_state.notin3
                                    elif len(tin_le3) == 1:
                                        st.session_state.point_list3[st.session_state.player_list3.index(player)] += st.session_state.notin3 * 2
                                else:
                                    if len(tin_le3) == 2:
                                        st.session_state.point_list3[st.session_state.player_list3.index(player)] -= st.session_state.notin3 * 2
                                    elif len(tin_le3) == 1:
                                        st.session_state.point_list3[st.session_state.player_list3.index(player)] -= st.session_state.notin3
                        st.session_state.point_history3.append(st.session_state.point_list3.copy())
                        st.rerun()
                col391, col392, col393 = st.columns([2, 3, 3])
                if "tz3" not in st.session_state:
                    st.session_state.tz3 = [1, 1]
                with col391:
                    if st.button(["抛🎲", "Roll 🎲"][lan], key = "49"):
                        st.session_state.tz3 = [random.randint(1, 6), random.randint(1, 6)]
                with col392:
                    st.markdown(f"<h2 style='text-align: center;'>[{st.session_state.tz3[0]}]</h2>",
                                unsafe_allow_html=True)
                with col393:
                    st.markdown(f"<h2 style='text-align: center;'>[{st.session_state.tz3[1]}]</h2>",
                                unsafe_allow_html=True)
                col381, col383, col382 = st.columns([1,3,1])
                with col381:
                    if st.button(["撤回操作", "Undo"][lan], key = "47"):
                        if len(st.session_state.point_history3) > 1:
                            st.session_state.point_history3.pop()
                            st.session_state.point_list3 = st.session_state.point_history3[-1].copy()
                            #print(st.session_state.point_history3)
                            #print(st.session_state.point_history3[-1])
                            st.rerun()
                        else:
                            error_message = ["没东西可以撤回了", "There Is Nothing To Undo!!!"][lan]
                with col382:
                    if st.button(["结束对局", "End The Game"][lan], key = "48"):
                        st.session_state.start3 = False
                        st.session_state.point_history3 = []
                        st.rerun()
                @st.dialog(["手动修改", "Manual Edit Point"][lan])
                def edit_3m():
                    edit0 = st.number_input(st.session_state.player_list3[0], value=st.session_state.point_list3[0])
                    edit1 = st.number_input(st.session_state.player_list3[1], value=st.session_state.point_list3[1])
                    edit2 = st.number_input(st.session_state.player_list3[2], value=st.session_state.point_list3[2])
                    if st.button(["修改", "Edit"][lan]):
                        st.session_state.point_list3 = [edit0, edit1, edit2, st.session_state.point_list3[3], st.session_state.point_list3[4]]
                        st.session_state.point_history3.append(st.session_state.point_list3.copy())
                        st.rerun()
                with col383:
                    if st.button(["手动修改", "Manual Edit Point"][lan], key="a1"):
                        edit_3m()
                if error_message_3:
                    st.error(error_message_3)
                    error_message_3 = ""
        else:
            with trackermode2:
                st.text("")
                st.text("")
                st.text("")
                st.text(["(添加3个玩家以开始)","(Insert 3 Players to Continue)"][lan])
if page == 5:
    form_url = "https://docs.google.com/forms/d/e/1FAIpQLSe4clzw2E6KzdOirVOOGV6mSTG0S_XC9KdmKhb4QnnOwohUKg/viewform?usp=dialog"
    st.markdown(f'<a href="{form_url}" target="_blank">{["提交反馈","Report Issues Or Give Feedback"][lan]}</a>',
                unsafe_allow_html=True)
    form_url2 = "https://docs.google.com/forms/d/e/1FAIpQLSdntZn5kiay5h0rfp5rAHmw5yixLWebDewznqtiONY5SqJ_pA/viewform?usp=dialog"
    st.markdown(f'<a href="{form_url2}" target="_blank">{["满意度调查","Satisfaction Survey"][lan]}</a>',
                unsafe_allow_html=True)
if page == 3:
    TENPAI_ALL_TILE = ["1m","2m","3m","4m","5m","6m","7m","8m","9m",
                    "1s","2s","3s","4s","5s","6s","7s","8s","9s",
                    "1p","2p","3p","4p","5p","6p","7p","8p","9p",
                    "1z","2z","3z","4z","5z","6z","7z"]
    st.title(["听牌计算机","Tenpai Calculator"][lan])
    tenpai_hand = ful_hand(st.text_input(["手牌","Hand"][lan],key="t3").lower().replace(" ",""))
    col123, col124 = st.columns(2)
    with col123:
        tenpai_fanfu = st.toggle(["番符计算（需要输入更多信息）","Han, Fu Caculation (More Information Are Needed)"][lan])
    if tenpai_fanfu:
        t4c1, t4c2, t4c3, t4c4 = st.columns(4)
        with t4c1:
            tenpai_meld1 = ful_hand(st.text_input(["副露1","Meld1"][lan],key="t4").lower().replace(" ",""))
        with t4c2:
            tenpai_meld2 = ful_hand(st.text_input(["副露2","Meld2"][lan],key="t5").lower().replace(" ", ""))
        with t4c3:
            tenpai_meld3 = ful_hand(st.text_input(["副露3","Meld3"][lan],key="t6").lower().replace(" ", ""))
        with t4c4:
            tenpai_meld4 = ful_hand(st.text_input(["副露4","Meld4"][lan],key="t7").lower().replace(" ", ""))
        t4c5, t4c6 = st.columns(2)
        with t4c5:
            tenpai_riichi = st.selectbox(["立直情况","Riichi"][lan], [["没立直", "立直", "双立直"],["No Riichi","Riichi","Double Riichi"]][lan])
            if lan == 1:
                tenpai_riichi = {"No Riichi":"没立直","Riichi":"立直","Double Riichi":"双立直"}[tenpai_riichi]
            tenpai_wind1 = st.selectbox(["场风","Round Wind"][lan], [["东", "南", "西", "北"],["East","South","West","North"]][lan], key="t1")
            if lan == 1:
                tenpai_wind1 = {"East": "东", "South": "南", "West": "西", "North": "北"}[tenpai_wind1]
        with t4c6:
            tenpai_dora = st.text_input(["宝牌指示牌","Dora Indicator"][lan],key="t8")
            tenpai_wind2 = st.selectbox(["自风","Seat Wind"][lan], [["东", "南", "西", "北"],["East","South","West","North"]][lan], key="t2")
            if lan == 1:
                tenpai_wind2 = {"East": "东", "South": "南", "West": "西", "North": "北"}[tenpai_wind2]
        tenpai_double_yakuman = st.checkbox(["国士无双十三面，纯正九莲宝灯，四暗刻单骑，大四喜是双倍役满","Kokushi Muso Juusanmen, Junsei Churen Poto, Suu Ankou Tanki, Dai Suushi are double yakuman"][lan],value=True,key="t9")
    with col124:
        tenpai_ignore = st.toggle(["忽视已拿4张的听牌","Ignoring Tenpai With 4 Tiles Already Had"][lan], value=True)

    def w_cal_han(w_cal_ipt,w_ipt11,fast):
        ALL_WW_TILE = ["1m", "2m", "3m", "4m", "5m", "6m", "7m", "8m", "9m",
                      "1s", "2s", "3s", "4s", "5s", "6s", "7s", "8s", "9s",
                      "1p", "2p", "3p", "4p", "5p", "6p", "7p", "8p", "9p",
                      "1z", "2z", "3z", "4z", "5z", "6z", "7z"]
        w_cal_ipt.replace("w", "")
        w_w_han_list = []
        for w_tile in ALL_WW_TILE:
            w_cal_han_result = cal_han(w_tile + w_cal_ipt, w_ipt11, lan, False, 1)[1]
            w_w_han_list.append(w_cal_han_result)
            if fast and w_cal_han_result != -1:
               return [True,1]
        w_max_index = w_w_han_list.index(max(w_w_han_list))
        w_cal_ipt = ALL_WW_TILE[w_max_index] + w_cal_ipt
        if max(w_w_han_list) != -1:
            return cal_han(w_cal_ipt, w_ipt11, lan, False, 1)
        else:
            return [False, -1]
    if st.button(["计算","Calculate"][lan]):
        dora_list = {"1s": "2s", "2s": "3s", "3s": "4s", "4s": "5s", "5s": "6s", "0s": "6s", "6s": "7s", "7s": "8s",
                "8s": "9s", "9s": "1s",
                "1p": "2p", "2p": "3p", "3p": "4p", "4p": "5p", "5p": "6p", "0p": "6p", "6p": "7p", "7p": "8p",
                "8p": "9p", "9p": "1p",
                "1m": "2m", "2m": "3m", "3m": "4m", "4m": "5m", "5m": "6m", "0m": "6m", "6m": "7m", "7m": "8m",
                "8m": "9m", "9m": "1m",
                "1z": "2z", "2z": "3z", "3z": "4z", "4z": "1z", "5z": "6z", "6z": "7z", "7z": "5z", "8z": "8z"}
        if tenpai_fanfu == False:
            try:
            #if True:
                if "w" in tenpai_hand:
                    if len(re.findall(r"[0-9][mpsz]", tenpai_hand)) == 0:
                        tenpai_meld = "1s1s1s.1s1s1s.1s1s1s.1s1s1s"
                    elif len(re.findall(r"[0-9][mpsz]", tenpai_hand)) == 3:
                        tenpai_meld = "1s1s1s.1s1s1s.1s1s1s"
                    elif len(re.findall(r"[0-9][mpsz]", tenpai_hand)) == 6:
                        tenpai_meld = "1s1s1s.1s1s1s"
                    elif len(re.findall(r"[0-9][mpsz]", tenpai_hand)) == 9:
                        tenpai_meld = "1s1s1s"
                    elif len(re.findall(r"[0-9][mpsz]", tenpai_hand)) == 12:
                        tenpai_meld = ""
                    else:
                        raise Exception
                    w_tenpai_count = False
                    ten_all_w = []
                    for tile in TENPAI_ALL_TILE:
                        w_tenpai_input = f"{tenpai_hand}{tile},{tenpai_meld},00000,,1z1z"
                        if w_cal_han(w_tenpai_input, True, True)[1] != -1:
                            if re.findall(r"[0-9][mpsz]", tenpai_hand).count(tile) >= 4:
                                if tenpai_ignore:
                                    ten_all_w.append(False)
                                else:
                                    ten_all_w.append(tile + ["(已拿四张)"," (Had 4 Already)"][lan])
                                    w_tenpai_count = True
                            else:
                                ten_all_w.append(tile)
                                w_tenpai_count = True
                    if len(ten_all_w) == 34:
                        st.success(["听全部","All Tiles"][lan])
                    else:
                        for tile in ten_all_w:
                            if tile:
                                if tile[-1] == ")":
                                    st.error(tile)
                                else:
                                    st.success(tile)
                    if w_tenpai_count == False:
                        st.error(["没听", "Noten"][lan])
                else:
                    if len(re.findall(r"[0-9][mpsz]", tenpai_hand)) == 1:
                        tenpai_meld = "1s1s1s.1s1s1s.1s1s1s.1s1s1s"
                    elif len(re.findall(r"[0-9][mpsz]", tenpai_hand)) == 4:
                        tenpai_meld = "1s1s1s.1s1s1s.1s1s1s"
                    elif len(re.findall(r"[0-9][mpsz]", tenpai_hand)) == 7:
                        tenpai_meld = "1s1s1s.1s1s1s"
                    elif len(re.findall(r"[0-9][mpsz]", tenpai_hand)) == 10:
                        tenpai_meld = "1s1s1s"
                    elif len(re.findall(r"[0-9][mpsz]", tenpai_hand)) == 13:
                        tenpai_meld = ""
                    else:
                        raise Exception
                    tenpai_count = False
                    for tile in TENPAI_ALL_TILE:
                        tenpai_input = f"{tenpai_hand}{tile},{tenpai_meld},00000,,1z1z"
                        if cal_han(tenpai_input, True, 0, False, 1)[0]:
                            if re.findall(r"[0-9][mpsz]", tenpai_hand).count(tile) >= 4:
                                if tenpai_ignore:
                                    pass
                                else:
                                    st.error(tile + ["(已拿四张)"," (Had 4 Already)"][lan])
                                    tenpai_count = True
                            else:
                                st.success(tile)
                                tenpai_count = True
                    if tenpai_count == False:
                        st.error(["没听", "Noten"][lan])
            except Exception:
                st.error(["请检查输入","Please Check Your Input"][lan])
        else:
            try:
            #if True:
                tenpai_check = False
                tenpai_tiles_hand_meld = re.findall(r"[0-9][mpsz]", tenpai_hand)
                if len(tenpai_tiles_hand_meld) == 14:
                    raise Exception
                if len(tenpai_tiles_hand_meld) == 13 and "w" in tenpai_hand:
                    raise Exception
                tenpai_input1 = ","
                for tenpai_meld in [tenpai_meld1, tenpai_meld2, tenpai_meld3, tenpai_meld4]:
                    if tenpai_meld:
                        tenpai_input1 += tenpai_meld + "."
                    for tile in re.findall(r"[0-9][mpsz]", tenpai_meld):
                        tenpai_tiles_hand_meld.append(tile)
                while tenpai_input1[-1] == ".":
                    tenpai_input1 = tenpai_input1[:-1]
                tenpai_input1 += ","
                if tenpai_riichi == "没立直":
                    tenpai_input2 = "0000,"
                elif tenpai_riichi == "立直":
                    tenpai_input2 = "1000,"
                elif tenpai_riichi == "双立直":
                    tenpai_input2 = "2000,"
                for tile in re.findall(r"[0-9][mpsz]", tenpai_dora):
                    tenpai_input2 += dora_list[tile]
                tenpai_input2 += ","
                for tenpai_wind in [tenpai_wind1, tenpai_wind2]:
                    tenpai_input2 += {"东": "1z", "南": "2z", "西": "3z", "北": "4z"}[tenpai_wind]
                for tile in TENPAI_ALL_TILE:
                    tenpai_st_output = f"{tile} "
                    for tenpai_tr in ["0", "1"]:
                        tenpai_input3 = tenpai_hand + tile + tenpai_input1 + tenpai_tr + tenpai_input2
                        if "w" in tenpai_hand:
                            tenpai_cal_han_output = w_cal_han(tenpai_input3, tenpai_double_yakuman, False)[0]
                        else:
                            tenpai_cal_han_output = cal_han(tenpai_input3, tenpai_double_yakuman, lan, False, 1)[0]
                        if tenpai_cal_han_output:
                            if tenpai_tr == "0":
                                tenpai_st_output += f"( {["荣", "Ron"][lan]}: {tenpai_cal_han_output} / "
                            elif tenpai_tr == "1":
                                tenpai_st_output += f"{["自摸", "Tsumo"][lan]}: {tenpai_cal_han_output} )"
                    if tenpai_st_output[-1] == ")":
                        if tenpai_tiles_hand_meld.count(tile) >= 4:
                            if tenpai_ignore:
                                pass
                            else:
                                tenpai_st_output += [" (已拿四张)", " ( Had 4 Already )"][lan]
                                st.error(tenpai_st_output)
                                tenpai_check = True
                        else:
                            if tenpai_st_output.count("役满") or tenpai_st_output.count("Yakuman"):
                                st.info(tenpai_st_output)
                            elif tenpai_st_output.count("无役") == 1 or tenpai_st_output.count("No Yaku") == 1:
                                st.warning(tenpai_st_output)
                            elif tenpai_st_output.count("无役") == 2 or tenpai_st_output.count("No Yaku") == 2:
                                st.error(tenpai_st_output)
                            else:
                                st.success(tenpai_st_output)
                            tenpai_check = True
                if not tenpai_check:
                    st.error(["没听", "Noten"][lan])
            except Exception:
                st.error(["请检查输入", "Please Check Your Input"][lan])

if page == 4:
    QING_ALL_TILE = ["1s", "2s", "3s", "4s", "5s", "6s", "7s", "8s", "9s",
                     "1s", "2s", "3s", "4s", "5s", "6s", "7s", "8s", "9s",
                     "1s", "2s", "3s", "4s", "5s", "6s", "7s", "8s", "9s",
                     "1s", "2s", "3s", "4s", "5s", "6s", "7s", "8s", "9s"]
    qcol1, qcol2 = st.columns([2, 1])
    with qcol1:
        minimum_tenpai = st.slider(["最小听牌数", "Minimum Tenpai Number"][lan], min_value=1, max_value=9)
    with qcol2:
        qing_type = st.selectbox(["数牌类型", "Type"][lan],
                                 [["饼子", "索子", "万字"], ["Pinzu", "Souzu", "Manzu"]][lan], index=1)
    if qing_type == "饼子" or qing_type == "Pinzu":
        qing_type = "p"
    elif qing_type == "索子" or qing_type == "Souzu":
        qing_type = "s"
    elif qing_type == "万字" or qing_type == "Manzu":
        qing_type = "m"
    if st.button(["生成新的 (最小听牌数越多生成耗时越久，请耐心等待(屎山代码发力了))", "Generate A New Hand (Might Take A While If Minimum Tenpai Number Is High)"][lan]):
        while True:
            random.shuffle(QING_ALL_TILE)
            qing_hand = sorted(QING_ALL_TILE[0:13])
            qing_ten = []
            for tile in ["1s", "2s", "3s", "4s", "5s", "6s", "7s", "8s", "9s"]:
                cal_han_input_qing = f"{"".join(qing_hand)}{tile},,00000,,1z1z"
                if cal_han(cal_han_input_qing, True, 0, False, 1)[0]:
                    if qing_hand.count(tile) != 4:
                        qing_ten.append(tile)
            if len(qing_ten) >= minimum_tenpai:
                break
        til1, til2, til3, til4, til5, til6, til7, til8, til9, til10, til11, til12, til13 = st.columns(13)
        with til1:
            st.image(f"mahjong19s/{qing_hand[0][0]}{qing_type}.png", width=300)
        with til2:
            st.image(f"mahjong19s/{qing_hand[1][0]}{qing_type}.png", width=300)
        with til3:
            st.image(f"mahjong19s/{qing_hand[2][0]}{qing_type}.png", width=300)
        with til4:
            st.image(f"mahjong19s/{qing_hand[3][0]}{qing_type}.png", width=300)
        with til5:
            st.image(f"mahjong19s/{qing_hand[4][0]}{qing_type}.png", width=300)
        with til6:
            st.image(f"mahjong19s/{qing_hand[5][0]}{qing_type}.png", width=300)
        with til7:
            st.image(f"mahjong19s/{qing_hand[6][0]}{qing_type}.png", width=300)
        with til8:
            st.image(f"mahjong19s/{qing_hand[7][0]}{qing_type}.png", width=300)
        with til9:
            st.image(f"mahjong19s/{qing_hand[8][0]}{qing_type}.png", width=300)
        with til10:
            st.image(f"mahjong19s/{qing_hand[9][0]}{qing_type}.png", width=300)
        with til11:
            st.image(f"mahjong19s/{qing_hand[10][0]}{qing_type}.png", width=300)
        with til12:
            st.image(f"mahjong19s/{qing_hand[11][0]}{qing_type}.png", width=300)
        with til13:
            st.image(f"mahjong19s/{qing_hand[12][0]}{qing_type}.png", width=300)
        with st.expander(["听牌", "Tenpai"][lan]):
            ttil1, ttil2, ttil3, ttil4, ttil5, ttil6, ttil7, ttil8, ttil9 = st.columns(9)
            with ttil1:
                if len(qing_ten) >= 1:
                    st.image(f"mahjong19s/{qing_ten[0][0]}{qing_type}.png", width=50)
            with ttil2:
                if len(qing_ten) >= 2:
                    st.image(f"mahjong19s/{qing_ten[1][0]}{qing_type}.png", width=50)
            with ttil3:
                if len(qing_ten) >= 3:
                    st.image(f"mahjong19s/{qing_ten[2][0]}{qing_type}.png", width=50)
            with ttil4:
                if len(qing_ten) >= 4:
                    st.image(f"mahjong19s/{qing_ten[3][0]}{qing_type}.png", width=50)
            with ttil5:
                if len(qing_ten) >= 5:
                    st.image(f"mahjong19s/{qing_ten[4][0]}{qing_type}.png", width=50)
            with ttil6:
                if len(qing_ten) >= 6:
                    st.image(f"mahjong19s/{qing_ten[5][0]}{qing_type}.png", width=50)
            with ttil7:
                if len(qing_ten) >= 7:
                    st.image(f"mahjong19s/{qing_ten[6][0]}{qing_type}.png", width=50)
            with ttil8:
                if len(qing_ten) >= 8:
                    st.image(f"mahjong19s/{qing_ten[7][0]}{qing_type}.png", width=50)
            with ttil9:
                if len(qing_ten) >= 9:
                    st.image(f"mahjong19s/{qing_ten[8][0]}{qing_type}.png", width=50)