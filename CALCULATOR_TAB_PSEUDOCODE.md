# Mahjong Point Calculator Tab - Pseudocode

## Overview
This pseudocode describes the logic flow for the Point Calculator tab (tab1) of the Riichi Mahjong Calculator application.

---

## Main Tab Structure

```
TAB1: Point Calculator
│
├── Display Title (bilingual: Chinese/English based on language selection)
│
├── INPUT SECTION
│   ├── Hand Input (ipt1)
│   │   └── Text input for hand tiles (winning tile goes last)
│   │       └── Process through ful_hand() function to normalize format
│   │
│   ├── Meld Inputs (ipt2, ipt3, ipt4, ipt5)
│   │   └── Four separate text inputs for open melds
│   │       └── Each processed through ful_hand() function
│   │
│   ├── Help Expander
│   │   ├── Display tile notation image
│   │   └── Show instructions for:
│   │       ├── Shorthand notation (e.g., 123m instead of 1m2m3m)
│   │       └── Closed kan notation (add 'a' at end)
│   │
│   ├── Win Type Selection (ipt6)
│   │   └── Dropdown: Tsumo (self-draw) or Ron (discard)
│   │       └── Convert English to Chinese if needed
│   │
│   ├── Winning Conditions (ipt7)
│   │   └── Multi-select for special conditions:
│   │       ├── Riichi (立直)
│   │       ├── Double Riichi (双立直)
│   │       ├── Ippatsu (一发)
│   │       ├── Chankan (枪杠)
│   │       ├── Rinshan Kaiho (岭上开花)
│   │       ├── Tenho (天和)
│   │       ├── Chiho (地和)
│   │       └── Haitei (海底)
│   │       └── Translate from English to Chinese if language is English
│   │
│   ├── Dora Indicators (ipt8)
│   │   └── Text input for dora indicator tiles
│   │       └── Include ura-dora if riichi was declared
│   │
│   ├── Kita Dora (ipt12)
│   │   └── Slider (0-4) for north tile dora in sanma
│   │
│   ├── Round Wind (ipt9)
│   │   └── Dropdown: East, South, West, North
│   │       └── Translate to Chinese if needed
│   │
│   ├── Seat Wind (ipt10)
│   │   └── Dropdown: East, South, West, North
│   │       └── Translate to Chinese if needed
│   │
│   └── Double Yakuman Option (ipt11)
│       └── Checkbox for treating certain hands as double yakuman
│           └── Default: True
│
└── CALCULATION SECTION (wrapped in try-except)
    │
    ├── Build Calculation Input String (cal_ipt)
    │   │
    │   ├── Step 1: Add hand tiles
    │   │   └── cal_ipt = ipt1 + ","
    │   │
    │   ├── Step 2: Add melds (separated by dots)
    │   │   ├── IF ipt2 exists: add ipt2 + "."
    │   │   ├── IF ipt3 exists: add ipt3 + "."
    │   │   ├── IF ipt4 exists: add ipt4 + "."
    │   │   ├── IF ipt5 exists: add ipt5 + "."
    │   │   └── Remove trailing dots
    │   │   └── Add ","
    │   │
    │   ├── Step 3: Encode win type
    │   │   ├── IF ipt6 == "自摸": add "1"
    │   │   └── ELSE: add "0"
    │   │
    │   ├── Step 4: Encode riichi status
    │   │   ├── IF "双立直" in ipt7: add "2"
    │   │   ├── ELSE IF "立直" in ipt7: add "1"
    │   │   └── ELSE: add "0"
    │   │
    │   ├── Step 5: Encode ippatsu
    │   │   ├── IF "一发" in ipt7: add "1"
    │   │   └── ELSE: add "0"
    │   │
    │   ├── Step 6: Encode special win conditions
    │   │   ├── IF "枪杠" in ipt7: add "1"
    │   │   ├── ELSE IF "岭上开花" in ipt7: add "2"
    │   │   └── ELSE: add "0"
    │   │
    │   ├── Step 7: Encode special timing
    │   │   ├── IF "天和" in ipt7: add "1,"
    │   │   ├── ELSE IF "地和" in ipt7: add "2,"
    │   │   ├── ELSE IF "海底" in ipt7: add "3,"
    │   │   └── ELSE: add "0,"
    │   │
    │   ├── Step 8: Convert dora indicators to actual dora
    │   │   ├── Define dora_list mapping (indicator -> dora)
    │   │   │   └── Examples: "1s" -> "2s", "9s" -> "1s", "4z" -> "1z"
    │   │   ├── Extract all tiles from ipt8 using regex
    │   │   ├── FOR each indicator tile:
    │   │   │   └── Add corresponding dora to cal_ipt
    │   │   └── Add kita dora: append "8z" * ipt12 times
    │   │   └── Add ","
    │   │
    │   └── Step 9: Add wind information
    │       ├── Convert round wind to tile notation
    │       │   └── 东->1z, 南->2z, 西->3z, 北->4z
    │       └── Convert seat wind to tile notation
    │           └── 东->1z, 南->2z, 西->3z, 北->4z
    │
    ├── Handle Wild Card (if 'w' in hand)
    │   │
    │   ├── IF "w" NOT in ipt1:
    │   │   └── Call cal_han(cal_ipt, ipt11, lan, True)
    │   │       └── Display results directly
    │   │
    │   └── ELSE (wild card present):
    │       ├── Define ALL_W_TILE list (all 34 tile types)
    │       ├── Remove "w" from cal_ipt
    │       ├── Initialize w_han_list = []
    │       │
    │       ├── FOR each tile in ALL_W_TILE:
    │       │   ├── Test_input = tile + cal_ipt
    │       │   ├── Calculate han value: cal_han(test_input, ipt11, lan, False)
    │       │   └── Append result[1] to w_han_list
    │       │
    │       ├── Find maximum han value index
    │       ├── Set wild card to best tile: ALL_W_TILE[w_max_index]
    │       ├── Update cal_ipt = best_tile + cal_ipt
    │       │
    │       ├── IF max(w_han_list) != -1:
    │       │   └── Display: "Wild Card Is {best_tile}"
    │       │
    │       └── Call cal_han(cal_ipt, ipt11, lan, True)
    │           └── Display final results
    │
    └── EXCEPTION HANDLING
        └── Display error message:
            └── "Results are generated automatically. If nothing appears, please double-check your input"
```

---

## Helper Functions Used

### 1. ful_hand(hand_input)
```
PURPOSE: Normalize hand input by adding suit letters to each number

ALGORITHM:
    Initialize new_hand_ipt = ""
    Initialize hand_letter_index = []
    
    FOR each letter in hand_input:
        IF letter in ["m", "p", "s", "z"]:
            Append letter to hand_letter_index
        ELSE:
            Append "" to hand_letter_index
    
    FOR each letter at index in hand_input:
        IF letter == "a" OR letter == "w":
            Append letter to new_hand_ipt
        ELSE IF letter NOT in ["m", "p", "s", "z"] AND next_letter NOT in ["m", "p", "s", "z"]:
            Append letter to new_hand_ipt
            Find next suit letter in hand_letter_index after current index
            Append that suit letter to new_hand_ipt
        ELSE:
            Append letter to new_hand_ipt
    
    RETURN new_hand_ipt

EXCEPTION:
    IF any error occurs:
        RETURN ""
```

### 2. cal_han(user_input, double_yakuman, language, output_flag)
```
PURPOSE: Calculate han, fu, and points for a mahjong hand

INPUT FORMAT: "hand,melds,info,dora,winds"
    - hand: tile notation (e.g., "1m2m3m4m5m6m7m8m9m1s1s1s1s")
    - melds: open melds separated by dots (e.g., "1m1m1m.2s2s2s")
    - info: 5-digit code
        [0]: 0=Ron, 1=Tsumo
        [1]: 0=No riichi, 1=Riichi, 2=Double riichi
        [2]: 0=No ippatsu, 1=Ippatsu
        [3]: 0=Normal, 1=Chankan, 2=Rinshan
        [4]: 0=Normal, 1=Tenho, 2=Chiho, 3=Haitei
    - dora: actual dora tiles (e.g., "2s3m")
    - winds: round wind + seat wind (e.g., "1z1z")

RETURN: [title_string, han_value]
    - title_string: Display string (e.g., "3番40符" or "役満")
    - han_value: Numeric han value (-1 if invalid, 100+ for yakuman)

MAIN LOGIC:
    1. Parse input string into components
    2. Validate hand structure
    3. Check for yakuman patterns
    4. IF yakuman found:
        - Calculate yakuman multiplier
        - Display yakuman name(s)
        - Calculate and display points
        - RETURN yakuman info
    5. ELSE:
        - Calculate regular yaku
        - Calculate fu (minipoints)
        - Determine han total
        - Calculate points based on han/fu
        - Display results
        - RETURN han/fu info
```

---

## Input Format Specification

### Tile Notation
- Numbers: 1-9
- Suits: m (manzu/characters), p (pinzu/circles), s (souzu/bamboo), z (honors)
- Red fives: 0m, 0p, 0s (treated as 5 with dora)
- Wild card: w (will be replaced with optimal tile)
- Closed kan marker: a (appended to 4-tile group)

### Examples
- Hand: "123m456p789s1z1z2z" (13 tiles + 1 winning tile)
- Meld: "1m1m1m" (pon/triple)
- Meld: "123s" (chi/sequence)
- Meld: "5p5p5p5p" (open kan)
- Meld: "5p5p5p5pa" (closed kan)

### Shorthand
- "123m" = "1m2m3m"
- "111z" = "1z1z1z"
- "1234m" = "1m2m3m4m"

---

## Calculation Flow

```
INPUT VALIDATION
    ├── Check hand has correct number of tiles (1, 4, 7, 10, or 13)
    ├── Check melds are valid (3 or 4 tiles each)
    └── Check total tiles = 14 (or 17/18 with kans)

HAND ANALYSIS
    ├── Identify possible pairs (jantou/head)
    ├── Identify possible melds (mentsu)
    │   ├── Sequences (shuntsu): 123, 234, etc.
    │   └── Triples (koutsu): 111, 222, etc.
    ├── Generate all valid hand combinations
    │   ├── Standard: 4 melds + 1 pair
    │   ├── Chiitoitsu: 7 pairs
    │   └── Kokushi: 13 terminals/honors + 1 pair
    └── Filter invalid combinations

YAKUMAN CHECK (highest priority)
    ├── Tenho/Chiho (heavenly/earthly hand)
    ├── Kokushi Musou (13 orphans)
    ├── Suuankou (4 concealed triples)
    ├── Daisangen (big three dragons)
    ├── Shousuushii/Daisuushii (little/big four winds)
    ├── Tsuuiisou (all honors)
    ├── Ryuuiisou (all green)
    ├── Chinroutou (all terminals)
    ├── Chuuren Poutou (nine gates)
    └── Suukantsu (4 kans)

IF yakuman found:
    CALCULATE points
    DISPLAY results
    RETURN

REGULAR YAKU CHECK
    ├── 1 Han Yaku
    │   ├── Riichi
    │   ├── Menzen Tsumo
    │   ├── Tanyao (all simples)
    │   ├── Yakuhai (value tiles)
    │   ├── Pinfu (all sequences)
    │   ├── Iipeikou (pure double sequence)
    │   ├── Ippatsu (one-shot)
    │   ├── Rinshan Kaihou (after kan)
    │   ├── Chankan (robbing kan)
    │   └── Haitei/Houtei (last tile)
    │
    ├── 2 Han Yaku
    │   ├── Double Riichi
    │   ├── Chiitoitsu (seven pairs)
    │   ├── Sanshoku Doujun (mixed triple sequence)
    │   ├── Ittsu (pure straight)
    │   ├── Toitoi (all triples)
    │   ├── Sanankou (3 concealed triples)
    │   ├── Sankantsu (3 kans)
    │   ├── Chanta (terminals/honors in all sets)
    │   ├── Honroutou (all terminals/honors)
    │   ├── Shousangen (little three dragons)
    │   └── Sanshoku Doukou (triple triples)
    │
    ├── 3 Han Yaku
    │   ├── Ryanpeikou (twice pure double sequence)
    │   ├── Junchan (terminals in all sets)
    │   └── Honitsu (half flush)
    │
    └── 6 Han Yaku
        └── Chinitsu (full flush)

ADD DORA
    ├── Count dora tiles in hand
    ├── Count red dora (if any)
    ├── Count ura-dora (if riichi)
    └── Count kita dora (if sanma)

CALCULATE FU (if han < 5)
    ├── Base: 20 fu
    ├── Add for closed hand ron: +10 fu
    ├── Add for tsumo (non-pinfu): +2 fu
    ├── Add for pair:
    │   ├── Dragons: +2 fu
    │   ├── Seat wind: +2 fu
    │   └── Round wind: +2 fu
    ├── Add for melds:
    │   ├── Concealed sequence: 0 fu
    │   ├── Open sequence: 0 fu
    │   ├── Concealed simple triple: 4 fu
    │   ├── Open simple triple: 2 fu
    │   ├── Concealed terminal/honor triple: 8 fu
    │   ├── Open terminal/honor triple: 4 fu
    │   ├── Concealed simple kan: 16 fu
    │   ├── Open simple kan: 8 fu
    │   ├── Concealed terminal/honor kan: 32 fu
    │   └── Open terminal/honor kan: 16 fu
    ├── Add for wait:
    │   ├── Edge wait: +2 fu
    │   ├── Closed wait: +2 fu
    │   └── Single wait: +2 fu
    └── Round up to nearest 10

DETERMINE LIMIT HAND
    ├── IF han >= 13: Kazoe Yakuman
    ├── IF han >= 11: Sanbaiman
    ├── IF han >= 8: Baiman
    ├── IF han >= 6: Haneman
    ├── IF han >= 5: Mangan
    ├── IF han == 4 AND fu >= 40: Mangan
    ├── IF han == 3 AND fu >= 70: Mangan
    └── ELSE: Calculate from han/fu table

CALCULATE POINTS
    ├── IF dealer (oya):
    │   ├── Ron: base_points * 6
    │   └── Tsumo: base_points * 2 (from each)
    └── IF non-dealer (ko):
        ├── Ron: base_points * 4
        └── Tsumo: base_points * 2 (from dealer), base_points * 1 (from others)

DISPLAY RESULTS
    ├── Show hand composition
    ├── List all yaku with han values
    ├── Show total han and fu
    ├── Display point values for dealer and non-dealer
    └── Show fu calculation breakdown (in expander)
```

---

## Error Handling

```
TRY:
    Execute all calculation logic
EXCEPT any exception:
    Display user-friendly error message
    Do not crash application
    Allow user to correct input
```

---

## Output Format

### Successful Calculation
```
Hand Type: [Standard/Chiitoitsu/Kokushi]
Win Method: [Ron/Tsumo] : [winning tile]
Hand: [tile groups]
Melds: [open melds] or (None)

[Yaku Name] [Han Value]
[Yaku Name] [Han Value]
...
[Total Han] [Fu Value or Limit Hand Name]

Dealer: [points] or [points]/[tsumo total]([from each])
Non-Dealer: [points] or [points]/[tsumo total]([from dealer],[from others])

Fu Calculation: [expandable details]
```

### Error Cases
- Invalid hand structure: "Please check your input"
- No yaku: "Where Is Your Han Baby???" (repeated error messages)
- Invalid tiles: Exception caught, show input error message

---

## Special Features

### Wild Card Support
- Input 'w' as a tile
- System tests all 34 possible tiles
- Selects tile that maximizes han value
- Displays which tile was chosen
- Calculates final result with optimal tile

### Bilingual Support
- All labels support Chinese and English
- Automatic translation of input values
- Output in selected language
- Consistent terminology

### Dora Conversion
- Automatic conversion from indicator to actual dora
- Handles wraparound (9->1, 4z->1z)
- Supports red dora (0m/0p/0s)
- Includes ura-dora for riichi hands
- Supports kita dora for sanma (3-player)

---

## Data Structures

### Point Tables
```
han_fu_co_point = {
    "1番30符": (ron_points, tsumo_from_dealer, tsumo_from_non_dealer),
    ...
}

han_fu_oya_point = {
    "1番30符": (ron_points, tsumo_from_each, tsumo_from_each),
    ...
}
```

### Translation Dictionaries
```
eng_yaku = {
    "立直": "Riichi",
    "平和": "Pinfu",
    ...
}

wind_translation = {
    "East": "东",
    "South": "南",
    ...
}
```

---

## End of Pseudocode
