from phBot import *
import QtBind
try:
    import phBotChat
except:
    phBotChat = None
import struct
import time
import binascii
import json
import os
import ctypes
try:
    import winsound
except:
    winsound = None

# ============================================================
# ZERK QUEST
# v0.84 - ZERK 105 MAP
# ============================================================

pName = "ZERK QUEST"
pVersion = "0.84-ZERK105-MAP"

gui = QtBind.init(__name__, pName)

HIDDEN_X = 2000
HIDDEN_Y = 2000
ui_page = "blue"
page_widgets = {
    "blue": [],
    "inventory": [],
    "zerk105": []
}

def register_page_widget(page, widget, x, y):
    if page in page_widgets:
        page_widgets[page].append((widget, x, y))
    return widget

def pLabel(page, text, x, y):
    widget = QtBind.createLabel(gui, text, x, y)
    return register_page_widget(page, widget, x, y)

def pButton(page, callback, text, x, y):
    widget = QtBind.createButton(gui, callback, text, x, y)
    return register_page_widget(page, widget, x, y)

def pCheckBox(page, callback, text, x, y):
    widget = QtBind.createCheckBox(gui, callback, text, x, y)
    return register_page_widget(page, widget, x, y)

def pList(page, x, y, w, h):
    widget = QtBind.createList(gui, x, y, w, h)
    return register_page_widget(page, widget, x, y)

btnTabBlue = QtBind.createButton(gui, "btnShowBlueZerkTab", "Blue Zerk 95", 10, 10)
btnTabInventory = QtBind.createButton(gui, "btnShowInventoryTab", "Inventory Expansion", 125, 10)
btnTabZerk105 = QtBind.createButton(gui, "btnShowZerk105Tab", "Zerk 105", 285, 10)
lblPageTitle = QtBind.createLabel(gui, "Blue Zerk (level 95)", 10, 42)

pLabel("blue", "Status", 10, 70)
lstBlueQuestStatus = pList("blue", 10, 92, 650, 92)

pButton("blue", "btnStartQ1", "QUEST 1", 10, 195)
pButton("blue", "btnStartQ2", "QUEST 2", 110, 195)
pButton("blue", "btnStartQ3", "QUEST 3", 210, 195)
pButton("blue", "btnStartQ4", "QUEST 4", 10, 230)
pButton("blue", "btnStartQ5", "QUEST 5", 110, 230)
pButton("blue", "btnStartQ6", "QUEST 6", 210, 230)
pButton("blue", "btnStartQ7", "QUEST 7", 10, 265)
pButton("blue", "btnStartQ8", "QUEST 8", 110, 265)
pButton("blue", "btnStartSelectedBlue", "START SELECTED", 210, 265)
pButton("blue", "btnStopQ1", "STOP", 360, 230)
pButton("blue", "btnQuestMobOn", "CHECK QUEST MOB", 360, 265)

cbxFindAutomaticPath = pCheckBox("blue", "", "Find automatic path", 10, 305)
QtBind.setChecked(gui, cbxFindAutomaticPath, True)
cbxAutoFixQuestMob = pCheckBox("blue", "", "AutoFix quest mob", 160, 305)
QtBind.setChecked(gui, cbxAutoFixQuestMob, True)
cbxReturnNormal = pCheckBox("blue", "", "Normal return", 310, 305)
cbxReturnSpecial = pCheckBox("blue", "", "Special return", 430, 305)
cbxReturnInstant = pCheckBox("blue", "", "Instant return", 550, 305)
QtBind.setChecked(gui, cbxReturnSpecial, True)
cbxSoundDone = pCheckBox("blue", "", "Beep on complete", 670, 305)
QtBind.setChecked(gui, cbxSoundDone, True)
pLabel("blue", "Blocks: Q1 General/Arena | Q2 Exorcist | Q3 Buddhist Priest | Q4 Spirit Shell | Q5 Hunter | Q6 Manual | Q7 Zerk Manual | Q8 Final", 10, 335)

pLabel("inventory", "Status", 10, 70)
lstInventoryQuestStatus = pList("inventory", 10, 92, 650, 92)
pButton("inventory", "btnStartInvQ1", "QUEST 1", 10, 195)
pButton("inventory", "btnStartInvQ2", "QUEST 2", 110, 195)
pButton("inventory", "btnStartInvQ3", "QUEST 3", 10, 230)
pButton("inventory", "btnStartInvQ4", "QUEST 4", 110, 230)
pButton("inventory", "btnStartSelectedInventory", "START SELECTED", 210, 230)
pButton("inventory", "btnStopQ1", "STOP", 360, 230)
cbxInventoryReverseWind = pCheckBox("inventory", "", "Use Reverse Scroll: Wind Town", 10, 270)
pLabel("inventory", "Training areas: attack radius 25 / pick radius 50. Return uses selected Blue Zerk return checkbox.", 10, 300)

pLabel("zerk105", "Status", 10, 70)
lstZerk105QuestStatus = pList("zerk105", 10, 92, 720, 250)
pButton("zerk105", "btnStartSelectedZerk105", "START SELECTED", 10, 355)
pButton("zerk105", "btnStopQ1", "STOP", 160, 355)
pLabel("zerk105", "Mapped only for now. Temple/boss steps stay manual until the flow is validated.", 10, 390)

ZERK_1_QUESTS = [
    {"order": 1, "id": 346, "npc": "General Sonhyeon", "turnin_npc": "General Sonhyeon", "name": "Army Test 1 (Chinese)", "servername": "QNO_CH_HWAN_1_1", "state": "CURRENT"},
    {"order": 2, "id": 347, "npc": "General Sonhyeon", "turnin_npc": "Exorcist Miaoryeong", "next": "Exorcist Miaoryeong", "name": "Material for medicine (Chinese)", "servername": "QNO_CH_HWAN_1_2", "state": "LOCKED"},
    {"order": 3, "id": 348, "npc": "Exorcist Miaoryeong", "turnin_npc": "Buddhist Priest Jeonghye", "next": "Buddhist Priest Jeonghye", "name": "Stone Beast's Bell (Chinese)", "objective": "Stone Beast's Bell", "servername": "QNO_CH_HWAN_1_3", "post_accept_ok": True, "state": "LOCKED"},
    {"order": 4, "id": 349, "npc": "Buddhist Priest Jeonghye", "turnin_npc": "Exorcist Miaoryeong", "next": "Exorcist Miaoryeong", "name": "Spirit's Shell (Chinese)", "objective": "Old Tombstone Ghost", "servername": "QNO_CH_HWAN_1_3_1", "post_accept_ok": True, "state": "LOCKED"},
    {"order": 5, "id": 350, "npc": "Exorcist Miaoryeong", "turnin_npc": "Hunter Associate Gwakwi", "next": "Hunter Associate Gwakwi", "name": "Miaoryeong's Charm (Chinese)", "servername": "QNO_CH_HWAN_1_4", "post_accept_ok": True, "handin_direct_reward": True, "state": "LOCKED"},
    {"order": 6, "id": 351, "npc": "Hunter Associate Gwakwi", "turnin_npc": "Exorcist Miaoryeong", "next": "Exorcist Miaoryeong", "name": "The Spirit (Chinese)", "servername": "QNO_CH_HWAN_1_4_1", "post_accept_ok": True, "manual_capture": True, "state": "LOCKED"},
    {"order": 7, "id": 352, "npc": "Exorcist Miaoryeong", "turnin_npc": "Exorcist Miaoryeong", "name": "Piece of Spirit (Chinese)", "servername": "QNO_CH_HWAN_1_5", "post_accept_ok": True, "manual_zerk": True, "state": "LOCKED"},
    {"order": 8, "id": 353, "npc": "Exorcist Miaoryeong", "turnin_npc": "General Sonhyeon", "next": "General Sonhyeon", "name": "New Power (Chinese)", "servername": "QNO_CH_HWAN_1_6", "post_accept_ok": True, "state": "LOCKED"},
]

INVENTORY_QUESTS = [
    {"order": 1, "id": 0, "npc": "Grocery Trader Jinjin", "turnin_npc": "Grocery Trader Jinjin", "name": "Inventory Expansion 1 (China)", "servername": "QSP_CH_EXINVENTORY_1", "npc_pos": (25000, 6497.0, 1068.0, 0.0), "mob_area": (24488, 6389.0, 758.0, 0.0), "train_radius": 50.0, "pick_radius": 50.0, "state": "CURRENT"},
    {"order": 2, "id": 0, "npc": "Grocery Trader Yeosun", "turnin_npc": "Grocery Trader Yeosun", "name": "Inventory Expansion 2 (China)", "servername": "QSP_WC_EXINVENTORY_2", "npc_pos": (26265, 3514.0, 1993.0, 0.0), "mob_area": (25754, 3773.0, 1577.0, 0.0), "state": "LOCKED"},
    {"order": 3, "id": 0, "npc": "Jewel Lapidary Mamoje", "turnin_npc": "Jewel Lapidary Mamoje", "name": "Inventory Expansion 3 (Common)", "servername": "QSP_KT_EXINVENTORY_3", "npc_pos": (23431, 86.0, -2.0, 0.0), "mob_area": (23676, -2051.0, 89.0, 0.0), "state": "LOCKED"},
    {"order": 4, "id": 0, "npc": "Towner Anashya", "turnin_npc": "Towner Anashya", "name": "Inventory Expansion 4 (Common)", "servername": "QSP_RM_EXINVENTORY_4", "npc_pos": (23155, -3765.0, -302.0, 0.0), "mob_area": (22895, -4586.0, -385.0, 0.0), "reverse_location": "Wind Town", "state": "LOCKED"},
]

ZERK_105_QUESTS = [
    {"order": 1, "npc": "Governor Senmute", "turnin_npc": "Governor Senmute", "name": "The Suspicious Sacrifice", "servername": "QNO_SD_MA_001", "npc_pos": (23343, -16757.0, -158.0, 0.0), "mob_areas": [{"name": "Uneg", "pos": (22834, -16309.0, -439.0, 0.0)}], "train_radius": 50.0, "pick_radius": 50.0, "state": "CURRENT"},
    {"order": 2, "npc": "Doctor Renenutet", "turnin_npc": "Doctor Renenutet", "name": "The Ceremonial Tool", "servername": "QNO_SD_MA_002", "npc_pos": (23087, -16720.0, -382.0, 0.0), "mob_areas": [{"name": "Sand Raider", "pos": (22324, -15895.0, -876.0, 0.0)}], "train_radius": 50.0, "pick_radius": 50.0, "state": "LOCKED"},
    {"order": 3, "npc": "Finance Officer Maneto", "turnin_npc": "Finance Officer Maneto", "name": "His Protesting Son", "servername": "QNO_SD_MA_003", "npc_pos": (23345, -16448.0, -79.0, 0.0), "state": "LOCKED"},
    {"order": 4, "npc": "Finance Officer Maneto", "turnin_npc": "Finance Officer Maneto", "name": "Stopping the Ceremony", "servername": "QNO_SD_MA_004", "npc_pos": (23345, -16448.0, -79.0, 0.0), "mob_areas": [{"name": "Uneg", "pos": (22834, -16309.0, -439.0, 0.0)}, {"name": "Sand Raider", "pos": (22324, -15895.0, -876.0, 0.0)}], "train_radius": 50.0, "pick_radius": 50.0, "state": "LOCKED"},
    {"order": 5, "npc": "Governor Senmute", "turnin_npc": "Governor Senmute", "name": "The Missing High Priest (1)", "servername": "QNO_SD_MA_005", "npc_pos": (23343, -16757.0, -158.0, 0.0), "state": "LOCKED"},
    {"order": 6, "npc": "Doctor Renenutet", "turnin_npc": "Doctor Renenutet", "name": "The Missing High Priest (2)", "servername": "QNO_SD_MA_006", "npc_pos": (23087, -16720.0, -382.0, 0.0), "state": "LOCKED"},
    {"order": 7, "npc": "Finance Officer Maneto", "turnin_npc": "Finance Officer Maneto", "name": "Berenice's Traces", "servername": "QNO_SD_MA_007", "npc_pos": (23345, -16448.0, -79.0, 0.0), "mob_areas": [{"name": "Tathen", "pos": (23861, -15600.0, 237.0, 0.0)}], "train_radius": 50.0, "pick_radius": 50.0, "state": "LOCKED"},
    {"order": 8, "npc": "Finance Officer Maneto", "turnin_npc": "Finance Officer Maneto", "name": "The Heartbreaking News (1)", "servername": "QNO_SD_MA_008", "npc_pos": (23345, -16448.0, -79.0, 0.0), "state": "LOCKED"},
    {"order": 9, "npc": "Doctor Renenutet", "turnin_npc": "Doctor Renenutet", "name": "The Heartbreaking News (2)", "servername": "QNO_SD_MA_009", "npc_pos": (23087, -16720.0, -382.0, 0.0), "state": "LOCKED"},
    {"order": 10, "npc": "Finance Officer Maneto", "turnin_npc": "Finance Officer Maneto", "name": "An Ominous Sense", "servername": "QNO_SD_MA_010", "npc_pos": (23345, -16448.0, -79.0, 0.0), "state": "LOCKED"},
    {"order": 11, "npc": "Governor Senmute", "turnin_npc": "Governor Senmute", "name": "Investigating the Strange Rumor", "servername": "QNO_SD_MA_011", "npc_pos": (23343, -16757.0, -158.0, 0.0), "state": "LOCKED"},
    {"order": 12, "npc": "Doctor Renenutet", "turnin_npc": "Doctor Renenutet", "name": "The Truth of the Strange Rumor (1)", "servername": "QNO_SD_MA_012", "npc_pos": (23087, -16720.0, -382.0, 0.0), "mob_areas": [{"name": "Dark Khepri", "pos": (19258, -14768.0, -3152.0, 0.0)}, {"name": "Desert Bug", "pos": (19259, -14500.0, -3129.0, 0.0)}], "train_radius": 50.0, "pick_radius": 50.0, "state": "LOCKED"},
    {"order": 13, "npc": "Doctor Renenutet", "turnin_npc": "Doctor Renenutet", "name": "The Truth of the Strange Rumor (2)", "servername": "QNO_SD_MA_013", "npc_pos": (23087, -16720.0, -382.0, 0.0), "mob_areas": [{"name": "Dark Sandman", "pos": (19262, -13976.0, -3118.0, 0.0)}, {"name": "Blood Sandman", "pos": (19263, -13693.0, -3179.0, 0.0)}, {"name": "Blood Hyena", "pos": (19265, -13308.0, -3122.0, 0.0)}], "train_radius": 50.0, "pick_radius": 50.0, "state": "LOCKED"},
    {"order": 14, "npc": "Doctor Renenutet", "turnin_npc": "Doctor Renenutet", "name": "The Truth of the Strange Rumor (3)", "servername": "QNO_SD_MA_014", "npc_pos": (23087, -16720.0, -382.0, 0.0), "mob_areas": [{"name": "Ure'uth", "pos": (19523, -12922.0, -3069.0, 0.0)}, {"name": "Mehen", "pos": (19269, -12613.0, -3126.0, 0.0)}, {"name": "Aker", "pos": (19270, -12320.0, -3216.0, 0.0)}], "train_radius": 50.0, "pick_radius": 50.0, "state": "LOCKED"},
    {"order": 15, "npc": "Doctor Renenutet", "turnin_npc": "Doctor Renenutet", "name": "Deranged Mentuhotep", "servername": "QNO_SD_MA_015", "npc_pos": (23087, -16720.0, -382.0, 0.0), "state": "LOCKED"},
    {"order": 16, "npc": "Governor Senmute", "turnin_npc": "Governor Senmute", "name": "Proving My Abilities", "servername": "QNO_SD_MA_016", "npc_pos": (23343, -16757.0, -158.0, 0.0), "mob_areas": [{"name": "Apis", "pos": (19019, -11372.0, -3277.0, 0.0)}], "manual": True, "state": "LOCKED"},
    {"order": 17, "npc": "Governor Senmute", "turnin_npc": "Governor Senmute", "name": "The Overdriving Heart (1)", "servername": "QNO_SD_MA_017", "npc_pos": (23343, -16757.0, -158.0, 0.0), "mob_areas": [{"name": "Sphinx (Tomb Beginner)", "pos": (19019, -11372.0, -3277.0, 0.0)}], "manual": True, "state": "LOCKED"},
    {"order": 18, "npc": "Governor Senmute", "turnin_npc": "Governor Senmute", "name": "The Overdriving Heart (2)", "servername": "QNO_SD_MA_018", "npc_pos": (23343, -16757.0, -158.0, 0.0), "mob_areas": [{"name": "Sekhmet (Tomb Beginner)", "pos": (19019, -11372.0, -3277.0, 0.0)}], "manual": True, "state": "LOCKED"},
    {"order": 19, "npc": "Governor Senmute", "turnin_npc": "Governor Senmute", "name": "The Overdriving Heart (3)", "servername": "QNO_SD_MA_019", "npc_pos": (23343, -16757.0, -158.0, 0.0), "mob_areas": [{"name": "Nephthys (Tomb Beginner)", "pos": (19019, -11372.0, -3277.0, 0.0)}], "manual": True, "state": "LOCKED"},
    {"order": 20, "npc": "Governor Senmute", "turnin_npc": "Governor Senmute", "name": "The Overdriving Heart (4)", "servername": "QNO_SD_MA_020", "npc_pos": (23343, -16757.0, -158.0, 0.0), "mob_areas": [{"name": "Horus (Tomb Beginner)", "pos": (19019, -11372.0, -3277.0, 0.0)}], "manual": True, "state": "LOCKED"},
    {"order": 21, "npc": "Governor Senmute", "turnin_npc": "Governor Senmute", "name": "The Overdriving Heart (5)", "servername": "QNO_SD_MA_021", "npc_pos": (23343, -16757.0, -158.0, 0.0), "mob_areas": [{"name": "Osiris (Tomb Beginner)", "pos": (19019, -11372.0, -3277.0, 0.0)}], "manual": True, "state": "LOCKED"},
]

active_chain = "blue"
current_quest_index = 0
try:
    PLUGIN_DIR = os.path.dirname(os.path.abspath(__file__))
except:
    PLUGIN_DIR = os.getcwd()
PROGRESS_FILE = os.path.join(PLUGIN_DIR, "ZERK_QUEST_PROGRESS.json")
progress_loaded = False
progress_data = {}

GENERAL_NAME = "General Sonhyeon"
GENERAL_REGION = 25255
GENERAL_X = 6202.0
GENERAL_Y = 1176.0
GENERAL_Z = 0.0

EXORCIST_NAME = "Exorcist Miaoryeong"
EXORCIST_REGION = 25253
EXORCIST_X = 5778.0
EXORCIST_Y = 1229.0
EXORCIST_Z = 0.0

BUDDHA_NAME = "Buddhist Priest Jeonghye"
BUDDHA_REGION = 25257
BUDDHA_X = 6594.0
BUDDHA_Y = 1246.0
BUDDHA_Z = 0.0

HUNTER_NAME = "Hunter Associate Gwakwi"
HUNTER_REGION = 25255
HUNTER_X = 6303.0
HUNTER_Y = 1188.0
HUNTER_Z = 0.0
HUNTER_ARRIVAL_DISTANCE = 8.0

ROUTES = {
    "GENERAL_TO_EXORCIST": [
        (6203, 1176, 0),
        (6202, 1169, 0),
        (6202, 1168, 0),
        (6202, 1167, 0),
        (6202, 1166, 0),
        (6202, 1165, 0),
        (6184, 1154, 0),
        (6180, 1150, 0),
        (6132, 1150, 0),
        (6131, 1151, 0),
        (6121, 1161, 0),
        (6111, 1171, 0),
        (6101, 1181, 0),
        (6091, 1191, 0),
        (6077, 1193, 0),
        (6063, 1194, 0),
        (6049, 1196, 0),
        (6035, 1198, 0),
        (6021, 1200, 0),
        (6008, 1202, 0),
        (5997, 1211, 0),
        (5986, 1220, 0),
        (5975, 1229, 0),
        (5965, 1238, 0),
        (5955, 1248, 0),
        (5945, 1258, 0),
        (5935, 1268, 0),
        (5880, 1278, 0),
        (5879, 1278, 0),
        (5869, 1268, 0),
        (5859, 1258, 0),
        (5849, 1248, 0),
        (5839, 1238, 0),
        (5827, 1232, 0),
        (5813, 1232, 0),
        (5799, 1232, 0),
        (5789, 1222, 0),
        (5781, 1225, 0),
        (5781, 1226, 0),
        (5781, 1227, 0),
        (5781, 1228, 0),
        (5780, 1229, 0),
        (5779, 1230, 0),
        (5778, 1231, 0),
        (5777, 1232, 0),
        (5778, 1229, 0),
    ],
    "EXORCIST_TO_B2_STONE_BEAST": [
        'walk,5775,1227,0',
        'walk,5776,1226,0',
        'walk,5777,1225,0',
        'walk,5778,1224,0',
        'walk,5779,1223,0',
        'walk,5780,1222,0',
        'walk,5793,1226,0',
        'walk,5803,1236,0',
        'walk,5813,1246,0',
        'walk,5823,1256,0',
        'walk,5835,1263,0',
        'walk,5847,1270,0',
        'walk,5859,1275,0',
        'walk,5873,1277,0',
        'walk,5880,1278,0',
        'walk,5935,1268,0',
        'walk,5936,1268,0',
        'walk,5937,1268,0',
        'walk,5938,1268,0',
        'walk,5939,1268,0',
        'walk,5940,1268,0',
        'walk,5954,1268,0',
        'walk,5968,1268,0',
        'walk,5982,1268,0',
        'walk,5996,1268,0',
        'walk,6010,1268,0',
        'walk,6022,1264,0',
        'walk,6032,1254,0',
        'walk,6042,1244,0',
        'walk,6052,1234,0',
        'walk,6062,1224,0',
        'walk,6072,1214,0',
        'walk,6082,1204,0',
        'walk,6092,1194,0',
        'walk,6102,1184,0',
        'walk,6112,1174,0',
        'walk,6122,1164,0',
        'walk,6132,1154,0',
        'walk,6132,1150,0',
        'walk,6180,1150,0',
        'walk,6181,1150,0',
        'walk,6182,1150,0',
        'walk,6183,1150,0',
        'walk,6184,1150,0',
        'walk,6185,1150,0',
        'walk,6199,1150,0',
        'walk,6213,1150,0',
        'walk,6227,1150,0',
        'walk,6241,1150,0',
        'walk,6255,1150,0',
        'walk,6269,1150,0',
        'walk,6283,1150,0',
        'walk,6297,1150,0',
        'walk,6311,1150,0',
        'walk,6325,1148,0',
        'walk,6337,1142,0',
        'walk,6350,1138,0',
        'walk,6364,1138,0',
        'walk,6378,1138,0',
        'walk,6392,1138,0',
        'walk,6406,1138,0',
        'walk,6420,1138,0',
        'walk,6434,1138,0',
        'walk,6448,1138,0',
        'walk,6462,1138,0',
        'walk,6476,1138,0',
        'walk,6490,1138,0',
        'walk,6504,1138,0',
        'walk,6517,1140,0',
        'walk,6531,1142,0',
        'walk,6545,1143,0',
        'walk,6559,1144,0',
        'walk,6573,1144,0',
        'walk,6587,1144,0',
        'walk,6601,1144,0',
        'walk,6615,1145,0',
        'walk,6629,1145,0',
        'walk,6643,1145,0',
        'walk,6657,1145,0',
        'walk,6662,1142,0',
        'walk,6712,1142,0',
        'walk,6713,1143,0',
        'walk,6714,1144,0',
        'walk,6715,1145,0',
        'walk,6716,1145,0',
        'walk,6717,1145,0',
        'walk,6731,1145,0',
        'walk,6745,1146,0',
        'walk,6759,1146,0',
        'walk,6773,1146,0',
        'walk,6787,1146,0',
        'walk,6801,1146,0',
        'walk,6815,1146,0',
        'walk,6829,1146,0',
        'walk,6843,1146,0',
        'walk,6857,1148,0',
        'walk,6868,1157,0',
        'walk,6879,1165,0',
        'walk,6892,1168,0',
        'walk,6906,1168,0',
        'walk,6920,1168,0',
        'walk,6934,1168,0',
        'walk,6948,1168,0',
        'walk,6962,1168,0',
        'walk,6976,1168,0',
        'walk,6990,1168,0',
        'walk,7004,1168,0',
        'walk,7018,1168,0',
        'walk,7028,1177,0',
        'walk,7038,1187,0',
        'walk,7048,1196,0',
        'walk,7058,1206,0',
        'walk,7068,1215,0',
        'walk,7078,1225,0',
        'walk,7088,1234,0',
        'walk,7098,1243,0',
        'walk,7109,1252,0',
        'walk,7118,1263,0',
        'walk,7122,1276,0',
        'walk,7122,1290,0',
        'walk,7123,1304,0',
        'walk,7126,1317,0',
        'walk,7128,1331,0',
        'walk,7128,1345,0',
        'walk,7128,1359,0',
        'walk,7136,1370,0',
        'walk,7146,1380,0',
        'walk,7155,1390,0',
        'walk,7165,1399,0',
        'walk,7175,1408,0',
        'walk,7185,1418,0',
        'walk,7195,1428,0',
        'walk,7196,1442,0',
        'walk,7196,1456,0',
        'walk,7196,1470,0',
        'walk,7196,1484,0',
        'walk,7196,1498,0',
        'walk,7196,1512,0',
        'walk,7196,1526,0',
        'walk,7196,1540,0',
        'walk,7196,1554,0',
        'walk,7196,1568,0',
        'walk,7196,1582,0',
        'walk,7196,1596,0',
        'walk,7196,1610,0',
        'walk,7196,1624,0',
        'walk,7196,1638,0',
        'walk,7196,1652,0',
        'walk,7196,1666,0',
        'walk,7196,1680,0',
        'walk,7196,1694,0',
        'walk,7196,1708,0',
        'walk,7196,1722,0',
        'walk,7196,1736,0',
        'walk,7196,1750,0',
        'walk,7196,1764,0',
        'walk,7196,1778,0',
        'walk,7196,1792,0',
        'walk,7196,1806,0',
        'walk,7196,1820,0',
        'walk,7196,1834,0',
        'walk,7196,1848,0',
        'walk,7196,1862,0',
        'walk,7199,1869,0',
        'walk,7200,1870,0',
        'walk,7200,1871,0',
        'walk,7200,1927,0',
        'walk,7199,1928,0',
        'walk,7199,1929,0',
        'walk,7199,1930,0',
        'walk,7199,1931,0',
        'walk,7199,1932,0',
        'walk,7199,1933,0',
        'walk,7199,1934,0',
        'walk,7199,1935,0',
        'walk,7199,1936,0',
        'walk,7199,1937,0',
        'walk,7199,1938,0',
        'walk,7199,1939,0',
        'walk,7199,1940,0',
        'walk,7199,1941,0',
        'walk,7199,1942,0',
        'walk,7199,1943,0',
        'walk,7199,1944,0',
        'walk,7199,1945,0',
        'walk,7199,1946,0',
        'walk,7199,1947,0',
        'walk,7200,1961,0',
        'walk,7200,1975,0',
        'walk,7200,1989,0',
        'walk,7201,2002,0',
        'walk,7200,2002,0',
        'walk,7200,2059,0',
        'walk,7200,2060,0',
        'walk,7200,2061,0',
        'walk,7200,2062,0',
        'walk,7200,2063,0',
        'walk,7200,2064,0',
        'walk,7200,2078,0',
        'walk,7200,2086,0',
        'walk,7200,2086,0',
        'walk,7200,2087,0',
        'walk,7200,2088,0',
        'walk,7200,2089,0',
        'walk,7200,2090,0',
        'walk,7200,2091,0',
        'walk,7200,2092,0',
        'walk,7200,2093,0',
        'walk,7200,2093,0',
        'walk,7200,2094,0',
        'walk,7200,2095,0',
        'walk,7200,2096,0',
        'walk,7199,2097,0',
        'walk,7199,2097,0',
        'walk,7200,2104,150',
        'wait,10000',
        'walk,-32761,-23234,-317,0',
        'walk,-32761,-23239,-305,0',
        'walk,-32761,-23249,-295,0',
        'walk,-32761,-23252,-282,0',
        'walk,-32761,-23252,-268,0',
        'walk,-32761,-23253,-254,0',
        'walk,-32761,-23253,-240,0',
        'walk,-32761,-23253,-226,0',
        'walk,-32761,-23253,-212,0',
        'walk,-32761,-23253,-198,0',
        'walk,-32761,-23254,-184,0',
        'walk,-32761,-23254,-170,0',
        'walk,-32761,-23254,-156,0',
        'walk,-32761,-23254,-142,0',
        'walk,-32761,-23254,-128,0',
        'walk,-32761,-23254,-114,0',
        'walk,-32761,-23254,-100,0',
        'walk,-32761,-23254,-86,0',
        'walk,-32761,-23254,-72,0',
        'walk,-32761,-23254,-58,0',
        'walk,-32761,-23254,-44,0',
        'walk,-32761,-23254,-30,0',
        'walk,-32761,-23254,-16,0',
        'walk,-32761,-23254,-2,0',
        'walk,-32761,-23254,12,0',
        'walk,-32761,-23254,26,0',
        'walk,-32761,-23257,39,0',
        'walk,-32761,-23266,49,0',
        'walk,-32761,-23276,59,0',
        'walk,-32761,-23284,70,0',
        'walk,-32761,-23284,84,0',
        'walk,-32761,-23284,98,0',
        'walk,-32761,-23284,112,0',
        'walk,-32761,-23284,126,0',
        'walk,-32761,-23284,140,0',
        'walk,-32761,-23284,154,0',
        'walk,-32761,-23284,168,0',
        'walk,-32761,-23284,182,0',
        'walk,-32761,-23284,196,0',
        'walk,-32761,-23284,210,0',
        'walk,-32761,-23284,224,0',
        'walk,-32761,-23284,238,0',
        'walk,-32761,-23288,251,0',
        'walk,-32761,-23298,261,0',
        'walk,-32761,-23308,271,0',
        'walk,-32761,-23318,281,0',
        'walk,-32761,-23328,291,0',
        'walk,-32761,-23338,301,0',
        'walk,-32761,-23348,311,0',
        'walk,-32761,-23358,321,0',
        'walk,-32761,-23368,331,0',
        'walk,-32761,-23376,342,0',
        'walk,-32761,-23383,353,0',
        'walk,-32761,-23392,364,0',
        'walk,-32761,-23393,378,0',
        'walk,-32761,-23393,392,0',
        'walk,-32761,-23393,406,0',
        'walk,-32761,-23393,420,0',
        'walk,-32761,-23393,434,0',
        'walk,-32761,-23393,448,0',
        'walk,-32761,-23393,462,0',
        'walk,-32761,-23393,476,0',
        'walk,-32761,-23393,490,0',
        'walk,-32761,-23393,504,0',
        'walk,-32761,-23393,518,0',
        'walk,-32761,-23387,530,0',
        'walk,-32761,-23377,540,0',
        'walk,-32761,-23367,550,0',
        'walk,-32761,-23357,560,0',
        'walk,-32761,-23347,570,0',
        'walk,-32761,-23337,580,0',
        'walk,-32761,-23327,590,0',
        'walk,-32761,-23317,600,0',
        'walk,-32761,-23307,610,0',
        'walk,-32761,-23297,620,0',
        'walk,-32761,-23287,630,0',
        'walk,-32761,-23277,640,0',
        'walk,-32761,-23267,650,0',
        'walk,-32761,-23257,660,0',
        'walk,-32761,-23247,670,0',
        'walk,-32761,-23232,715,0',
        'walk,-32761,-23236,651,223',
        'walk,-32761,-23232,659,223',
        'wait,10000',
        'walk,-32762,-24772,561,0',
        'walk,-32762,-24753,561,0',
        'walk,-32762,-24730,560,0',
        'walk,-32762,-24711,560,0',
        'walk,-32762,-24692,560,0',
        'walk,-32762,-24661,560,-47',
        'walk,-32762,-24642,560,-47',
        'walk,-32762,-24625,560,-47',
        'walk,-32762,-24608,559,-47',
        'walk,-32762,-24592,559,-47',
        'walk,-32762,-24580,559,-18',
        'walk,-32762,-24565,559,0',
        'walk,-32762,-24546,559,0',
        'walk,-32762,-24528,559,0',
        'walk,-32762,-24511,559,0',
        'walk,-32762,-24493,559,0',
        'walk,-32762,-24475,558,0',
        'walk,-32762,-24466,559,0',
        'walk,-32762,-24459,559,0',
        'wait,10000',
        'walk,-32762,-24236,558,0',
        'walk,-32762,-24220,559,0',
        'walk,-32762,-24187,558,0',
    ],
    "BUDDHA_TO_Q4_PATH_START": [
        'walk,6595,1237,0',
        'walk,6596,1227,2',
        'walk,6597,1216,0',
        'walk,6608,1212,0',
        'walk,6607,1214,0',
    ],
}

ARRIVAL_DISTANCE = 18.0
EXORCIST_ARRIVAL_DISTANCE = 4.0
EXORCIST_ACCEPT_DISTANCE = 18.0
BUDDHA_ARRIVAL_DISTANCE = 8.0
Q3_DUNGEON_REGION = -32762
Q3_DUNGEON_X = -24187.0
Q3_DUNGEON_Y = 558.0
Q3_DUNGEON_Z = 0.0
Q3_DUNGEON_ARRIVAL_DISTANCE = 18.0
Q3_TRAIN_RADIUS = 50.0
Q3_TRAIN_CHECK_DELAY = 2.0
Q3_RETURN_SCROLL_DELAY = 3.0
Q3_TOWN_CHECK_DELAY = 4.0
Q1_ARENA_TRAIN_RADIUS = 50.0
Q1_ARENA_PICK_RADIUS = 50.0
Q1_ARENA_TRAIN_CHECK_DELAY = 2.0
Q4_TOMB_REGION = 23980
Q4_TOMB_X = 7179.0
Q4_TOMB_Y = 311.0
Q4_TOMB_Z = 0.0
Q4_TOMB_ARRIVAL_DISTANCE = 18.0
Q4_TOMB_MANUAL_DISTANCE = 80.0
Q4_PREFIX_TARGET_X = 6607.0
Q4_PREFIX_TARGET_Y = 1214.0
Q4_PREFIX_ARRIVAL_DISTANCE = 8.0
Q4_PREFIX_MIN_WAIT = 1.0
Q4_PREFIX_TIMEOUT = 12.0
Q4_TRAIN_RADIUS = 10.0
Q4_PICK_RADIUS = 50.0
Q4_TRAIN_CHECK_DELAY = 2.0
Q4_SPIRIT_BELL_ITEM = "Spirit's Bell"
Q4_SPIRIT_BELL_ID = 23329
Q4_SPIRIT_BELL_ITEM_TYPE = 0x0C30
Q4_SPIRIT_BELL_USE_ARG = 0x0009
DELAY_AFTER_Q4_USE_BELL = 2.50
Q4_RETURN_SCROLL_DELAY = 3.0
Q4_TOWN_CHECK_DELAY = 4.0
RETURN_SCROLL_NORMAL_COMMAND = "use,returnscroll"
RETURN_SCROLL_SPECIAL_COMMAND = "use,Special Return Scroll"
RETURN_SCROLL_INSTANT_COMMAND = "use,Instant Return Scroll"
RETURN_SCROLL_RETRY_DELAY = 8.0
RETURN_SCROLL_MAX_ATTEMPTS = 3
Q5_HUNTER_TALK_OPTION = 0x06
Q5_HUNTER_REWARD_DELAY = 4.00
Q6_MANUAL_CAPTURE_MESSAGE = "ZERK QUEST: DO THIS PART MANUALLY. After collecting the spirit, press QUEST 6 again to resume and finish the quest automatically."
Q7_MANUAL_ZERK_MESSAGE = "TALK AGAIN WITH HER WITH FULL ZERK. KILL THE SPIRIT WHILE ZERK IS ACTIVE."
JANGAN_REGION_MIN = 25000
JANGAN_REGION_MAX = 25299
Q6_RETURN_SCROLL_DELAY = 3.0
Q6_TOWN_CHECK_DELAY = 4.0
INVENTORY_NPC_ARRIVAL_DISTANCE = 32.0
INVENTORY_MOB_ARRIVAL_DISTANCE = 25.0
INVENTORY_TRAIN_RADIUS = 25.0
INVENTORY_PICK_RADIUS = 50.0
INVENTORY_TRAIN_CHECK_DELAY = 2.0
INVENTORY_RETURN_SCROLL_DELAY = 3.0
INVENTORY_TOWN_CHECK_DELAY = 4.0
INVENTORY_REVERSE_WIND_COMMAND = "reverse,location,Wind Town"
INVENTORY_AFTER_REVERSE_DELAY = 5.0
INVENTORY_PATH_STUCK_SECONDS = 5.0
INVENTORY_PATH_PROGRESS_EPSILON = 4.0
HUNTER_AUTO_PATH_TIMEOUT = 45.0
EXORCIST_AUTO_PATH_TIMEOUT = 25.0
EXORCIST_AUTO_PATH_MAX_RETRIES = 2
EXORCIST_AUTO_PATH_NUDGE = 2.0
DELAY_AFTER_EXORCIST_NUDGE = 2.0
AUTO_PATH_TIMEOUT = 25.0
AUTO_PATH_MAX_RETRIES = 2
AUTO_PATH_NUDGE = 2.0
DELAY_AFTER_AUTO_PATH_NUDGE = 2.0
PATH_STUCK_SECONDS = 5.0
PATH_START_GRACE_SECONDS = 12.0
PATH_MOVE_EPSILON = 1.5
PATH_DEST_PROGRESS_EPSILON = 4.0
Q4_TOMB_PROGRESS_LOG_SECONDS = 8.0
MAX_HANDIN_REWARD_RETRIES = 3
ARENA_REGION = 22966
ARENA_X = 9120.0
ARENA_Y = -463.0
ARENA_Z = 51.8
ARENA_MAX_DISTANCE = 50.0
CONFIRM_OK_OPCODE = 0x30D4
CONFIRM_OK_VALUE = 0x05
MAX_CONFIRM_OK_ATTEMPTS = 3
DELAY_AFTER_QUEST_CMD = 2.50
DELAY_AFTER_CONFIRM_OK = 1.50
DELAY_RETRY_CONFIRM_OK = 1.50
DELAY_BEFORE_SECOND_DIALOG = 1.20
DELAY_AFTER_OPEN_SECOND_DIALOG = 1.20
DELAY_AFTER_ARENA_QUEST_OPTION = 2.00
DELAY_AFTER_ARENA_ENTER_OPTION = 2.00
DELAY_WAIT_ARENA_TELEPORT = 6.00
MAX_ARENA_ENTRY_ATTEMPTS = 3
DELAY_AFTER_HANDIN_CMD = 2.50
DELAY_AFTER_HANDIN_OK = 1.50
DELAY_AFTER_REWARD = 2.00
DELAY_BEFORE_REWARD_CLOSE = 0.60
DELAY_AFTER_REWARD_CLOSE = 1.40
DELAY_BEFORE_POST_ACCEPT_OK = 1.20
DELAY_AFTER_POST_ACCEPT_OK = 1.20
STATE_IDLE = "IDLE"
STATE_GO_GENERAL = "GO_GENERAL"
STATE_GENERAL_AUTO_RETRY = "GENERAL_AUTO_RETRY"
STATE_SELECT_1 = "SELECT_1"
STATE_OPEN_1 = "OPEN_1"
STATE_ACCEPT = "ACCEPT"
STATE_CONFIRM_OK = "CONFIRM_OK"
STATE_WAIT_ACCEPT = "WAIT_ACCEPT"
STATE_POST_ACCEPT_OK = "POST_ACCEPT_OK"
STATE_POST_ACCEPT_CONTINUE = "POST_ACCEPT_CONTINUE"
STATE_SELECT_2 = "SELECT_2"
STATE_OPEN_2 = "OPEN_2"
STATE_ARENA_QUEST_OPTION = "ARENA_QUEST_OPTION"
STATE_ARENA_ENTER_OPTION = "ARENA_ENTER_OPTION"
STATE_ARENA_CONFIRM = "ARENA_CONFIRM"
STATE_WAIT_ENTER = "WAIT_ENTER"
STATE_ARENA = "ARENA"
STATE_WAIT_RETURN_CHECK = "WAIT_RETURN_CHECK"
STATE_WAIT_RETURN_FAIL = "WAIT_RETURN_FAIL"
STATE_GO_HANDIN_GENERAL = "GO_HANDIN_GENERAL"
STATE_HANDIN = "HANDIN"
STATE_HANDIN_OK = "HANDIN_OK"
STATE_HANDIN_REWARD = "HANDIN_REWARD"
STATE_HANDIN_CLOSE = "HANDIN_CLOSE"
STATE_WAIT_HANDIN = "WAIT_HANDIN"
STATE_GO_EXORCIST = "GO_EXORCIST"
STATE_GO_BUDDHA = "GO_BUDDHA"
STATE_BUDDHA_AUTO_RETRY = "BUDDHA_AUTO_RETRY"
STATE_GO_HUNTER = "GO_HUNTER"
STATE_HUNTER_AUTO_RETRY = "HUNTER_AUTO_RETRY"
STATE_Q5_HUNTER_SELECT = "Q5_HUNTER_SELECT"
STATE_Q5_HUNTER_OPEN = "Q5_HUNTER_OPEN"
STATE_Q5_HUNTER_TALK = "Q5_HUNTER_TALK"
STATE_Q5_HUNTER_REWARD = "Q5_HUNTER_REWARD"
STATE_GO_Q3_DUNGEON = "GO_Q3_DUNGEON"
STATE_Q3_TRAIN = "Q3_TRAIN"
STATE_Q3_RETURN_SCROLL = "Q3_RETURN_SCROLL"
STATE_Q3_WAIT_TOWN = "Q3_WAIT_TOWN"
STATE_GO_Q4_TOMB = "GO_Q4_TOMB"
STATE_Q4_TOMB_PREFIX_WAIT = "Q4_TOMB_PREFIX_WAIT"
STATE_Q4_TOMB_START_PATH = "Q4_TOMB_START_PATH"
STATE_Q4_TOMB_AUTO_RETRY = "Q4_TOMB_AUTO_RETRY"
STATE_Q4_WAIT_MANUAL_TOMB = "Q4_WAIT_MANUAL_TOMB"
STATE_Q4_USE_BELL = "Q4_USE_BELL"
STATE_Q4_START_TRAIN = "Q4_START_TRAIN"
STATE_Q4_TRAIN = "Q4_TRAIN"
STATE_Q4_RETURN_SCROLL = "Q4_RETURN_SCROLL"
STATE_Q4_WAIT_TOWN = "Q4_WAIT_TOWN"
STATE_Q6_RETURN_SCROLL = "Q6_RETURN_SCROLL"
STATE_Q6_WAIT_TOWN = "Q6_WAIT_TOWN"
STATE_INVENTORY_GO_NPC = "INVENTORY_GO_NPC"
STATE_INVENTORY_GO_MOB = "INVENTORY_GO_MOB"
STATE_INVENTORY_TRAIN = "INVENTORY_TRAIN"
STATE_INVENTORY_RETURN_SCROLL = "INVENTORY_RETURN_SCROLL"
STATE_INVENTORY_WAIT_TOWN = "INVENTORY_WAIT_TOWN"
STATE_INVENTORY_REVERSE_WIND = "INVENTORY_REVERSE_WIND"
STATE_INVENTORY_AFTER_REVERSE = "INVENTORY_AFTER_REVERSE"
STATE_EXORCIST_AUTO_RETRY = "EXORCIST_AUTO_RETRY"
STATE_ACCEPT_NEXT = "ACCEPT_NEXT"
STATE_CONFIRM_NEXT_OK = "CONFIRM_NEXT_OK"
STATE_WAIT_NEXT_ACCEPT = "WAIT_NEXT_ACCEPT"
STATE_DONE = "DONE"

ARENA_ENTRY_STATES = (
    STATE_ARENA_QUEST_OPTION,
    STATE_ARENA_ENTER_OPTION,
    STATE_ARENA_CONFIRM,
    STATE_WAIT_ENTER,
)

state = STATE_IDLE
state_time = 0.0
capture_client = False
death_seen = False
success_seen = False
last_loop = 0.0
confirm_ok_attempts = 0
arena_started_at = 0.0
arena_entry_attempts = 0
exorcist_route_mode = ""
exorcist_route_fallback = None
exorcist_path_started_at = 0.0
exorcist_path_retries = 0
exorcist_path_origin = None
general_path_started_at = 0.0
general_path_retries = 0
general_path_origin = None
general_retry_next_state = STATE_GO_GENERAL
general_retry_reason = "PATH -> General Sonhyeon"
buddha_path_started_at = 0.0
buddha_path_retries = 0
buddha_path_origin = None
buddha_retry_reason = "Indo para Buddhist Priest Jeonghye por path automatico."
hunter_path_started_at = 0.0
hunter_path_retries = 0
hunter_path_origin = None
hunter_retry_reason = "Indo para Hunter Associate Gwakwi por path automatico."
q4_tomb_path_started_at = 0.0
q4_tomb_path_retries = 0
q4_tomb_path_origin = None
q4_tomb_prefix_started_at = 0.0
q4_tomb_last_dist = 999999.0
q4_tomb_last_progress_at = 0.0
q4_tomb_last_progress_log_at = 0.0
inventory_path_started_at = 0.0
inventory_path_retries = 0
inventory_target = None
inventory_target_kind = ""
inventory_last_distance = 999999.0
inventory_last_progress_at = 0.0
inventory_last_progress_log_at = 0.0
inventory_reverse_next_kind = "NPC"
handin_reward_retry_count = 0
quest_accept_name_index = 0
post_accept_ok_sent = False
path_watch_state = ""
path_watch_last_pos = None
path_watch_last_moved_at = 0.0
last_dialog_npc_uid = None
last_dialog_npc_name = ""
return_scroll_attempts = 0
return_scroll_commands = []
return_scroll_wait_state = ""
return_scroll_label = ""
return_scroll_delay = 0.0

def zlog(msg):
    log("[ZERK] " + str(msg))

def show_ui_page(page):
    global ui_page
    ui_page = page
    titles = {
        "blue": "Blue Zerk (level 95)",
        "inventory": "Inventory Expansion Quest",
        "zerk105": "Zerk 105 Prerequisites"
    }
    try:
        QtBind.setText(gui, lblPageTitle, titles.get(page, page))
    except:
        pass
    for page_name, widgets in page_widgets.items():
        visible = page_name == page
        for widget, x, y in widgets:
            try:
                if visible:
                    QtBind.move(gui, widget, x, y)
                else:
                    QtBind.move(gui, widget, HIDDEN_X, HIDDEN_Y)
            except:
                pass

def btnShowBlueZerkTab():
    set_active_chain_for_status("blue")
    show_ui_page("blue")
    refresh_status_ui()

def btnShowInventoryTab():
    set_active_chain_for_status("inventory")
    show_ui_page("inventory")
    refresh_status_ui()

def btnShowZerk105Tab():
    set_active_chain_for_status("zerk105")
    show_ui_page("zerk105")
    refresh_status_ui()

def btnInventoryPlaceholder():
    msg = "Inventory Expansion Quest is not configured yet. Add NPCs, quest names and coordinates first."
    zlog(msg)
    show_client_notice(msg)

def set_active_chain(chain):
    global active_chain
    active_chain = chain
    refresh_status_ui()

def set_active_chain_for_status(chain):
    global active_chain
    active_chain = chain

def current_quest_list():
    if active_chain == "zerk105":
        return ZERK_105_QUESTS
    if active_chain == "inventory":
        return INVENTORY_QUESTS
    return ZERK_1_QUESTS

def chain_progress_field():
    if active_chain == "zerk105":
        return "zerk105_done"
    if active_chain == "inventory":
        return "inventory_done"
    return "done"

def chain_label():
    if active_chain == "zerk105":
        return "ZERK105"
    if active_chain == "inventory":
        return "INVENTORY"
    return "ZERK"

def character_progress_key():
    try:
        char = get_character_data()
        if char:
            for key in ("name", "player_name", "charname"):
                value = str(char.get(key, "")).strip()
                if value:
                    return value
    except:
        pass
    return "UNKNOWN"

def load_progress():
    global progress_loaded, progress_data
    if progress_loaded:
        return
    progress_loaded = True
    progress_data = {}
    try:
        if os.path.exists(PROGRESS_FILE):
            with open(PROGRESS_FILE, "r") as f:
                data = json.load(f)
            if isinstance(data, dict):
                progress_data = data
    except Exception as ex:
        zlog("PROGRESS LOAD ERRO: %s" % str(ex))
        progress_data = {}

def save_progress():
    try:
        with open(PROGRESS_FILE, "w") as f:
            json.dump(progress_data, f, indent=2, sort_keys=True)
    except Exception as ex:
        zlog("PROGRESS SAVE ERRO: %s" % str(ex))

def progress_entry():
    load_progress()
    key = character_progress_key()
    entry = progress_data.get(key)
    if not isinstance(entry, dict):
        entry = {"done": []}
        progress_data[key] = entry
    if not isinstance(entry.get("done"), list):
        entry["done"] = []
    return key, entry

def completed_orders():
    key, entry = progress_entry()
    field = chain_progress_field()
    done = set()
    for value in entry.get(field, []):
        try:
            done.add(int(value))
        except:
            pass
    return done

def mark_quest_done(order):
    key, entry = progress_entry()
    field = chain_progress_field()
    done = completed_orders()
    done.add(int(order))
    entry[field] = sorted(list(done))
    entry["updated_at"] = int(time.time())
    progress_data[key] = entry
    save_progress()
    zlog("PROGRESS SAVE -> %s %s Q%d DONE" % (key, chain_label(), int(order)))

def set_state(new_state, delay=0.0):
    global state, state_time, path_watch_state, path_watch_last_pos, path_watch_last_moved_at
    if new_state != state:
        path_watch_state = ""
        path_watch_last_pos = None
        path_watch_last_moved_at = 0.0
    state = new_state
    state_time = time.time() + float(delay)
    try:
        refresh_status_ui()
    except:
        pass
    zlog("STATE -> %s" % new_state)

def current_quest():
    quests = current_quest_list()
    if 0 <= current_quest_index < len(quests):
        return quests[current_quest_index]
    return None

def quest_names(qdef):
    if not qdef:
        return []
    names = [str(qdef.get("name", ""))]
    for alias in qdef.get("aliases", []):
        alias = str(alias)
        if alias and alias not in names:
            names.append(alias)
    return names

def quest_servernames(qdef):
    if not qdef:
        return []
    names = [str(qdef.get("servername", ""))]
    for alias in qdef.get("servername_aliases", []):
        alias = str(alias)
        if alias and alias not in names:
            names.append(alias)
    return names

def current_accept_quest_name():
    qdef = current_quest()
    names = quest_names(qdef)
    if not names:
        return ""
    index = quest_accept_name_index
    if index < 0 or index >= len(names):
        index = 0
    return names[index]

def has_next_accept_quest_name():
    qdef = current_quest()
    return quest_accept_name_index + 1 < len(quest_names(qdef))

def next_accept_quest_name():
    global quest_accept_name_index, confirm_ok_attempts
    quest_accept_name_index += 1
    confirm_ok_attempts = 0
    return current_accept_quest_name()

def needs_post_accept_ok():
    qdef = current_quest()
    if not qdef:
        return False
    return bool(qdef.get("post_accept_ok", False)) and not post_accept_ok_sent

def active_chain_status():
    try:
        quests = get_quests()
        if not quests:
            return 0, "NOT_FOUND"
        for qid, active in quests.items():
            active_name = str(active.get("name", ""))
            active_servername = str(active.get("servername", ""))
            for qdef in current_quest_list():
                if active_servername in quest_servernames(qdef) or active_name in quest_names(qdef):
                    if bool(active.get("completed", False)):
                        return int(qdef["order"]), "COMPLETED"
                    if bool(active.get("objectives_completed", False)):
                        return int(qdef["order"]), "OBJECTIVES_COMPLETED"
                    return int(qdef["order"]), "ACTIVE"
    except:
        pass
    return 0, "NOT_FOUND"

def quest_display_state(qdef, active_order, active_status, done_orders):
    order = int(qdef["order"])
    if order in done_orders or (active_order > 0 and order < active_order):
        return "DONE", "#55ff55"
    if order == active_order:
        if active_status in ("COMPLETED", "OBJECTIVES_COMPLETED"):
            return "READY", "#55ff55"
        return "ACTIVE", "#ffd966"
    if active_order > 0:
        next_available = active_order
    elif done_orders:
        next_available = max(done_orders) + 1
    else:
        next_available = 1
    if order == next_available:
        return "OPEN", "#66ccff"
    return "LOCKED", "#999999"

def log_chain():
    refresh_status_ui()
    active_order, active_status = active_chain_status()
    done_orders = completed_orders()
    zlog("------------ %s QUEST ------------" % chain_label())
    for i, q in enumerate(current_quest_list()):
        q["state"], color = quest_display_state(q, active_order, active_status, done_orders)
        arrow = "->" if i == current_quest_index else "  "
        zlog("%s [%s] %d - %s | %s" % (arrow, q["state"], q["order"], q["name"], q["servername"]))
    zlog("--------------------------------------")

def status_html(text, color):
    return "<font color='%s'>%s</font>" % (color, text)

def quest_status_line(qdef, state_text):
    suffix = ""
    try:
        mobs = qdef.get("mob_areas", [])
        if mobs:
            suffix = " -> " + " / ".join([str(m.get("name", "")) for m in mobs if m.get("name")])
        if bool(qdef.get("manual", False)):
            suffix += " [MANUAL]"
    except:
        suffix = ""
    return "Q%d: %s - %s%s" % (int(qdef["order"]), state_text, qdef["name"], suffix)

def refresh_status_ui():
    saved_chain = active_chain

    set_active_chain_for_status("blue")
    active_order, active_status = active_chain_status()
    done_orders = completed_orders()

    try:
        QtBind.clear(gui, lstBlueQuestStatus)
    except:
        pass
    for q in ZERK_1_QUESTS:
        state_text, color = quest_display_state(q, active_order, active_status, done_orders)
        q["state"] = state_text
        try:
            QtBind.append(gui, lstBlueQuestStatus, quest_status_line(q, state_text))
        except:
            pass

    set_active_chain_for_status("inventory")
    inv_active_order, inv_active_status = active_chain_status()
    inv_done_orders = completed_orders()
    try:
        QtBind.clear(gui, lstInventoryQuestStatus)
    except:
        pass
    for i, q in enumerate(INVENTORY_QUESTS):
        state_text, color = quest_display_state(q, inv_active_order, inv_active_status, inv_done_orders)
        q["state"] = state_text
        try:
            QtBind.append(gui, lstInventoryQuestStatus, quest_status_line(q, state_text))
        except:
            pass

    set_active_chain_for_status("zerk105")
    z105_active_order, z105_active_status = active_chain_status()
    z105_done_orders = completed_orders()
    try:
        QtBind.clear(gui, lstZerk105QuestStatus)
    except:
        pass
    for q in ZERK_105_QUESTS:
        state_text, color = quest_display_state(q, z105_active_order, z105_active_status, z105_done_orders)
        q["state"] = state_text
        try:
            QtBind.append(gui, lstZerk105QuestStatus, quest_status_line(q, state_text))
        except:
            pass

    set_active_chain_for_status(saved_chain)

def get_distance_to_general():
    try:
        pos = get_position()
        if not pos:
            return 999999.0
        dx = float(pos["x"]) - GENERAL_X
        dy = float(pos["y"]) - GENERAL_Y
        return (dx * dx + dy * dy) ** 0.5
    except:
        return 999999.0

def get_distance_to(x, y):
    try:
        pos = get_position()
        if not pos:
            return 999999.0
        dx = float(pos["x"]) - float(x)
        dy = float(pos["y"]) - float(y)
        return (dx * dx + dy * dy) ** 0.5
    except:
        return 999999.0

def current_region():
    try:
        pos = get_position()
        if not pos:
            return 0
        return int(pos.get("region", 0) or 0)
    except:
        return 0

def q4_tomb_arrival_distance():
    dist = get_distance_to(Q4_TOMB_X, Q4_TOMB_Y)
    region = current_region()
    if region == Q4_TOMB_REGION and dist <= Q4_TOMB_MANUAL_DISTANCE:
        return dist
    return 999999.0

def wait_q4_tomb_arrival(reason):
    stop_script()
    capture_on()
    zlog("%s Aguardando chegada manual/TP no Tombstone para usar Spirit's Bell." % reason)
    set_state(STATE_Q4_WAIT_MANUAL_TOMB, 1.0)

def q4_tomb_path_is_progressing(dist):
    global q4_tomb_path_started_at, q4_tomb_last_dist, q4_tomb_last_progress_at, q4_tomb_last_progress_log_at
    now = time.time()
    if q4_tomb_last_dist >= 999998.0:
        q4_tomb_last_dist = dist
        q4_tomb_last_progress_at = now
        return True
    if dist <= q4_tomb_last_dist - PATH_DEST_PROGRESS_EPSILON:
        q4_tomb_last_dist = dist
        q4_tomb_last_progress_at = now
        q4_tomb_path_started_at = now
        if now - q4_tomb_last_progress_log_at >= Q4_TOMB_PROGRESS_LOG_SECONDS:
            zlog("Q4 TOMB PATH OK -> distancia diminuindo: %.1f" % dist)
            q4_tomb_last_progress_log_at = now
        return True
    if now - q4_tomb_last_progress_at < PATH_STUCK_SECONDS:
        return True
    return False

def is_in_jangan_map():
    region = current_region()
    in_jangan = JANGAN_REGION_MIN <= region <= JANGAN_REGION_MAX
    zlog("JANGAN MAP CHECK -> REGION=%d IN_JANGAN=%s" % (region, str(in_jangan)))
    return in_jangan

def go_exorcist_or_return_scroll(label):
    if is_in_jangan_map():
        zlog("%s -> ja esta no mapa de Jangan; path automatico para Exorcist." % label)
        go_exorcist(None)
        return
    command = selected_return_scroll_command()
    zlog("%s -> fora do mapa de Jangan; usando %s antes do path." % (label, command))
    use_return_scroll(STATE_Q6_WAIT_TOWN, label, Q6_TOWN_CHECK_DELAY, command)

def find_npc_by_name(npc_name):
    try:
        npcs = get_npcs()
        if not npcs:
            return None, None
        for uid, npc in npcs.items():
            if str(npc.get("name", "")) == npc_name:
                return uid, npc
    except Exception as ex:
        zlog("get_npcs ERRO: %s" % str(ex))
    return None, None

def find_general():
    return find_npc_by_name(GENERAL_NAME)

def is_current_inventory_npc_visible():
    qdef = current_quest()
    if not qdef:
        return False
    npc_name = qdef.get("npc", "")
    uid, npc = find_npc_by_name(npc_name)
    return uid is not None

def remember_dialog_npc(npc_name, uid):
    global last_dialog_npc_uid, last_dialog_npc_name
    last_dialog_npc_uid = int(uid)
    last_dialog_npc_name = str(npc_name)

def select_npc(npc_name, label="SELECT NPC"):
    uid, npc = find_npc_by_name(npc_name)
    if uid is None:
        zlog("%s nao encontrado para SELECT." % npc_name)
        return False
    try:
        data = struct.pack("<I", int(uid))
        inject_joymax(0x7045, data, False)
        remember_dialog_npc(npc_name, uid)
        zlog("%s 0x7045 | NPC=%s | UID=%s | DATA=%s" %
             (label, npc_name, uid, binascii.hexlify(data).decode("ascii").upper()))
        return True
    except Exception as ex:
        zlog("%s ERRO: %s" % (label, str(ex)))
        return False

def open_npc(npc_name, label="OPEN NPC"):
    uid, npc = find_npc_by_name(npc_name)
    if uid is None:
        zlog("%s nao encontrado para OPEN." % npc_name)
        return False
    try:
        data = struct.pack("<IB", int(uid), 0x02)
        inject_joymax(0x7046, data, False)
        remember_dialog_npc(npc_name, uid)
        zlog("%s 0x7046 | NPC=%s | UID=%s | DATA=%s" %
             (label, npc_name, uid, binascii.hexlify(data).decode("ascii").upper()))
        return True
    except Exception as ex:
        zlog("%s ERRO: %s" % (label, str(ex)))
        return False

def select_general():
    return select_npc(GENERAL_NAME, "SELECT")

def open_general():
    return open_npc(GENERAL_NAME, "OPEN")

def find_current_active_quest():
    qdef = current_quest()
    if not qdef:
        return None, None
    names = quest_names(qdef)
    servernames = quest_servernames(qdef)
    try:
        quests = get_quests()
        if not quests:
            return None, None
        for qid, q in quests.items():
            name = str(q.get("name", ""))
            servername = str(q.get("servername", ""))
            if servername in servernames or name in names:
                return qid, q
    except Exception as ex:
        zlog("get_quests ERRO: %s" % str(ex))
    return None, None

def sync_current_quest_index():
    global current_quest_index
    try:
        quests = get_quests()
        if not quests:
            return False

        for qid, active in quests.items():
            active_name = str(active.get("name", ""))
            active_servername = str(active.get("servername", ""))
            for i, qdef in enumerate(current_quest_list()):
                if active_servername in quest_servernames(qdef) or active_name in quest_names(qdef):
                    if current_quest_index != i:
                        current_quest_index = i
                        zlog("SYNC QUEST -> order=%d | ID=%s | NAME=%s | SERVERNAME=%s" %
                             (qdef["order"], qid, active.get("name"), active.get("servername")))
                        log_chain()
                    return True
    except Exception as ex:
        zlog("SYNC QUEST ERRO: %s" % str(ex))
    return False

def quest_status():
    qid, q = find_current_active_quest()
    if q is None:
        return "NOT_FOUND"
    if bool(q.get("completed", False)):
        return "COMPLETED"
    if bool(q.get("objectives_completed", False)):
        return "OBJECTIVES_COMPLETED"
    return "ACTIVE"

def accept_current_quest():
    global post_accept_ok_sent
    qdef = current_quest()
    if not qdef:
        return False
    post_accept_ok_sent = False
    npc_name = qdef.get("npc", GENERAL_NAME)
    quest_name = current_accept_quest_name()
    if not quest_name:
        zlog("QUEST CMD ERRO: nome da quest vazio.")
        return False
    cmd = "quest,%s,%s" % (npc_name, quest_name)
    zlog("QUEST CMD -> " + cmd)
    try:
        start_script(cmd + "\n")
        return True
    except Exception as ex:
        zlog("QUEST CMD ERRO: %s" % str(ex))
        return False

def handin_current_quest():
    qdef = current_quest()
    if not qdef:
        return False
    npc_name = qdef.get("turnin_npc", qdef.get("npc", GENERAL_NAME))
    cmd = "quest,%s,%s" % (npc_name, qdef["name"])
    zlog("QUEST ENTREGA CMD -> " + cmd)
    try:
        start_script(cmd + "\n")
        return True
    except Exception as ex:
        zlog("QUEST ENTREGA CMD ERRO: %s" % str(ex))
        return False

def send_quest_reward():
    qdef = current_quest()
    if not qdef:
        return False
    try:
        qid, active = find_current_active_quest()
        if qid is None:
            qid = int(qdef.get("id", 0))
        if int(qid) <= 0:
            zlog("REWARD ERRO: QUEST_ID nao encontrado para %s." % qdef["name"])
            return False
        data = struct.pack("<IB", int(qid), 0x00)
        inject_joymax(0x7515, data, False)
        zlog("REWARD 0x7515 | QUEST_ID=%s | DATA=%s" %
             (qid, binascii.hexlify(data).decode("ascii").upper()))
        return True
    except Exception as ex:
        zlog("REWARD ERRO: %s" % str(ex))
        return False

def confirm_accept_ok():
    try:
        data = struct.pack("<B", CONFIRM_OK_VALUE)
        inject_joymax(CONFIRM_OK_OPCODE, data, False)
        zlog("CONFIRM OK 0x%04X | DATA=%s" %
             (CONFIRM_OK_OPCODE, binascii.hexlify(data).decode("ascii").upper()))
        return True
    except Exception as ex:
        zlog("CONFIRM OK ERRO: %s" % str(ex))
        return False

def send_dialog_choice(value, label):
    try:
        data = struct.pack("<B", int(value))
        inject_joymax(0x30D4, data, False)
        zlog("%s 0x30D4 | DATA=%s" %
             (label, binascii.hexlify(data).decode("ascii").upper()))
        return True
    except Exception as ex:
        zlog("%s ERRO: %s" % (label, str(ex)))
        return False

def send_arena_confirm():
    try:
        data = b""
        inject_joymax(0x34B6, data, False)
        zlog("ARENA CONFIRM 0x34B6 | DATA=")
        return True
    except Exception as ex:
        zlog("ARENA CONFIRM ERRO: %s" % str(ex))
        return False

def close_npc_dialog(npc_name):
    if last_dialog_npc_uid is not None:
        zlog("CLOSE NPC usando UID salvo da janela | NPC esperado=%s | ultimo=%s | UID=%s" %
             (npc_name, last_dialog_npc_name, last_dialog_npc_uid))
        return close_npc_dialog_uid(last_dialog_npc_uid)
    uid, npc = find_npc_by_name(npc_name)
    if uid is None:
        if last_dialog_npc_uid is None:
            zlog("CLOSE NPC falhou: %s nao encontrado e sem UID salvo." % npc_name)
            return False
        uid = last_dialog_npc_uid
        zlog("CLOSE NPC fallback UID salvo | NPC esperado=%s | ultimo=%s | UID=%s" %
             (npc_name, last_dialog_npc_name, uid))
    return close_npc_dialog_uid(uid)

def close_npc_dialog_uid(uid):
    try:
        data = struct.pack("<I", int(uid))
        inject_joymax(0x704B, data, False)
        zlog("CLOSE NPC 0x704B | UID=%s | DATA=%s" %
             (uid, binascii.hexlify(data).decode("ascii").upper()))
        return True
    except Exception as ex:
        zlog("CLOSE NPC ERRO: %s" % str(ex))
        return False

def close_current_quest_dialog():
    qdef = current_quest()
    npc_name = GENERAL_NAME
    if qdef:
        npc_name = qdef.get("turnin_npc", qdef.get("npc", GENERAL_NAME))
    return close_npc_dialog(npc_name)

def begin_auto_arena_entry(delay=0.0):
    global arena_entry_attempts
    arena_entry_attempts += 1
    zlog("ENTRADA ARENA AUTO -> tentativa %d/%d" %
         (arena_entry_attempts, MAX_ARENA_ENTRY_ATTEMPTS))
    set_state(STATE_ARENA_QUEST_OPTION, delay)

def after_quest_active(qid, active):
    global quest_accept_name_index
    qdef = current_quest()
    quest_accept_name_index = 0
    zlog("QUEST ATIVA | ID=%s | NAME=%s | SERVERNAME=%s" %
         (qid, active.get("name"), active.get("servername")))
    stop_script()
    if active_chain == "inventory":
        if qdef:
            zlog("INVENTORY Q%d ATIVA -> indo para area de mob." % int(qdef["order"]))
            start_inventory_path("MOB", "Inventory Q%d -> area de mob." % int(qdef["order"]))
        else:
            set_state(STATE_DONE)
        return
    if qdef and qdef["order"] == 1:
        set_state(STATE_SELECT_2, DELAY_BEFORE_SECOND_DIALOG)
    elif qdef and qdef["order"] == 2:
        zlog("Q2 ATIVA -> indo para Exorcist Miaoryeong.")
        go_exorcist()
    elif qdef and qdef["order"] == 3:
        zlog("Q3 ATIVA -> indo para Jangan Cave B2.")
        go_q3_dungeon()
    elif qdef and qdef["order"] == 4:
        zlog("Q4 ATIVA -> indo para Tombstone usar Spirit's Bell.")
        go_q4_tomb()
    elif qdef and qdef["order"] == 5:
        zlog("Q5 ATIVA -> indo para Hunter Associate Gwakwi.")
        go_hunter("Exorcist > Hunter Associate Gwakwi para entregar Q5.")
    elif qdef and qdef["order"] == 6:
        zlog("Q6 ATIVA -> traps recebidas; fechando Hunter e parando para captura manual.")
        close_npc_dialog(HUNTER_NAME)
        stop_for_q6_manual_capture("Hunter Associate Gwakwi")
    elif qdef and qdef["order"] == 7:
        zlog("Q7 ATIVA -> fechar Exorcist e avisar zerk manual.")
        close_npc_dialog(EXORCIST_NAME)
        stop_for_q7_manual_zerk("Exorcist Miaoryeong")
    elif qdef and qdef["order"] == 8:
        zlog("Q8 ATIVA -> indo para General Sonhyeon entregar New Power.")
        go_general(STATE_GO_GENERAL, "PATH -> General Sonhyeon para entregar Q8")
    else:
        set_state(STATE_DONE)

def packet_hex(data):
    try:
        if not data:
            return ""
        return binascii.hexlify(bytes(data)).decode("ascii").upper()
    except:
        return "<HEX_ERROR>"

def capture_on():
    global capture_client
    capture_client = True
    zlog("CAPTURE ON")
    zlog("FALLBACK MANUAL/DIAGNOSTICO: clique na opcao da quest/arena e confirme a entrada.")

def capture_off():
    global capture_client
    if capture_client:
        capture_client = False
        zlog("CAPTURE OFF")

def show_client_notice(text):
    sent = False
    try:
        if phBotChat:
            fn = getattr(phBotChat, "ClientNotice", None)
            if callable(fn):
                sent = bool(fn(text))
                if sent:
                    zlog("CLIENT NOTICE enviado.")
                    return True
    except Exception as ex:
        zlog("CLIENT NOTICE ERRO: %s" % str(ex))

    try:
        fn = globals().get("show_notification", None)
        if callable(fn):
            sent = bool(fn("ZERK QUEST", text))
            if sent:
                zlog("PHBOT NOTIFICATION enviada.")
                return True
    except Exception as ex:
        zlog("PHBOT NOTIFICATION ERRO: %s" % str(ex))

    try:
        ctypes.windll.user32.MessageBoxW(0, text, "ZERK QUEST", 0x40 | 0x1000)
        zlog("WINDOWS POPUP enviado.")
        return True
    except Exception as ex:
        zlog("WINDOWS POPUP ERRO: %s" % str(ex))

    return False

def guard_start_quest(order):
    order = int(order)
    done_orders = completed_orders()
    active_order, active_status = active_chain_status()
    if order in done_orders or (active_order > 0 and order < active_order):
        msg = "Q%d already finished on this character." % order
        zlog("START Q%d BLOQUEADO -> ja finalizada neste personagem." % order)
        show_client_notice(msg)
        refresh_status_ui()
        return False
    if active_order > 0:
        next_available = active_order
    elif done_orders:
        next_available = max(done_orders) + 1
    else:
        next_available = 1
    if order > next_available:
        msg = "Q%d is locked. Complete previous quests first." % order
        zlog("START Q%d BLOQUEADO -> etapa futura/locked; proxima=%d." %
             (order, next_available))
        show_client_notice(msg)
        refresh_status_ui()
        return False
    return True

def stop_for_q6_manual_capture(source):
    stop_script()
    stop_bot()
    capture_on()
    zlog("========================================")
    zlog("Q6 MANUAL CAPTURE | %s" % source)
    zlog("DO THIS PART MANUALLY.")
    zlog("Use the traps and collect the spirit. The script stopped here on purpose.")
    zlog("After collecting the spirit, press QUEST 6 again to resume and finish automatically.")
    zlog("========================================")
    show_client_notice(Q6_MANUAL_CAPTURE_MESSAGE)
    set_state(STATE_DONE)

def stop_for_q7_manual_zerk(source):
    stop_script()
    stop_bot()
    capture_on()
    zlog("========================================")
    zlog("Q7 MANUAL ZERK | %s" % source)
    zlog(Q7_MANUAL_ZERK_MESSAGE)
    zlog("Do not let the bot kill this target without zerk active.")
    zlog("After the quest is complete, use RESUME or START Q7 to deliver it.")
    zlog("========================================")
    show_client_notice(Q7_MANUAL_ZERK_MESSAGE)
    set_state(STATE_DONE)

def pre_path_nudge(label):
    try:
        p = get_position()
        if not p:
            zlog("%s PRE-PATH NUDGE ignorado: posicao vazia." % label)
            return False
        x = float(p["x"]) + AUTO_PATH_NUDGE
        y = float(p["y"]) + AUTO_PATH_NUDGE
        z = float(p.get("z", 0.0))
        move_to(x, y, z)
        zlog("%s PRE-PATH NUDGE -> +%.1f X / +%.1f Y" %
             (label, AUTO_PATH_NUDGE, AUTO_PATH_NUDGE))
        return True
    except Exception as ex:
        zlog("%s PRE-PATH NUDGE ERRO: %s" % (label, str(ex)))
        return False

def remember_path_origin(label):
    try:
        p = get_position()
        if not p:
            zlog("%s PATH ORIGIN vazio." % label)
            return None
        origin = {
            "region": int(p.get("region", 0)),
            "x": float(p["x"]),
            "y": float(p["y"]),
            "z": float(p.get("z", 0.0)),
        }
        zlog("%s PATH ORIGIN -> REGION=%d X=%.1f Y=%.1f Z=%.1f" %
             (label, origin["region"], origin["x"], origin["y"], origin["z"]))
        return origin
    except Exception as ex:
        zlog("%s PATH ORIGIN ERRO: %s" % (label, str(ex)))
        return None

def return_to_path_origin(label, origin):
    try:
        if not origin:
            zlog("%s PATH RETRY sem origin; nao tem posicao para voltar." % label)
            return False
        move_to(origin["x"], origin["y"], origin["z"])
        zlog("%s PATH RETRY -> voltando para origin X=%.1f Y=%.1f" %
             (label, origin["x"], origin["y"]))
        return True
    except Exception as ex:
        zlog("%s PATH RETRY VOLTA ERRO: %s" % (label, str(ex)))
        return False

def go_general(next_state=STATE_GO_GENERAL, reason="PATH -> General Sonhyeon", reset_retry=True):
    global general_path_started_at, general_path_retries, general_path_origin
    global general_retry_next_state, general_retry_reason
    stop_bot()
    stop_script()
    if reset_retry:
        general_path_retries = 0
        general_path_origin = remember_path_origin("GENERAL")
        general_retry_next_state = next_state
        general_retry_reason = reason
    general_path_started_at = time.time()
    cmd = "path,%d,%d,%d,%d" % (GENERAL_REGION, int(GENERAL_X), int(GENERAL_Y), int(GENERAL_Z))
    zlog(reason)
    try:
        pre_path_nudge("GENERAL")
        zlog(cmd)
        start_script(cmd + "\n")
        set_state(next_state)
    except Exception as ex:
        zlog("PATH ERRO: %s" % str(ex))
        set_state(STATE_IDLE)

def build_walk_script(points):
    lines = []
    for point in points:
        if isinstance(point, str):
            line = point.strip()
            if line:
                lines.append(line)
            continue
        if len(point) == 4:
            region, x, y, z = point
            lines.append("walk,%d,%d,%d,%d" % (int(region), int(x), int(y), int(z)))
            continue
        x, y, z = point
        lines.append("walk,%d,%d,%d" % (int(x), int(y), int(z)))
    return "\n".join(lines) + "\n"

def should_find_automatic_path():
    try:
        return bool(QtBind.isChecked(gui, cbxFindAutomaticPath))
    except:
        return True

def should_auto_fix_quest_mob():
    try:
        return bool(QtBind.isChecked(gui, cbxAutoFixQuestMob))
    except:
        return True

def should_beep_on_complete():
    try:
        return bool(QtBind.isChecked(gui, cbxSoundDone))
    except:
        return True

def selected_return_scroll_command():
    try:
        if QtBind.isChecked(gui, cbxReturnInstant):
            return RETURN_SCROLL_INSTANT_COMMAND
    except:
        pass
    try:
        if QtBind.isChecked(gui, cbxReturnSpecial):
            return RETURN_SCROLL_SPECIAL_COMMAND
    except:
        pass
    try:
        if QtBind.isChecked(gui, cbxReturnNormal):
            return RETURN_SCROLL_NORMAL_COMMAND
    except:
        pass
    return RETURN_SCROLL_SPECIAL_COMMAND

def selected_return_scroll_commands():
    selected = []
    try:
        if QtBind.isChecked(gui, cbxReturnInstant):
            selected.append(RETURN_SCROLL_INSTANT_COMMAND)
    except:
        pass
    try:
        if QtBind.isChecked(gui, cbxReturnSpecial):
            selected.append(RETURN_SCROLL_SPECIAL_COMMAND)
    except:
        pass
    try:
        if QtBind.isChecked(gui, cbxReturnNormal):
            selected.append(RETURN_SCROLL_NORMAL_COMMAND)
    except:
        pass

    fallback = [
        RETURN_SCROLL_SPECIAL_COMMAND,
        RETURN_SCROLL_NORMAL_COMMAND,
        RETURN_SCROLL_INSTANT_COMMAND
    ]
    for command in fallback:
        if command not in selected:
            selected.append(command)
    return selected

def should_inventory_reverse_wind():
    try:
        return bool(QtBind.isChecked(gui, cbxInventoryReverseWind))
    except:
        return False

def start_inventory_reverse_wind(next_kind="NPC"):
    global inventory_reverse_next_kind
    inventory_reverse_next_kind = next_kind
    zlog("Inventory Q4 -> using Reverse Scroll: Wind Town before %s path." % next_kind)
    set_state(STATE_INVENTORY_REVERSE_WIND, 0.50)

def should_use_inventory_q4_reverse_to_npc():
    if not should_inventory_reverse_wind() or is_current_inventory_npc_visible():
        return False
    target = inventory_target_pos("NPC")
    if not target:
        return False
    dist = get_distance_to(target[1], target[2])
    return dist > INVENTORY_NPC_ARRIVAL_DISTANCE

def inventory_target_pos(kind):
    qdef = current_quest()
    if not qdef:
        return None
    if kind == "MOB":
        return qdef.get("mob_area")
    return qdef.get("npc_pos")

def start_inventory_path(kind, reason, reset_retry=True):
    global inventory_path_started_at, inventory_path_retries, inventory_target, inventory_target_kind
    global inventory_last_distance, inventory_last_progress_at, inventory_last_progress_log_at
    stop_bot()
    stop_script()
    target = inventory_target_pos(kind)
    if not target:
        zlog("INVENTORY PATH ERRO: destino ausente para %s." % kind)
        set_state(STATE_IDLE)
        return
    region, x, y, z = target
    if reset_retry:
        inventory_path_retries = 0
    inventory_target = target
    inventory_target_kind = kind
    inventory_path_started_at = time.time()
    inventory_last_distance = get_distance_to(x, y)
    inventory_last_progress_at = time.time()
    inventory_last_progress_log_at = 0.0
    cmd = "path,%d,%d,%d,%d" % (int(region), int(x), int(y), int(z))
    zlog(reason)
    try:
        pre_path_nudge("INVENTORY %s" % kind)
        zlog(cmd)
        start_script(cmd + "\n")
        if kind == "MOB":
            set_state(STATE_INVENTORY_GO_MOB)
        else:
            set_state(STATE_INVENTORY_GO_NPC)
    except Exception as ex:
        zlog("INVENTORY PATH ERRO: %s" % str(ex))
        set_state(STATE_IDLE)

def retry_inventory_path():
    global inventory_path_retries
    stop_script()
    inventory_path_retries += 1
    zlog("INVENTORY PATH travou; recalculando do ponto atual (%d/%d)." %
         (inventory_path_retries, AUTO_PATH_MAX_RETRIES))
    start_inventory_path(inventory_target_kind or "NPC", "INVENTORY retry path.", False)

def inventory_path_progress_watchdog(retry_fn, retries, max_retries):
    """Recalcula a rota quando o personagem deixa de se aproximar do destino."""
    global inventory_last_distance, inventory_last_progress_at, inventory_last_progress_log_at
    if not inventory_target or inventory_path_started_at <= 0.0:
        return False
    if time.time() - inventory_path_started_at < PATH_START_GRACE_SECONDS:
        return False

    target = inventory_target
    distance = get_distance_to(target[1], target[2])
    now = time.time()
    if distance + INVENTORY_PATH_PROGRESS_EPSILON < inventory_last_distance:
        inventory_last_distance = distance
        inventory_last_progress_at = now
        if now - inventory_last_progress_log_at >= 8.0:
            zlog("INVENTORY PATH PROGRESS -> destino %.1f m" % distance)
            inventory_last_progress_log_at = now
        return False

    if now - inventory_last_progress_at < INVENTORY_PATH_STUCK_SECONDS:
        return False
    if retries >= max_retries:
        return False

    zlog("INVENTORY PATH WATCHDOG -> distancia nao diminui ha %.1fs; recalculando." %
         (now - inventory_last_progress_at))
    inventory_last_progress_at = now
    retry_fn()
    return True

def start_inventory_training():
    qdef = current_quest()
    label = "INV Q%d" % int(qdef["order"]) if qdef else "INV"
    radius = float(qdef.get("train_radius", INVENTORY_TRAIN_RADIUS)) if qdef else INVENTORY_TRAIN_RADIUS
    pick_radius = float(qdef.get("pick_radius", INVENTORY_PICK_RADIUS)) if qdef else INVENTORY_PICK_RADIUS
    start_training_here(label, radius, STATE_INVENTORY_TRAIN,
                        INVENTORY_TRAIN_CHECK_DELAY, pick_radius)

def route_inventory_step(source):
    sync_current_quest_index()
    qdef = current_quest()
    if not qdef:
        zlog("%s -> Inventory chain concluida ou quest nao configurada." % source)
        set_state(STATE_DONE)
        return
    status = quest_status()
    zlog("%s INVENTORY CHECK -> Q%d %s | STATUS=%s" %
         (source, qdef["order"], qdef["name"], status))
    if status in ("COMPLETED", "OBJECTIVES_COMPLETED"):
        start_inventory_path("NPC", "Inventory Q%d completa -> voltar ao NPC para entregar." % int(qdef["order"]))
        return
    if status == "ACTIVE":
        start_inventory_path("MOB", "Inventory Q%d ativa -> ir para area de mob." % int(qdef["order"]))
        return
    if int(qdef["order"]) == 4 and should_use_inventory_q4_reverse_to_npc():
        start_inventory_reverse_wind("NPC")
        return
    start_inventory_path("NPC", "Inventory Q%d nao ativa -> ir ao NPC para aceitar." % int(qdef["order"]))

def start_inventory_order(order):
    global current_quest_index, death_seen, success_seen, confirm_ok_attempts, arena_started_at
    global arena_entry_attempts, handin_reward_retry_count, quest_accept_name_index, post_accept_ok_sent
    set_active_chain_for_status("inventory")
    if not guard_start_quest(order):
        return
    current_quest_index = int(order) - 1
    death_seen = False
    success_seen = False
    confirm_ok_attempts = 0
    arena_started_at = 0.0
    arena_entry_attempts = 0
    handin_reward_retry_count = 0
    quest_accept_name_index = 0
    post_accept_ok_sent = False
    capture_off()
    zlog("========================================")
    zlog("INVENTORY EXPANSION v%s" % pVersion)
    zlog("START INVENTORY Q%d" % int(order))
    qdef = current_quest()
    radius = float(qdef.get("train_radius", INVENTORY_TRAIN_RADIUS)) if qdef else INVENTORY_TRAIN_RADIUS
    pick_radius = float(qdef.get("pick_radius", INVENTORY_PICK_RADIUS)) if qdef else INVENTORY_PICK_RADIUS
    zlog("Training area will be set to radius %.0f / pick %.0f." %
         (radius, pick_radius))
    zlog("========================================")
    run_auto_quest_mob_fix("INVENTORY START Q%d" % int(order))
    log_chain()
    route_inventory_step("START INVENTORY Q%d" % int(order))

def btnStartInvQ1():
    start_inventory_order(1)

def btnStartInvQ2():
    start_inventory_order(2)

def btnStartInvQ3():
    start_inventory_order(3)

def btnStartInvQ4():
    start_inventory_order(4)

def selected_quest_order(widget, quests, chain_name):
    try:
        idx = QtBind.currentIndex(gui, widget)
        if idx is None:
            idx = -1
        idx = int(idx)
    except:
        idx = -1
    if idx < 0 or idx >= len(quests):
        msg = "Select a quest from the %s list first." % chain_name
        zlog(msg)
        show_client_notice(msg)
        return 0
    try:
        return int(quests[idx]["order"])
    except:
        return 0

def btnStartSelectedInventory():
    order = selected_quest_order(lstInventoryQuestStatus, INVENTORY_QUESTS, "Inventory Expansion")
    if order > 0:
        start_inventory_order(order)

def btnStartSelectedZerk105():
    global current_quest_index
    set_active_chain_for_status("zerk105")
    order = selected_quest_order(lstZerk105QuestStatus, ZERK_105_QUESTS, "Zerk 105")
    if order <= 0:
        return
    current_quest_index = order - 1
    qdef = current_quest()
    zlog("========================================")
    zlog("ZERK 105 MAPPED STEP")
    zlog("Q%d -> %s | %s" % (order, qdef.get("name", ""), qdef.get("servername", "")))
    zlog("NPC -> %s | %s" % (qdef.get("npc", ""), str(qdef.get("npc_pos", ""))))
    for mob in qdef.get("mob_areas", []):
        zlog("MOB -> %s | %s" % (mob.get("name", ""), str(mob.get("pos", ""))))
    if bool(qdef.get("manual", False)):
        show_client_notice("Zerk 105 Q%d is mapped as manual for now. Use the list as a guide." % order)
    else:
        show_client_notice("Zerk 105 Q%d is mapped only. Automation will be added after validation." % order)
    zlog("========================================")
    refresh_status_ui()

def btnResumeInventory():
    global current_quest_index, handin_reward_retry_count, quest_accept_name_index, post_accept_ok_sent
    set_active_chain_for_status("inventory")
    active_order, active_status = active_chain_status()
    if active_order > 0:
        current_quest_index = active_order - 1
    else:
        done_orders = completed_orders()
        current_quest_index = max(done_orders) if done_orders else 0
    handin_reward_retry_count = 0
    quest_accept_name_index = 0
    post_accept_ok_sent = False
    capture_off()
    zlog("========================================")
    zlog("INVENTORY RESUME / VALIDATOR")
    zlog("========================================")
    run_auto_quest_mob_fix("INVENTORY RESUME")
    route_inventory_step("INVENTORY RESUME")

def play_done_beep(label="QUEST"):
    if not should_beep_on_complete():
        return
    try:
        wav_path = os.path.join(PLUGIN_DIR, "bip.wav")
        if winsound and os.path.isfile(wav_path):
            winsound.PlaySound(wav_path, winsound.SND_FILENAME | winsound.SND_ASYNC)
            zlog("%s COMPLETE SOUND -> %s" % (label, wav_path))
        else:
            ctypes.windll.user32.MessageBeep(0xFFFFFFFF)
            zlog("%s COMPLETE BEEP." % label)
    except Exception as ex:
        zlog("%s BEEP ERRO: %s" % (label, str(ex)))

def start_exorcist_manual_route(route_key="GENERAL_TO_EXORCIST"):
    global exorcist_route_mode, exorcist_route_fallback, exorcist_path_started_at, exorcist_path_retries
    route = ROUTES[route_key]
    script = build_walk_script(route)
    exorcist_route_mode = "MANUAL"
    exorcist_route_fallback = None
    exorcist_path_started_at = time.time()
    exorcist_path_retries = 0
    zlog("Q2 -> rota manual %s" % route_key)
    zlog("ROTA EXORCIST -> %d passos | destino=%d,%d" %
         (len(route), int(EXORCIST_X), int(EXORCIST_Y)))
    try:
        start_script(script)
        set_state(STATE_GO_EXORCIST)
    except Exception as ex:
        zlog("ROTA EXORCIST ERRO: %s" % str(ex))
        set_state(STATE_IDLE)

def start_exorcist_auto_path(reason, fallback_route_key=None, reset_retry=True):
    global exorcist_route_mode, exorcist_route_fallback, exorcist_path_started_at
    global exorcist_path_retries, exorcist_path_origin
    exorcist_route_mode = "AUTO"
    exorcist_route_fallback = fallback_route_key
    if reset_retry:
        exorcist_path_retries = 0
        exorcist_path_origin = remember_path_origin("EXORCIST")
    exorcist_path_started_at = time.time()
    cmd = "path,%d,%d,%d,%d" % (EXORCIST_REGION, int(EXORCIST_X), int(EXORCIST_Y), int(EXORCIST_Z))
    zlog(reason)
    try:
        pre_path_nudge("EXORCIST")
        zlog(cmd)
        start_script(cmd + "\n")
        set_state(STATE_GO_EXORCIST)
    except Exception as ex:
        zlog("PATH EXORCIST ERRO: %s" % str(ex))
        if fallback_route_key:
            start_exorcist_manual_route(fallback_route_key)
        else:
            set_state(STATE_IDLE)

def start_buddha_auto_path(reason, reset_retry=True):
    global buddha_path_started_at, buddha_path_retries, buddha_path_origin, buddha_retry_reason
    if reset_retry:
        buddha_path_retries = 0
        buddha_path_origin = remember_path_origin("BUDDHA")
        buddha_retry_reason = reason
    buddha_path_started_at = time.time()
    cmd = "path,%d,%d,%d,%d" % (BUDDHA_REGION, int(BUDDHA_X), int(BUDDHA_Y), int(BUDDHA_Z))
    zlog(reason)
    try:
        pre_path_nudge("BUDDHA")
        zlog(cmd)
        start_script(cmd + "\n")
        set_state(STATE_GO_BUDDHA)
    except Exception as ex:
        zlog("PATH BUDDHA ERRO: %s" % str(ex))
        set_state(STATE_IDLE)

def start_hunter_auto_path(reason, reset_retry=True):
    global hunter_path_started_at, hunter_path_retries, hunter_path_origin, hunter_retry_reason
    if reset_retry:
        hunter_path_retries = 0
        hunter_path_origin = remember_path_origin("HUNTER")
        hunter_retry_reason = reason
    hunter_path_started_at = time.time()
    cmd = "path,%d,%d,%d,%d" % (HUNTER_REGION, int(HUNTER_X), int(HUNTER_Y), int(HUNTER_Z))
    zlog(reason)
    try:
        pre_path_nudge("HUNTER")
        zlog(cmd)
        start_script(cmd + "\n")
        set_state(STATE_GO_HUNTER)
    except Exception as ex:
        zlog("PATH HUNTER ERRO: %s" % str(ex))
        set_state(STATE_IDLE)

def go_buddha(reason="Indo para Buddhist Priest Jeonghye por path automatico."):
    stop_bot()
    stop_script()
    dist = get_distance_to(BUDDHA_X, BUDDHA_Y)
    if dist <= BUDDHA_ARRIVAL_DISTANCE:
        zlog("Ja esta perto do Buddhist Priest Jeonghye | distancia=%.1f" % dist)
        set_state(STATE_GO_BUDDHA, 0.25)
        return
    start_buddha_auto_path(reason)

def go_hunter(reason="Indo para Hunter Associate Gwakwi por path automatico."):
    stop_bot()
    stop_script()
    dist = get_distance_to(HUNTER_X, HUNTER_Y)
    if dist <= HUNTER_ARRIVAL_DISTANCE:
        zlog("Ja esta perto do Hunter Associate Gwakwi | distancia=%.1f" % dist)
        set_state(STATE_GO_HUNTER, 0.25)
        return
    start_hunter_auto_path(reason)

def go_exorcist(fallback_route_key="GENERAL_TO_EXORCIST"):
    stop_bot()
    stop_script()
    qdef = current_quest()
    if qdef and qdef.get("order") in (6, 7) and quest_status() in ("COMPLETED", "OBJECTIVES_COMPLETED"):
        if not is_in_jangan_map():
            command = selected_return_scroll_command()
            zlog("EXORCIST PATH bloqueado: Q%d completa fora de Jangan; usando %s primeiro." %
                 (qdef["order"], command))
            use_return_scroll(STATE_Q6_WAIT_TOWN, "Q%d completa" % qdef["order"], Q6_TOWN_CHECK_DELAY, command)
            return

    dist = get_distance_to(EXORCIST_X, EXORCIST_Y)
    if dist <= EXORCIST_ARRIVAL_DISTANCE:
        zlog("Ja esta perto da Exorcist Miaoryeong | distancia=%.1f" % dist)
        set_state(STATE_GO_EXORCIST, 0.25)
        return

    if should_find_automatic_path():
        start_exorcist_auto_path("Indo para Exorcist Miaoryeong por path automatico.", fallback_route_key)
        return

    if fallback_route_key:
        start_exorcist_manual_route(fallback_route_key)
    else:
        start_exorcist_auto_path("Indo para Exorcist Miaoryeong por path automatico.", None)

def go_q3_dungeon():
    stop_bot()
    stop_script()
    route = ROUTES["EXORCIST_TO_B2_STONE_BEAST"]
    script = build_walk_script(route)
    zlog("Q3 -> rota Exorcist > Jangan Cave B2 | Stone Beast's Bell")
    zlog("ROTA Q3 B2 -> %d comandos; waits preservados para troca de fase." % len(route))
    try:
        start_script(script)
        set_state(STATE_GO_Q3_DUNGEON)
    except Exception as ex:
        zlog("ROTA Q3 B2 ERRO: %s" % str(ex))
        set_state(STATE_IDLE)

def go_q4_tomb(reset_retry=True):
    global q4_tomb_path_started_at, q4_tomb_path_retries, q4_tomb_path_origin, q4_tomb_prefix_started_at
    stop_bot()
    stop_script()
    if reset_retry:
        q4_tomb_path_retries = 0
        q4_tomb_path_origin = remember_path_origin("Q4 TOMB")
    q4_tomb_path_started_at = 0.0
    q4_tomb_prefix_started_at = time.time()
    prefix = ROUTES["BUDDHA_TO_Q4_PATH_START"]
    script = build_walk_script(prefix)
    zlog("Q4 -> saida manual do Buda para evitar parede/autopath.")
    zlog("Q4 -> %d walks curtos; depois confirma prefix e calcula path ate Tombstone." % len(prefix))
    try:
        start_script(script)
        set_state(STATE_Q4_TOMB_PREFIX_WAIT, Q4_PREFIX_MIN_WAIT)
    except Exception as ex:
        zlog("Q4 PREFIX ERRO: %s" % str(ex))
        set_state(STATE_IDLE)

def start_q4_tomb_auto_path():
    global q4_tomb_path_started_at, q4_tomb_last_dist, q4_tomb_last_progress_at, q4_tomb_last_progress_log_at
    stop_script()
    cmd = "path,%d,%d,%d,%d" % (Q4_TOMB_REGION, int(Q4_TOMB_X), int(Q4_TOMB_Y), int(Q4_TOMB_Z))
    q4_tomb_path_started_at = time.time()
    q4_tomb_last_dist = get_distance_to(Q4_TOMB_X, Q4_TOMB_Y)
    q4_tomb_last_progress_at = time.time()
    q4_tomb_last_progress_log_at = 0.0
    zlog("Q4 -> calculando path ate Tombstone apos prefix manual.")
    zlog("Q4 TOMB DIST INICIAL -> %.1f" % q4_tomb_last_dist)
    zlog(cmd)
    try:
        start_script(cmd + "\n")
        set_state(STATE_GO_Q4_TOMB)
    except Exception as ex:
        zlog("PATH Q4 TOMB ERRO: %s" % str(ex))
        set_state(STATE_IDLE)

def route_current_step(source):
    sync_current_quest_index()
    if active_chain == "inventory":
        route_inventory_step(source)
        return
    qdef = current_quest()
    if not qdef:
        zlog("%s -> cadeia concluida ou quest atual nao configurada." % source)
        set_state(STATE_DONE)
        return

    status = quest_status()
    zlog("%s CHECK -> Q%d %s | STATUS=%s" %
         (source, qdef["order"], qdef["name"], status))

    if qdef["order"] == 1:
        if status in ("COMPLETED", "OBJECTIVES_COMPLETED"):
            go_general(STATE_GO_HANDIN_GENERAL, "PATH -> General Sonhyeon para entregar Q1")
        elif status == "ACTIVE":
            go_general(STATE_GO_GENERAL, "PATH -> General Sonhyeon para continuar Q1")
        else:
            go_general(STATE_GO_GENERAL, "PATH -> General Sonhyeon para aceitar Q1")
        return

    if qdef["order"] == 2:
        if status in ("ACTIVE", "COMPLETED", "OBJECTIVES_COMPLETED"):
            zlog("Q2 encontrada -> destino Exorcist Miaoryeong.")
            go_exorcist()
        else:
            go_general(STATE_GO_GENERAL, "PATH -> General Sonhyeon para aceitar Q2")
        return

    if qdef["order"] == 3:
        if status in ("COMPLETED", "OBJECTIVES_COMPLETED"):
            zlog("Q3 completa -> destino Buddhist Priest Jeonghye para entrega.")
            go_buddha("Cidade/B2 > Buddhist Priest Jeonghye para entregar Q3.")
        elif status == "ACTIVE":
            if get_distance_to(BUDDHA_X, BUDDHA_Y) <= BUDDHA_ARRIVAL_DISTANCE:
                zlog("Q3 ativa e ja esta no Buda -> tentando entrega com OK + Reward.")
                set_state(STATE_GO_BUDDHA, 0.25)
            elif get_distance_to(Q3_DUNGEON_X, Q3_DUNGEON_Y) <= Q3_DUNGEON_ARRIVAL_DISTANCE:
                zlog("Q3 ativa e ja esta no ponto do B2 -> ligando treino.")
                set_state(STATE_GO_Q3_DUNGEON, 0.25)
            elif get_distance_to(EXORCIST_X, EXORCIST_Y) <= EXORCIST_ARRIVAL_DISTANCE:
                zlog("Q3 ativa e esta na Exorcist -> destino Jangan Cave B2.")
                go_q3_dungeon()
            else:
                zlog("Q3 ativa/incompleta -> indo para Exorcist antes da rota B2.")
                go_exorcist(None)
        else:
            zlog("Q3 nao ativa -> destino Exorcist Miaoryeong para aceitar.")
            if get_distance_to(EXORCIST_X, EXORCIST_Y) <= EXORCIST_ACCEPT_DISTANCE:
                zlog("Q3 perto da Exorcist -> aceitando quest diretamente.")
                set_state(STATE_ACCEPT, 0.30)
                return
            go_exorcist(None)
        return

    if qdef["order"] == 4:
        if status in ("COMPLETED", "OBJECTIVES_COMPLETED"):
            zlog("Q4 completa -> destino Exorcist Miaoryeong para entrega.")
            go_exorcist(None)
        elif status == "ACTIVE":
            if get_distance_to(Q4_TOMB_X, Q4_TOMB_Y) <= Q4_TOMB_ARRIVAL_DISTANCE:
                zlog("Q4 ativa e ja esta no local do Tombstone -> usando Spirit's Bell.")
                stop_script()
                set_state(STATE_Q4_USE_BELL, 0.25)
            elif get_distance_to(BUDDHA_X, BUDDHA_Y) <= BUDDHA_ARRIVAL_DISTANCE:
                zlog("Q4 ativa e esta no Buda -> indo para Tombstone.")
                go_q4_tomb()
            else:
                zlog("Q4 ativa/incompleta -> indo para Tombstone.")
                go_q4_tomb()
        else:
            zlog("Q4 nao ativa -> destino Buddhist Priest Jeonghye para aceitar.")
            go_buddha("Indo para Buddhist Priest Jeonghye para aceitar Q4.")
        return

    if qdef["order"] == 5:
        if status in ("ACTIVE", "COMPLETED", "OBJECTIVES_COMPLETED"):
            zlog("Q5 encontrada -> destino Hunter Associate Gwakwi para entrega.")
            go_hunter("Exorcist > Hunter Associate Gwakwi para entregar Q5.")
        else:
            zlog("Q5 nao ativa -> destino Exorcist Miaoryeong para aceitar.")
            if get_distance_to(EXORCIST_X, EXORCIST_Y) <= EXORCIST_ACCEPT_DISTANCE:
                zlog("Q5 perto da Exorcist -> aceitando Miaoryeong's Charm.")
                set_state(STATE_ACCEPT, 0.30)
                return
            go_exorcist(None)
        return

    if qdef["order"] == 6:
        if status in ("COMPLETED", "OBJECTIVES_COMPLETED"):
            zlog("Q6 completa -> entregar na Exorcist Miaoryeong.")
            go_exorcist_or_return_scroll("Q6 completa")
        elif status == "ACTIVE":
            zlog("Q6 ativa -> traps/captura manual; nao vai para Exorcist ainda.")
            if get_distance_to(HUNTER_X, HUNTER_Y) <= HUNTER_ARRIVAL_DISTANCE:
                close_npc_dialog(HUNTER_NAME)
            stop_for_q6_manual_capture("Q6 ativa")
        else:
            zlog("Q6 nao ativa -> destino Hunter Associate Gwakwi para aceitar The Spirit.")
            if get_distance_to(HUNTER_X, HUNTER_Y) <= HUNTER_ARRIVAL_DISTANCE:
                zlog("Q6 perto do Hunter -> aceitando The Spirit.")
                set_state(STATE_GO_HUNTER, 0.30)
                return
            go_hunter("Indo para Hunter Associate Gwakwi para aceitar Q6 The Spirit.")
        return

    if qdef["order"] == 7:
        if status in ("COMPLETED", "OBJECTIVES_COMPLETED"):
            zlog("Q7 completa -> entregar na Exorcist Miaoryeong.")
            go_exorcist_or_return_scroll("Q7 completa")
        elif status == "ACTIVE":
            if get_distance_to(EXORCIST_X, EXORCIST_Y) <= EXORCIST_ACCEPT_DISTANCE:
                zlog("Q7 ativa e perto da Exorcist -> parte manual com zerk.")
                stop_for_q7_manual_zerk("Q7 ativa")
            else:
                zlog("Q7 ativa, mas longe da Exorcist -> voltando antes da parte manual.")
                go_exorcist_or_return_scroll("Q7 ativa")
        else:
            zlog("Q7 nao ativa -> destino Exorcist Miaoryeong para aceitar Piece of Spirit.")
            if get_distance_to(EXORCIST_X, EXORCIST_Y) <= EXORCIST_ACCEPT_DISTANCE:
                zlog("Q7 perto da Exorcist -> aceitando Piece of Spirit.")
                set_state(STATE_ACCEPT, 0.30)
                return
            go_exorcist(None)
        return

    if qdef["order"] == 8:
        if status in ("ACTIVE", "COMPLETED", "OBJECTIVES_COMPLETED"):
            zlog("Q8 encontrada -> destino General Sonhyeon para entrega final.")
            go_general(STATE_GO_GENERAL, "PATH -> General Sonhyeon para entregar Q8")
        else:
            zlog("Q8 nao ativa -> destino Exorcist Miaoryeong para aceitar New Power.")
            if get_distance_to(EXORCIST_X, EXORCIST_Y) <= EXORCIST_ACCEPT_DISTANCE:
                zlog("Q8 perto da Exorcist -> aceitando New Power.")
                set_state(STATE_ACCEPT, 0.30)
                return
            go_exorcist(None)
        return

    if qdef.get("manual", False):
        zlog("Q%d %s marcada como MANUAL neste script." % (qdef["order"], qdef["name"]))
        zlog("Pare aqui, capture/execute manualmente e use RESUME depois se necessario.")
        capture_on()
        set_state(STATE_DONE)
        return

    zlog("Q%d ainda nao tem automacao completa neste script." % qdef["order"])
    set_state(STATE_DONE)

def set_training_pick_radius_if_available(pick_radius):
    for fn_name in ("set_training_pick_radius", "set_training_pickup_radius", "set_pick_radius"):
        fn = globals().get(fn_name, None)
        if not callable(fn):
            continue
        try:
            result = fn(float(pick_radius))
            zlog("TRAIN PICK -> %s(%.1f)=%s" % (fn_name, float(pick_radius), str(result)))
            return True
        except Exception as ex:
            zlog("TRAIN PICK ERRO %s: %s" % (fn_name, str(ex)))
    zlog("TRAIN PICK -> API indisponivel; Pick Radius fica pelo perfil/area salva.")
    return False

def start_training_here(label, radius, next_state, delay, pick_radius=None):
    stop_script()
    try:
        p = get_position()
    except:
        p = None
    if not p:
        zlog("%s TRAIN ERRO: get_position vazio." % label)
        set_state(STATE_IDLE)
        return

    try:
        ok_pos = set_training_position(p["region"], p["x"], p["y"], p["z"])
        pos_error = False
    except Exception as ex:
        ok_pos = False
        pos_error = True
        zlog("%s TRAIN ERRO set_training_position: %s" % (label, str(ex)))

    try:
        ok_radius = set_training_radius(radius)
    except Exception as ex:
        ok_radius = False
        zlog("%s TRAIN ERRO set_training_radius: %s" % (label, str(ex)))

    ok_pick = None
    if pick_radius is not None:
        ok_pick = set_training_pick_radius_if_available(pick_radius)

    try:
        ok_start = start_bot()
        start_error = False
    except Exception as ex:
        ok_start = False
        start_error = True
        zlog("%s TRAIN ERRO start_bot: %s" % (label, str(ex)))

    if pick_radius is None:
        zlog("%s TRAIN -> position=%s radius=%s start_bot=%s | R=%.1f" %
             (label, str(ok_pos), str(ok_radius), str(ok_start), radius))
    else:
        zlog("%s TRAIN -> position=%s radius=%s pick=%s start_bot=%s | R=%.1f PICK=%.1f" %
             (label, str(ok_pos), str(ok_radius), str(ok_pick), str(ok_start), radius, pick_radius))
    if not pos_error and not start_error:
        set_state(next_state, delay)
    else:
        set_state(STATE_IDLE)

def start_q1_arena_training():
    stop_script()
    try:
        p = get_position()
    except:
        p = None
    if not p:
        zlog("Q1 ARENA TRAIN ERRO: get_position vazio; aguardando TP de saida mesmo assim.")
        set_state(STATE_ARENA, Q1_ARENA_TRAIN_CHECK_DELAY)
        return

    try:
        ok_pos = set_training_position(p["region"], p["x"], p["y"], p["z"])
    except Exception as ex:
        ok_pos = False
        zlog("Q1 ARENA TRAIN ERRO set_training_position: %s" % str(ex))

    try:
        ok_radius = set_training_radius(Q1_ARENA_TRAIN_RADIUS)
    except Exception as ex:
        ok_radius = False
        zlog("Q1 ARENA TRAIN ERRO set_training_radius: %s" % str(ex))

    ok_pick = set_training_pick_radius_if_available(Q1_ARENA_PICK_RADIUS)

    try:
        ok_start = start_bot()
    except Exception as ex:
        ok_start = False
        zlog("Q1 ARENA TRAIN ERRO start_bot: %s" % str(ex))

    zlog("Q1 ARENA TRAIN -> position=%s radius=%s pick=%s start_bot=%s | R=%.1f PICK=%.1f" %
         (str(ok_pos), str(ok_radius), str(ok_pick), str(ok_start),
          Q1_ARENA_TRAIN_RADIUS, Q1_ARENA_PICK_RADIUS))
    if ok_pos and ok_start:
        zlog("ARENA ATIVA -> treino local 50/50 ligado; aguardando TP de saida para checar quest.")
    else:
        zlog("ARENA ATIVA -> treino nao confirmou; mantenha manual se necessario, ainda aguardando TP de saida.")
    set_state(STATE_ARENA, Q1_ARENA_TRAIN_CHECK_DELAY)

def start_q3_training():
    start_training_here("Q3", Q3_TRAIN_RADIUS, STATE_Q3_TRAIN, Q3_TRAIN_CHECK_DELAY)

def start_q4_training():
    start_training_here("Q4", Q4_TRAIN_RADIUS, STATE_Q4_TRAIN, Q4_TRAIN_CHECK_DELAY, Q4_PICK_RADIUS)

def get_item_field_int(data, names, default=0):
    if not data:
        return default
    for name in names:
        if name in data:
            try:
                return int(data.get(name, default) or default)
            except:
                return default
    return default

def calculate_use_item_type(model):
    try:
        item_data = get_item(int(model))
        if not item_data:
            zlog("ITEM TYPE ERRO: get_item(%s) vazio." % str(model))
            return None
        cash = get_item_field_int(item_data, ("cash_item", "cashitem", "cash", "is_cash_item"), 0)
        tid1 = get_item_field_int(item_data, ("tid1", "typeid1"), 0)
        tid2 = get_item_field_int(item_data, ("tid2", "typeid2"), 0)
        tid3 = get_item_field_int(item_data, ("tid3", "typeid3"), 0)
        tid4 = get_item_field_int(item_data, ("tid4", "typeid4"), 0)
        item_type = cash + (tid1 * 3) + (tid2 * 32) + (tid3 * 128) + (tid4 * 2048)
        zlog("ITEM TYPE -> model=%s tid=%d/%d/%d/%d cash=%d type=%d" %
             (str(model), tid1, tid2, tid3, tid4, cash, item_type))
        return item_type
    except Exception as ex:
        zlog("ITEM TYPE ERRO: %s" % str(ex))
        return None

def find_inventory_item_by_model(model, fallback_name=""):
    try:
        inv = get_inventory()
        items = (inv or {}).get("items", [])
        for slot, item in enumerate(items):
            if not item:
                continue
            item_model = int(item.get("model", 0) or 0)
            item_name = str(item.get("name", ""))
            if item_model == int(model) or (fallback_name and item_name == fallback_name):
                item["slot"] = int(item.get("slot", slot))
                return item
    except Exception as ex:
        zlog("INVENTORY ERRO: %s" % str(ex))
    return None

def use_inventory_item_by_model(model, fallback_name=""):
    item = find_inventory_item_by_model(model, fallback_name)
    if not item:
        zlog("ITEM NAO ENCONTRADO -> model=%s name=%s" % (str(model), fallback_name))
        return False

    item_type = calculate_use_item_type(item.get("model", model))
    if item_type is None:
        return False

    try:
        slot = int(item.get("slot", 0))
        data = struct.pack("<BH", slot, int(item_type))
        inject_joymax(0x704C, data, True)
        zlog("USE ITEM 0x704C | SLOT=%d MODEL=%s NAME=%s TYPE=%d DATA=%s" %
             (slot, str(item.get("model", model)), str(item.get("name", "")), int(item_type),
              binascii.hexlify(data).decode("ascii").upper()))
        return True
    except Exception as ex:
        zlog("USE ITEM 0x704C ERRO: %s" % str(ex))
    return False

def use_spirit_bell_packet():
    item = find_inventory_item_by_model(Q4_SPIRIT_BELL_ID, Q4_SPIRIT_BELL_ITEM)
    if not item:
        zlog("SPIRIT BELL NAO ENCONTRADO -> model=%d" % Q4_SPIRIT_BELL_ID)
        return False

    try:
        slot = int(item.get("slot", 0))
        data = struct.pack("<BHH", slot, Q4_SPIRIT_BELL_ITEM_TYPE, Q4_SPIRIT_BELL_USE_ARG)
        inject_joymax(0x704C, data, True)
        zlog("SPIRIT BELL 0x704C | SLOT=%d MODEL=%s TYPE=0x%04X ARG=0x%04X DATA=%s" %
             (slot, str(item.get("model", Q4_SPIRIT_BELL_ID)), Q4_SPIRIT_BELL_ITEM_TYPE,
              Q4_SPIRIT_BELL_USE_ARG, binascii.hexlify(data).decode("ascii").upper()))
        return True
    except Exception as ex:
        zlog("SPIRIT BELL 0x704C ERRO: %s" % str(ex))
        return False

def use_spirit_bell():
    stop_bot()
    stop_script()
    zlog("Q4 -> usando %s por pacote capturado." % Q4_SPIRIT_BELL_ITEM)
    if use_spirit_bell_packet():
        set_state(STATE_Q4_START_TRAIN, DELAY_AFTER_Q4_USE_BELL)
        return

    zlog("Q4 -> pacote capturado falhou; tentando uso generico por ID/model %d." % Q4_SPIRIT_BELL_ID)
    if use_inventory_item_by_model(Q4_SPIRIT_BELL_ID, Q4_SPIRIT_BELL_ITEM):
        set_state(STATE_Q4_START_TRAIN, DELAY_AFTER_Q4_USE_BELL)
        return

    cmd = "use,%s" % Q4_SPIRIT_BELL_ITEM
    zlog("Q4 -> fallback script command: %s" % cmd)
    try:
        start_script(cmd + "\n")
        set_state(STATE_Q4_START_TRAIN, DELAY_AFTER_Q4_USE_BELL)
    except Exception as ex:
        zlog("Q4 USE BELL FALLBACK ERRO: %s" % str(ex))
        capture_on()
        set_state(STATE_DONE)

def use_return_scroll(wait_state=STATE_Q3_WAIT_TOWN, label="Q3", delay=Q3_TOWN_CHECK_DELAY, command="use,returnscroll", reset_attempts=True, fixed_command=False):
    global return_scroll_attempts, return_scroll_commands, return_scroll_wait_state, return_scroll_label, return_scroll_delay
    stop_bot()
    stop_script()
    if reset_attempts:
        return_scroll_attempts = 0
        if fixed_command and command:
            return_scroll_commands = [command]
        else:
            return_scroll_commands = selected_return_scroll_commands()
            if command and command in return_scroll_commands:
                return_scroll_commands.remove(command)
                return_scroll_commands.insert(0, command)
            elif command:
                return_scroll_commands.insert(0, command)
        return_scroll_wait_state = wait_state
        return_scroll_label = label
        return_scroll_delay = delay

    if not return_scroll_commands:
        return_scroll_commands = [command or RETURN_SCROLL_SPECIAL_COMMAND]

    command = return_scroll_commands[min(return_scroll_attempts, len(return_scroll_commands) - 1)]
    return_scroll_attempts += 1
    zlog("%s -> using return scroll attempt %d/%d." %
         (label, return_scroll_attempts, RETURN_SCROLL_MAX_ATTEMPTS))
    zlog(command)
    try:
        start_script(command + "\n")
        set_state(wait_state, delay)
    except Exception as ex:
        zlog("RETURN SCROLL ERRO: %s" % str(ex))
        capture_on()
        set_state(STATE_DONE)

def retry_return_scroll_if_needed():
    if return_scroll_attempts >= RETURN_SCROLL_MAX_ATTEMPTS:
        zlog("%s -> return scroll did not teleport after %d attempts; manual action required." %
             (return_scroll_label or "RETURN", RETURN_SCROLL_MAX_ATTEMPTS))
        capture_on()
        set_state(STATE_DONE)
        return
    use_return_scroll(return_scroll_wait_state or state,
                      return_scroll_label or "RETURN",
                      RETURN_SCROLL_RETRY_DELAY,
                      None,
                      False)

def nudge_and_retry_exorcist_path():
    global exorcist_path_retries
    stop_script()
    try:
        return_to_path_origin("EXORCIST", exorcist_path_origin)
        exorcist_path_retries += 1
        zlog("PATH EXORCIST travou; voltando origin e recalculando (%d/%d)." %
             (exorcist_path_retries, EXORCIST_AUTO_PATH_MAX_RETRIES))
        set_state(STATE_EXORCIST_AUTO_RETRY, DELAY_AFTER_EXORCIST_NUDGE)
    except Exception as ex:
        zlog("NUDGE EXORCIST ERRO: %s" % str(ex))
        capture_on()
        set_state(STATE_DONE)

def retry_general_path():
    global general_path_retries
    stop_script()
    return_to_path_origin("GENERAL", general_path_origin)
    general_path_retries += 1
    zlog("PATH GENERAL travou; voltando origin e recalculando (%d/%d)." %
         (general_path_retries, AUTO_PATH_MAX_RETRIES))
    set_state(STATE_GENERAL_AUTO_RETRY, DELAY_AFTER_AUTO_PATH_NUDGE)

def retry_buddha_path():
    global buddha_path_retries
    stop_script()
    return_to_path_origin("BUDDHA", buddha_path_origin)
    buddha_path_retries += 1
    zlog("PATH BUDDHA travou; voltando origin e recalculando (%d/%d)." %
         (buddha_path_retries, AUTO_PATH_MAX_RETRIES))
    set_state(STATE_BUDDHA_AUTO_RETRY, DELAY_AFTER_AUTO_PATH_NUDGE)

def retry_hunter_path():
    global hunter_path_retries
    stop_script()
    return_to_path_origin("HUNTER", hunter_path_origin)
    hunter_path_retries += 1
    zlog("PATH HUNTER travou; voltando origin e recalculando (%d/%d)." %
         (hunter_path_retries, AUTO_PATH_MAX_RETRIES))
    set_state(STATE_HUNTER_AUTO_RETRY, DELAY_AFTER_AUTO_PATH_NUDGE)

def begin_q5_hunter_handin():
    zlog("Q5 Hunter -> fluxo capturado: SELECT NPC > OPEN > TALK 06 > REWARD.")
    set_state(STATE_Q5_HUNTER_SELECT, 0.35)

def retry_q4_tomb_path():
    global q4_tomb_path_retries
    stop_script()
    q4_tomb_path_retries += 1
    zlog("PATH Q4 TOMB travou; recalculando do ponto atual (%d/%d)." %
         (q4_tomb_path_retries, AUTO_PATH_MAX_RETRIES))
    set_state(STATE_Q4_TOMB_AUTO_RETRY, 0.80)

def distance2d(ax, ay, bx, by):
    return ((float(bx) - float(ax)) ** 2 + (float(by) - float(ay)) ** 2) ** 0.5

def path_watchdog_ready(started_at):
    return started_at > 0.0 and time.time() - started_at >= PATH_START_GRACE_SECONDS

def path_watchdog(label, retry_fn, retries, max_retries):
    global path_watch_state, path_watch_last_pos, path_watch_last_moved_at
    try:
        p = get_position()
    except:
        p = None
    if not p:
        return False

    now = time.time()
    current_pos = {
        "region": int(p.get("region", 0) or 0),
        "x": float(p.get("x", 0.0) or 0.0),
        "y": float(p.get("y", 0.0) or 0.0),
        "z": float(p.get("z", 0.0) or 0.0),
    }

    if path_watch_state != state or path_watch_last_pos is None:
        path_watch_state = state
        path_watch_last_pos = current_pos
        path_watch_last_moved_at = now
        return False

    moved = distance2d(
        path_watch_last_pos["x"],
        path_watch_last_pos["y"],
        current_pos["x"],
        current_pos["y"]
    )
    if current_pos["region"] != path_watch_last_pos["region"] or moved >= PATH_MOVE_EPSILON:
        path_watch_last_pos = current_pos
        path_watch_last_moved_at = now
        return False

    if now - path_watch_last_moved_at < PATH_STUCK_SECONDS:
        return False

    if retries >= max_retries:
        return False

    zlog("%s PATH WATCHDOG -> parado %.1fs; recalculando rota agora." %
         (label, now - path_watch_last_moved_at))
    path_watch_last_moved_at = now
    retry_fn()
    return True

def confirm_arena_entry():
    try:
        char = get_character_data()
        pos = get_position()
        if not char or not pos:
            zlog("Nao consegui ler character/position para confirmar arena.")
            return False

        region = int(char["region"])
        x = float(pos["x"])
        y = float(pos["y"])
        z = float(pos.get("z", 0.0))

        zlog("ARENA -> REGION=%d X=%.1f Y=%.1f Z=%.1f" % (region, x, y, z))

        dx = x - ARENA_X
        dy = y - ARENA_Y
        dist = (dx * dx + dy * dy) ** 0.5
        if region != ARENA_REGION or dist > ARENA_MAX_DISTANCE:
            zlog("ARENA CHECK FALHOU | esperado REGION=%d perto de %.1f,%.1f | dist=%.1f" %
                 (ARENA_REGION, ARENA_X, ARENA_Y, dist))
            return False

        zlog("ARENA CHECK OK | REGION=%d dist=%.1f <= %.1f" %
             (region, dist, ARENA_MAX_DISTANCE))
        return True

    except Exception as ex:
        zlog("ARENA CHECK ERRO: %s" % str(ex))
        return False

def apply_q4_training_area_config(config):
    changed = False
    try:
        loop = config.get("Loop")
        if not isinstance(loop, dict):
            return False
        script_areas = loop.get("Script")
        if not isinstance(script_areas, dict):
            return False

        for area_name, area in script_areas.items():
            if not isinstance(area, dict):
                continue
            name = str(area_name or "")
            enabled = bool(area.get("Enabled", False))
            is_autoquest = name.lower() == "autoquest"
            is_q4_area = int(area.get("Region", 0) or 0) == Q4_TOMB_REGION
            if not is_autoquest and not (enabled and is_q4_area):
                continue

            if int(area.get("Radius", 0) or 0) != int(Q4_TRAIN_RADIUS):
                area["Radius"] = int(Q4_TRAIN_RADIUS)
                changed = True
            if int(area.get("Pick Radius", 0) or 0) != int(Q4_PICK_RADIUS):
                area["Pick Radius"] = int(Q4_PICK_RADIUS)
                changed = True
    except Exception as ex:
        zlog("CONFIG Q4 AREA ERRO: %s" % str(ex))
    return changed

def enable_attack_quest_monster_config(source="MANUAL", allow_reload=True):
    get_path_fn = globals().get("get_config_path", None)
    if not callable(get_path_fn):
        zlog("CONFIG QUEST MOB -> get_config_path() indisponivel; nao deu para alterar perfil.")
        return (False, False)

    config_path = str(get_path_fn() or "").strip()
    if not config_path or not os.path.isfile(config_path):
        zlog("CONFIG QUEST MOB -> caminho do perfil invalido: %s" % config_path)
        return (False, False)

    try:
        with open(config_path, "r", encoding="utf-8-sig") as handle:
            config = json.load(handle)
        if not isinstance(config, dict):
            zlog("CONFIG QUEST MOB -> JSON raiz nao e objeto.")
            return (False, False)

        previous = bool(config.get("Attack Quest Monster", False))
        config["Attack Quest Monster"] = True
        area_changed = apply_q4_training_area_config(config)
        changed = (not previous) or area_changed

        if not changed:
            zlog("CONFIG QUEST MOB -> ja estava OK | source=%s | %s" % (source, config_path))
        else:
            with open(config_path, "w", encoding="utf-8") as handle:
                json.dump(config, handle, ensure_ascii=False, indent=4)
            zlog("CONFIG QUEST MOB -> aplicado | source=%s | quest_mob=%s->true | Q4 R=%d PICK=%d | %s" %
                 (source, str(previous).lower(), int(Q4_TRAIN_RADIUS), int(Q4_PICK_RADIUS), config_path))

        reload_fn = globals().get("reload_profile", None)
        if allow_reload and changed and callable(reload_fn):
            reload_fn()
            zlog("CONFIG QUEST MOB -> reload_profile() chamado.")
            return (changed, True)
        if allow_reload and changed:
            zlog("CONFIG QUEST MOB -> reload_profile() indisponivel; recarregue o perfil/phBot manualmente.")
        return (changed, False)
    except Exception as ex:
        zlog("CONFIG QUEST MOB ERRO: %s" % str(ex))
        return (False, False)

def run_auto_quest_mob_fix(source):
    if not should_auto_fix_quest_mob():
        zlog("CONFIG QUEST MOB -> AutoFix desligado | source=%s" % source)
        return
    enable_attack_quest_monster_config(source, True)

def btnQuestMobOn():
    zlog("========================================")
    zlog("QUEST MOB ON / RELOAD")
    zlog("========================================")
    enable_attack_quest_monster_config("BOTAO", True)

def btnStartQ1():
    global death_seen, success_seen, confirm_ok_attempts, arena_started_at
    global arena_entry_attempts
    global handin_reward_retry_count, quest_accept_name_index, post_accept_ok_sent

    if not guard_start_quest(1):
        return

    death_seen = False
    success_seen = False
    confirm_ok_attempts = 0
    arena_started_at = 0.0
    arena_entry_attempts = 0
    handin_reward_retry_count = 0
    quest_accept_name_index = 0
    post_accept_ok_sent = False
    capture_off()

    zlog("========================================")
    zlog("ZERK QUEST v%s" % pVersion)
    zlog("START")
    zlog("========================================")
    run_auto_quest_mob_fix("START")
    sync_current_quest_index()
    log_chain()

    qdef = current_quest()
    if not qdef:
        zlog("ZERK 1 concluida.")
        return

    if qdef["order"] == 2:
        status = quest_status()
        if status == "ACTIVE":
            zlog("Q2 ja esta ativa -> %s | %s" %
                 (qdef["name"], qdef["servername"]))
            go_exorcist()
            return
        go_general(STATE_GO_GENERAL, "PATH -> General Sonhyeon para aceitar Q2")
        return

    if qdef["order"] != 1:
        zlog("Fluxo da quest atual ainda nao mapeado.")
        return

    go_general()

def btnStartQ2():
    global current_quest_index, death_seen, success_seen, confirm_ok_attempts, arena_started_at
    global arena_entry_attempts
    global handin_reward_retry_count, quest_accept_name_index, post_accept_ok_sent

    if not guard_start_quest(2):
        return

    current_quest_index = 1
    death_seen = False
    success_seen = False
    confirm_ok_attempts = 0
    arena_started_at = 0.0
    arena_entry_attempts = 0
    handin_reward_retry_count = 0
    quest_accept_name_index = 0
    post_accept_ok_sent = False
    capture_off()

    zlog("========================================")
    zlog("ZERK QUEST v%s" % pVersion)
    zlog("START Q2")
    zlog("========================================")
    run_auto_quest_mob_fix("START Q2")
    log_chain()
    go_general(STATE_GO_GENERAL, "PATH -> General Sonhyeon para aceitar Q2")

def btnStartQ3():
    global current_quest_index, death_seen, success_seen, confirm_ok_attempts, arena_started_at
    global arena_entry_attempts, exorcist_path_retries, exorcist_path_started_at
    global handin_reward_retry_count, quest_accept_name_index, post_accept_ok_sent

    if not guard_start_quest(3):
        return

    current_quest_index = 2
    death_seen = False
    success_seen = False
    confirm_ok_attempts = 0
    arena_started_at = 0.0
    arena_entry_attempts = 0
    exorcist_path_retries = 0
    exorcist_path_started_at = 0.0
    handin_reward_retry_count = 0
    quest_accept_name_index = 0
    post_accept_ok_sent = False
    capture_off()

    zlog("========================================")
    zlog("ZERK QUEST v%s" % pVersion)
    zlog("START Q3")
    zlog("Valida status da Q3 e retoma: Exorcist, B2 ou Buda.")
    zlog("========================================")
    run_auto_quest_mob_fix("START Q3")
    log_chain()

    route_current_step("START Q3")

def btnStartQ4():
    global current_quest_index, death_seen, success_seen, confirm_ok_attempts, arena_started_at
    global arena_entry_attempts, exorcist_path_retries, exorcist_path_started_at
    global handin_reward_retry_count, quest_accept_name_index, post_accept_ok_sent

    if not guard_start_quest(4):
        return

    current_quest_index = 3
    death_seen = False
    success_seen = False
    confirm_ok_attempts = 0
    arena_started_at = 0.0
    arena_entry_attempts = 0
    exorcist_path_retries = 0
    exorcist_path_started_at = 0.0
    handin_reward_retry_count = 0
    quest_accept_name_index = 0
    post_accept_ok_sent = False
    capture_off()

    zlog("========================================")
    zlog("ZERK QUEST v%s" % pVersion)
    zlog("START Q4")
    zlog("Valida status da Q4 e retoma: Buda, Tombstone ou Exorcist.")
    zlog("========================================")
    run_auto_quest_mob_fix("START Q4")
    log_chain()

    route_current_step("START Q4")

def btnStartQ5():
    global current_quest_index, death_seen, success_seen, confirm_ok_attempts, arena_started_at
    global arena_entry_attempts, exorcist_path_retries, exorcist_path_started_at
    global hunter_path_retries, hunter_path_started_at
    global handin_reward_retry_count, quest_accept_name_index, post_accept_ok_sent

    if not guard_start_quest(5):
        return

    current_quest_index = 4
    death_seen = False
    success_seen = False
    confirm_ok_attempts = 0
    arena_started_at = 0.0
    arena_entry_attempts = 0
    exorcist_path_retries = 0
    exorcist_path_started_at = 0.0
    hunter_path_retries = 0
    hunter_path_started_at = 0.0
    handin_reward_retry_count = 0
    quest_accept_name_index = 0
    post_accept_ok_sent = False
    capture_off()

    zlog("========================================")
    zlog("ZERK QUEST v%s" % pVersion)
    zlog("START Q5")
    zlog("Fluxo: Exorcist Miaoryeong -> Hunter Associate Gwakwi.")
    zlog("Q6 fica MANUAL por enquanto.")
    zlog("========================================")
    run_auto_quest_mob_fix("START Q5")
    log_chain()

    route_current_step("START Q5")

def btnStartQ6():
    global current_quest_index, death_seen, success_seen, confirm_ok_attempts, arena_started_at
    global arena_entry_attempts, exorcist_path_retries, exorcist_path_started_at
    global hunter_path_retries, hunter_path_started_at
    global handin_reward_retry_count, quest_accept_name_index, post_accept_ok_sent

    if not guard_start_quest(6):
        return

    current_quest_index = 5
    death_seen = False
    success_seen = False
    confirm_ok_attempts = 0
    arena_started_at = 0.0
    arena_entry_attempts = 0
    exorcist_path_retries = 0
    exorcist_path_started_at = 0.0
    hunter_path_retries = 0
    hunter_path_started_at = 0.0
    handin_reward_retry_count = 0
    quest_accept_name_index = 0
    post_accept_ok_sent = False
    capture_off()

    zlog("========================================")
    zlog("ZERK QUEST v%s" % pVersion)
    zlog("START Q6")
    zlog("Fluxo: Hunter Associate Gwakwi -> aceitar The Spirit -> fechar NPC -> MANUAL.")
    zlog("Quando receber as traps, o script para com aviso.")
    zlog("========================================")
    run_auto_quest_mob_fix("START Q6")
    log_chain()

    route_current_step("START Q6")

def btnStartQ7():
    global current_quest_index, death_seen, success_seen, confirm_ok_attempts, arena_started_at
    global arena_entry_attempts, exorcist_path_retries, exorcist_path_started_at
    global hunter_path_retries, hunter_path_started_at
    global handin_reward_retry_count, quest_accept_name_index, post_accept_ok_sent

    if not guard_start_quest(7):
        return

    current_quest_index = 6
    death_seen = False
    success_seen = False
    confirm_ok_attempts = 0
    arena_started_at = 0.0
    arena_entry_attempts = 0
    exorcist_path_retries = 0
    exorcist_path_started_at = 0.0
    hunter_path_retries = 0
    hunter_path_started_at = 0.0
    handin_reward_retry_count = 0
    quest_accept_name_index = 0
    post_accept_ok_sent = False
    capture_off()

    zlog("========================================")
    zlog("ZERK QUEST v%s" % pVersion)
    zlog("START Q7")
    zlog("Fluxo: Exorcist Miaoryeong -> aceitar Piece of Spirit -> MANUAL ZERK.")
    zlog(Q7_MANUAL_ZERK_MESSAGE)
    zlog("========================================")
    run_auto_quest_mob_fix("START Q7")
    log_chain()

    route_current_step("START Q7")

def btnStartQ8():
    global current_quest_index, death_seen, success_seen, confirm_ok_attempts, arena_started_at
    global arena_entry_attempts, exorcist_path_retries, exorcist_path_started_at
    global hunter_path_retries, hunter_path_started_at
    global handin_reward_retry_count, quest_accept_name_index, post_accept_ok_sent

    if not guard_start_quest(8):
        return

    current_quest_index = 7
    death_seen = False
    success_seen = False
    confirm_ok_attempts = 0
    arena_started_at = 0.0
    arena_entry_attempts = 0
    exorcist_path_retries = 0
    exorcist_path_started_at = 0.0
    hunter_path_retries = 0
    hunter_path_started_at = 0.0
    handin_reward_retry_count = 0
    quest_accept_name_index = 0
    post_accept_ok_sent = False
    capture_off()

    zlog("========================================")
    zlog("ZERK QUEST v%s" % pVersion)
    zlog("START Q8")
    zlog("Fluxo final: Exorcist Miaoryeong -> New Power -> General Sonhyeon -> Reward.")
    zlog("========================================")
    run_auto_quest_mob_fix("START Q8")
    log_chain()

    route_current_step("START Q8")

def btnStartSelectedBlue():
    order = selected_quest_order(lstBlueQuestStatus, ZERK_1_QUESTS, "Blue Zerk 95")
    if order == 1:
        btnStartQ1()
    elif order == 2:
        btnStartQ2()
    elif order == 3:
        btnStartQ3()
    elif order == 4:
        btnStartQ4()
    elif order == 5:
        btnStartQ5()
    elif order == 6:
        btnStartQ6()
    elif order == 7:
        btnStartQ7()
    elif order == 8:
        btnStartQ8()

def btnResumeQuest():
    global death_seen, success_seen, confirm_ok_attempts, arena_started_at
    global arena_entry_attempts, exorcist_path_retries, exorcist_path_started_at
    global hunter_path_retries, hunter_path_started_at
    global handin_reward_retry_count, quest_accept_name_index, post_accept_ok_sent

    death_seen = False
    success_seen = False
    confirm_ok_attempts = 0
    arena_started_at = 0.0
    arena_entry_attempts = 0
    exorcist_path_retries = 0
    exorcist_path_started_at = 0.0
    hunter_path_retries = 0
    hunter_path_started_at = 0.0
    handin_reward_retry_count = 0
    quest_accept_name_index = 0
    post_accept_ok_sent = False
    capture_off()

    zlog("========================================")
    zlog("ZERK QUEST v%s" % pVersion)
    zlog("RESUME / VALIDATOR")
    zlog("========================================")
    run_auto_quest_mob_fix("RESUME")
    route_current_step("RESUME")

def btnStopQ1():
    global confirm_ok_attempts, arena_started_at, arena_entry_attempts, exorcist_path_retries, exorcist_path_started_at
    global hunter_path_retries, hunter_path_started_at
    global handin_reward_retry_count, quest_accept_name_index, post_accept_ok_sent
    confirm_ok_attempts = 0
    arena_started_at = 0.0
    arena_entry_attempts = 0
    exorcist_path_retries = 0
    exorcist_path_started_at = 0.0
    hunter_path_retries = 0
    hunter_path_started_at = 0.0
    handin_reward_retry_count = 0
    quest_accept_name_index = 0
    post_accept_ok_sent = False
    capture_off()
    stop_script()
    stop_bot()
    set_state(STATE_IDLE)
    zlog("STOP / RESET")

def handle_silkroad(opcode, data):
    if capture_client and opcode not in (0x7021, 0x704F, 0x2002):
        zlog("C->S 0x%04X LEN=%d DATA=%s" % (opcode, len(data) if data else 0, packet_hex(data)))
    return True

def teleported():
    global success_seen, arena_started_at, exorcist_path_retries, exorcist_path_started_at

    zlog("TELEPORTED | state=%s" % state)

    if state in (STATE_GO_Q4_TOMB, STATE_Q4_TOMB_AUTO_RETRY, STATE_Q4_WAIT_MANUAL_TOMB):
        qdef = current_quest()
        if qdef and qdef["order"] == 4 and quest_status() == "ACTIVE":
            zlog("TP durante Q4 ativa -> aguardando/detectando Tombstone para usar Spirit's Bell.")
            wait_q4_tomb_arrival("Q4")
            return

    if state in ARENA_ENTRY_STATES:
        capture_off()
        if confirm_arena_entry():
            arena_started_at = time.time()
            start_q1_arena_training()
        else:
            zlog("TP em etapa de entrada, mas local da arena nao confirmou.")
            set_state(STATE_WAIT_ENTER, 2.0)
        return

    if state in (STATE_ARENA, STATE_WAIT_RETURN_CHECK, STATE_WAIT_RETURN_FAIL):
        stop_bot()
        elapsed = 0.0
        if arena_started_at > 0.0:
            elapsed = time.time() - arena_started_at
        if death_seen:
            set_state(STATE_WAIT_RETURN_FAIL, 2.0)
            zlog("TP SAIDA ARENA -> FALHOU/MORREU | tempo=%.1fs" % elapsed)
        else:
            set_state(STATE_WAIT_RETURN_CHECK, 2.0)
            zlog("TP SAIDA ARENA -> verificando quest apos retorno | tempo=%.1fs" % elapsed)
        return

    if state == STATE_Q3_WAIT_TOWN:
        stop_script()
        exorcist_path_retries = 0
        exorcist_path_started_at = 0.0
        zlog("TP RETURN SCROLL -> cidade. Indo para Buddhist Priest Jeonghye por path automatico.")
        go_buddha("Cidade > Buddhist Priest Jeonghye para entregar Q3.")
        return

    if state == STATE_Q4_WAIT_TOWN:
        stop_script()
        exorcist_path_retries = 0
        exorcist_path_started_at = 0.0
        zlog("TP SPECIAL RETURN -> cidade. Indo para Exorcist Miaoryeong por path automatico.")
        go_exorcist(None)
        return

    if state == STATE_Q6_WAIT_TOWN:
        stop_script()
        exorcist_path_retries = 0
        exorcist_path_started_at = 0.0
        zlog("TP RETURN SCROLL -> cidade. Indo para Exorcist Miaoryeong por path automatico.")
        go_exorcist(None)
        return

    if state == STATE_INVENTORY_WAIT_TOWN:
        stop_script()
        zlog("TP RETURN SCROLL -> cidade. Inventory voltando ao NPC para entrega.")
        start_inventory_path("NPC", "Inventory retorno -> NPC de entrega.")
        return

    if state == STATE_INVENTORY_REVERSE_WIND:
        stop_script()
        zlog("TP REVERSE WIND -> waiting %.1fs before Inventory %s path." %
             (INVENTORY_AFTER_REVERSE_DELAY, inventory_reverse_next_kind))
        set_state(STATE_INVENTORY_AFTER_REVERSE, INVENTORY_AFTER_REVERSE_DELAY)
        return

def handle_event(t, data):
    global death_seen
    if t == 7 and state == STATE_ARENA:
        death_seen = True
        stop_bot()
        set_state(STATE_WAIT_RETURN_FAIL)
        zlog("MORTE detectada dentro da arena.")
    return

def event_loop():
    global last_loop, success_seen, death_seen, confirm_ok_attempts, arena_started_at
    global arena_entry_attempts, current_quest_index
    global exorcist_path_started_at, exorcist_path_retries
    global handin_reward_retry_count, quest_accept_name_index
    global post_accept_ok_sent

    now = time.time()

    if now - last_loop < 0.20:
        return
    last_loop = now

    if now < state_time:
        return

    if state == STATE_GO_GENERAL:
        dist = get_distance_to_general()
        if dist <= ARRIVAL_DISTANCE:
            zlog("CHEGOU no General | distancia=%.1f" % dist)
            stop_script()

            qdef = current_quest()
            status = quest_status()
            if qdef and qdef["order"] == 1 and status in ("COMPLETED", "OBJECTIVES_COMPLETED"):
                zlog("Q1 ja esta completa -> BLOCO 2 entrega.")
                set_state(STATE_HANDIN, 0.50)
            elif qdef and qdef["order"] == 2 and status in ("COMPLETED", "OBJECTIVES_COMPLETED"):
                zlog("Q2 ja esta completa -> indo para Exorcist Miaoryeong.")
                go_exorcist()
            elif qdef and qdef["order"] == 8 and status in ("ACTIVE", "COMPLETED", "OBJECTIVES_COMPLETED"):
                zlog("Q8 no General -> entrega final com OK + Reward.")
                set_state(STATE_HANDIN, 0.50)
            elif qdef and qdef["order"] == 3:
                zlog("Q3 deve iniciar perto da Exorcist; use START Q3 nela.")
                set_state(STATE_IDLE)
            elif status == "ACTIVE":
                qid, active = find_current_active_quest()
                after_quest_active(qid, active)
            else:
                # IMPORTANTE:
                # O comando nativo "quest,..." ja faz a interacao necessaria
                # com o NPC. Nao abrimos 0x7045/0x7046 antes dele para evitar
                # "Failed to enter NPC [error 7179]".
                zlog("Quest nao ativa; usando comando QUEST diretamente.")
                set_state(STATE_ACCEPT, 0.3)
        elif path_watchdog_ready(general_path_started_at) and path_watchdog("GENERAL", retry_general_path, general_path_retries, AUTO_PATH_MAX_RETRIES):
            return
        elif general_path_started_at > 0.0 and time.time() - general_path_started_at >= AUTO_PATH_TIMEOUT:
            if general_path_retries < AUTO_PATH_MAX_RETRIES:
                retry_general_path()
            else:
                zlog("PATH GENERAL falhou apos retry; capture/manual necessario.")
                capture_on()
                set_state(STATE_DONE)
        return

    if state == STATE_GENERAL_AUTO_RETRY:
        go_general(general_retry_next_state, general_retry_reason, False)
        return

    if state == STATE_SELECT_1:
        if select_general():
            set_state(STATE_OPEN_1, 0.35)
        return

    if state == STATE_OPEN_1:
        if open_general():
            set_state(STATE_ACCEPT, 0.70)
        return

    if state == STATE_ACCEPT:
        if accept_current_quest():
            confirm_ok_attempts = 0
            zlog("Aguardando dialogo OK extra antes de confirmar.")
            set_state(STATE_CONFIRM_OK, DELAY_AFTER_QUEST_CMD)
        return

    if state == STATE_CONFIRM_OK:
        qid, active = find_current_active_quest()
        if active is not None:
            zlog("QUEST JA ATIVA ANTES DO OK EXTRA | ID=%s | NAME=%s | SERVERNAME=%s" %
                 (qid, active.get("name"), active.get("servername")))
            if needs_post_accept_ok():
                zlog("QUEST ATIVA -> aguardando OK final do dialogo.")
                set_state(STATE_POST_ACCEPT_OK, DELAY_BEFORE_POST_ACCEPT_OK)
                return
            after_quest_active(qid, active)
            return

        if confirm_ok_attempts < MAX_CONFIRM_OK_ATTEMPTS:
            confirm_ok_attempts += 1
            zlog("CONFIRM OK EXTRA -> tentativa %d/%d" %
                 (confirm_ok_attempts, MAX_CONFIRM_OK_ATTEMPTS))
            if confirm_accept_ok():
                set_state(STATE_WAIT_ACCEPT, DELAY_AFTER_CONFIRM_OK)
            else:
                set_state(STATE_CONFIRM_OK, DELAY_RETRY_CONFIRM_OK)
            return

        if has_next_accept_quest_name():
            name = next_accept_quest_name()
            zlog("Quest nao ativou; tentando nome alternativo -> %s" % name)
            set_state(STATE_ACCEPT, 0.50)
            return

        zlog("CONFIRM OK EXTRA sem quest ativa apos %d tentativas; aguardando Auto Quest/capture." %
             MAX_CONFIRM_OK_ATTEMPTS)
        set_state(STATE_WAIT_ACCEPT, DELAY_AFTER_CONFIRM_OK)
        return

    if state == STATE_WAIT_ACCEPT:
        qid, active = find_current_active_quest()
        if active is not None:
            zlog("QUEST ACEITA | ID=%s | NAME=%s | SERVERNAME=%s" %
                 (qid, active.get("name"), active.get("servername")))
            if needs_post_accept_ok():
                zlog("QUEST ACEITA -> aguardando OK final do dialogo.")
                set_state(STATE_POST_ACCEPT_OK, DELAY_BEFORE_POST_ACCEPT_OK)
                return
            after_quest_active(qid, active)
        elif confirm_ok_attempts < MAX_CONFIRM_OK_ATTEMPTS:
            zlog("Quest ainda nao ativa; repetindo OK extra.")
            set_state(STATE_CONFIRM_OK, DELAY_RETRY_CONFIRM_OK)
        elif has_next_accept_quest_name():
            name = next_accept_quest_name()
            zlog("Quest ainda nao ativa; tentando nome alternativo -> %s" % name)
            set_state(STATE_ACCEPT, 0.50)
        else:
            zlog("Quest nao ativou; capture manual ligado para este dialogo.")
            capture_on()
            set_state(STATE_DONE)
        return

    if state == STATE_POST_ACCEPT_OK:
        zlog("CONFIRM OK FINAL POS-ACEITE.")
        if confirm_accept_ok():
            post_accept_ok_sent = True
            set_state(STATE_POST_ACCEPT_CONTINUE, DELAY_AFTER_POST_ACCEPT_OK)
        else:
            set_state(STATE_POST_ACCEPT_OK, DELAY_RETRY_CONFIRM_OK)
        return

    if state == STATE_POST_ACCEPT_CONTINUE:
        qid, active = find_current_active_quest()
        if active is not None:
            zlog("POS-ACEITE OK -> seguindo fluxo da quest ativa.")
            after_quest_active(qid, active)
        else:
            zlog("POS-ACEITE OK enviado, mas quest nao aparece ativa; capture manual ligado.")
            capture_on()
            set_state(STATE_DONE)
        return

    if state == STATE_SELECT_2:
        if select_general():
            set_state(STATE_OPEN_2, 0.35)
        return

    if state == STATE_OPEN_2:
        if open_general():
            begin_auto_arena_entry(DELAY_AFTER_OPEN_SECOND_DIALOG)
        return

    if state == STATE_ARENA_QUEST_OPTION:
        if send_dialog_choice(0x06, "ARENA QUEST OPTION"):
            set_state(STATE_ARENA_ENTER_OPTION, DELAY_AFTER_ARENA_QUEST_OPTION)
        return

    if state == STATE_ARENA_ENTER_OPTION:
        if send_dialog_choice(0x05, "ARENA ENTER OPTION"):
            set_state(STATE_ARENA_CONFIRM, DELAY_AFTER_ARENA_ENTER_OPTION)
        return

    if state == STATE_ARENA_CONFIRM:
        if send_arena_confirm():
            set_state(STATE_WAIT_ENTER, DELAY_WAIT_ARENA_TELEPORT)
        return

    if state == STATE_WAIT_ENTER:
        if not capture_client:
            if arena_entry_attempts < MAX_ARENA_ENTRY_ATTEMPTS:
                zlog("TP de entrada ainda nao chegou; reenviando entrada automatica.")
                begin_auto_arena_entry(0.50)
            else:
                zlog("Entrada automatica nao confirmou TP apos %d tentativas." %
                     MAX_ARENA_ENTRY_ATTEMPTS)
                capture_on()
        return

    if state == STATE_ARENA:
        try:
            char = get_character_data()
            if char and bool(char.get("dead", False)):
                death_seen = True
                stop_bot()
                set_state(STATE_WAIT_RETURN_FAIL)
                zlog("DEAD=True -> QUEST FALHOU")
                return
        except:
            pass

        return

    if state == STATE_WAIT_RETURN_FAIL:
        zlog("Q1 FALHOU/MORREU. Clique START para refazer quando estiver pronto.")
        set_state(STATE_IDLE)
        return

    if state == STATE_WAIT_RETURN_CHECK:
        status = quest_status()
        zlog("STATUS APOS RETORNO -> %s" % status)
        if status in ("COMPLETED", "OBJECTIVES_COMPLETED", "NOT_FOUND"):
            zlog("QUEST FINALIZADA/SAIU DA LISTA -> BLOCO 2 entrega.")
            go_general(STATE_GO_HANDIN_GENERAL, "PATH -> General Sonhyeon para entregar Q1")
        else:
            zlog("QUEST AINDA ATIVA -> resultado da arena nao confirmado.")
            set_state(STATE_IDLE)
        return

    if state == STATE_GO_HANDIN_GENERAL:
        dist = get_distance_to_general()
        if dist <= ARRIVAL_DISTANCE:
            zlog("CHEGOU no General para entrega | distancia=%.1f" % dist)
            stop_script()
            set_state(STATE_HANDIN, 0.50)
        elif general_path_started_at > 0.0 and time.time() - general_path_started_at >= AUTO_PATH_TIMEOUT:
            if general_path_retries < AUTO_PATH_MAX_RETRIES:
                retry_general_path()
            else:
                zlog("PATH GENERAL ENTREGA falhou apos retry; capture/manual necessario.")
                capture_on()
                set_state(STATE_DONE)
        return

    if state == STATE_HANDIN:
        if handin_current_quest():
            handin_reward_retry_count = 0
            qdef = current_quest()
            if qdef and bool(qdef.get("handin_direct_reward", False)):
                zlog("Entrega enviada; esta quest abre Reward direto, pulando OK intermediario.")
                set_state(STATE_HANDIN_REWARD, DELAY_AFTER_HANDIN_CMD)
            else:
                zlog("Entrega enviada; aguardando dialogo de confirmacao.")
                set_state(STATE_HANDIN_OK, DELAY_AFTER_HANDIN_CMD)
        return

    if state == STATE_HANDIN_OK:
        zlog("CONFIRM OK ENTREGA -> antes do Reward.")
        if confirm_accept_ok():
            set_state(STATE_HANDIN_REWARD, DELAY_AFTER_HANDIN_OK)
        return

    if state == STATE_HANDIN_REWARD:
        if send_quest_reward():
            set_state(STATE_HANDIN_CLOSE, DELAY_BEFORE_REWARD_CLOSE)
        else:
            zlog("Reward nao enviado; validando status da quest para evitar loop.")
            set_state(STATE_WAIT_HANDIN, DELAY_AFTER_REWARD)
        return

    if state == STATE_HANDIN_CLOSE:
        zlog("FECHANDO JANELA POS-REWARD.")
        close_current_quest_dialog()
        set_state(STATE_WAIT_HANDIN, DELAY_AFTER_REWARD_CLOSE)
        return

    if state == STATE_WAIT_HANDIN:
        qdef = current_quest()
        order = qdef["order"] if qdef else 0
        status = quest_status()
        zlog("STATUS APOS ENTREGA -> %s" % status)
        if status == "NOT_FOUND":
            zlog("Q%d ENTREGUE/REMOVIDA DA LISTA." % order)
            mark_quest_done(order)
            current_quest_index += 1
            log_chain()
            zlog("BLOCO %d FINALIZADO. Use o START do proximo bloco." % order)
            play_done_beep("Q%d" % order)
            set_state(STATE_DONE)
        elif status in ("COMPLETED", "OBJECTIVES_COMPLETED") and handin_reward_retry_count < MAX_HANDIN_REWARD_RETRIES:
            handin_reward_retry_count += 1
            zlog("Q%d ainda aparece completa; reenviando Reward (%d/%d)." %
                 (order, handin_reward_retry_count, MAX_HANDIN_REWARD_RETRIES))
            if send_quest_reward():
                set_state(STATE_HANDIN_CLOSE, DELAY_BEFORE_REWARD_CLOSE)
            else:
                capture_on()
                set_state(STATE_DONE)
        elif status in ("COMPLETED", "OBJECTIVES_COMPLETED"):
            zlog("Q%d ainda aparece completa apos %d Rewards; capture manual ligado." %
                 (order, MAX_HANDIN_REWARD_RETRIES))
            capture_on()
            set_state(STATE_DONE)
        else:
            zlog("Q%d ainda ativa apos tentativa de entrega." % order)
            set_state(STATE_IDLE)
        return

    if state == STATE_GO_EXORCIST:
        dist = get_distance_to(EXORCIST_X, EXORCIST_Y)
        qdef = current_quest()
        status = quest_status()
        if qdef and qdef["order"] == 3 and status == "NOT_FOUND" and dist <= EXORCIST_ACCEPT_DISTANCE:
            zlog("CHEGOU perto da Exorcist para aceitar Q3 | distancia=%.1f" % dist)
            stop_script()
            set_state(STATE_ACCEPT, 0.50)
            return

        if dist <= EXORCIST_ARRIVAL_DISTANCE:
            zlog("CHEGOU em Exorcist Miaoryeong | REGION=%d X=%.1f Y=%.1f | distancia=%.1f" %
                 (EXORCIST_REGION, EXORCIST_X, EXORCIST_Y, dist))
            stop_script()
            if qdef and qdef["order"] == 2:
                zlog("Q2 no Exorcist -> entregando com OK + Reward.")
                set_state(STATE_HANDIN, 0.50)
            elif qdef and qdef["order"] == 3:
                if status in ("COMPLETED", "OBJECTIVES_COMPLETED"):
                    zlog("Q3 completa -> indo para Buddhist Priest Jeonghye entregar.")
                    go_buddha("Exorcist > Buddhist Priest Jeonghye para entregar Q3.")
                elif status == "ACTIVE":
                    zlog("Q3 ativa -> indo para Jangan Cave B2.")
                    go_q3_dungeon()
                else:
                    zlog("Q3 nao ativa -> aceitando na Exorcist.")
                    set_state(STATE_ACCEPT, 0.50)
            elif qdef and qdef["order"] == 4:
                if status in ("COMPLETED", "OBJECTIVES_COMPLETED"):
                    zlog("Q4 completa na Exorcist -> entregando com OK + Reward.")
                    set_state(STATE_HANDIN, 0.50)
                elif status == "ACTIVE":
                    zlog("Q4 ativa mas nao completa -> voltando para Tombstone.")
                    go_q4_tomb()
                else:
                    zlog("Q4 nao encontrada na Exorcist; use RESUME perto do Buda se precisar aceitar.")
                    set_state(STATE_DONE)
            elif qdef and qdef["order"] == 5:
                if status in ("ACTIVE", "COMPLETED", "OBJECTIVES_COMPLETED"):
                    zlog("Q5 ativa/completa -> indo para Hunter Associate Gwakwi entregar.")
                    go_hunter("Exorcist > Hunter Associate Gwakwi para entregar Q5.")
                else:
                    zlog("Q5 na Exorcist -> aceitando Miaoryeong's Charm.")
                    set_state(STATE_ACCEPT, 0.50)
            elif qdef and qdef["order"] == 6:
                if status in ("COMPLETED", "OBJECTIVES_COMPLETED"):
                    zlog("Q6 completa na Exorcist -> entregando com OK + Reward.")
                    set_state(STATE_HANDIN, 0.50)
                elif status == "ACTIVE":
                    zlog("Q6 ativa na Exorcist -> captura manual ainda nao finalizada.")
                    stop_for_q6_manual_capture("Exorcist Miaoryeong")
                else:
                    zlog("Q6 nao ativa na Exorcist; volte ao Hunter ou use START Q6.")
                    set_state(STATE_DONE)
            elif qdef and qdef["order"] == 7:
                if status in ("COMPLETED", "OBJECTIVES_COMPLETED"):
                    zlog("Q7 completa na Exorcist -> entregando com OK + Reward.")
                    set_state(STATE_HANDIN, 0.50)
                elif status == "ACTIVE":
                    zlog("Q7 ativa na Exorcist -> luta com zerk fica manual.")
                    stop_for_q7_manual_zerk("Exorcist Miaoryeong")
                else:
                    zlog("Q7 na Exorcist -> aceitando Piece of Spirit.")
                    set_state(STATE_ACCEPT, 0.50)
            elif qdef and qdef["order"] == 8:
                if status in ("ACTIVE", "COMPLETED", "OBJECTIVES_COMPLETED"):
                    zlog("Q8 ja ativa -> indo para General Sonhyeon entregar final.")
                    go_general(STATE_GO_GENERAL, "PATH -> General Sonhyeon para entregar Q8")
                else:
                    zlog("Q8 na Exorcist -> aceitando New Power.")
                    set_state(STATE_ACCEPT, 0.50)
            else:
                zlog("Exorcist pronta; aguardando proximo capture/fluxo.")
                set_state(STATE_DONE)
        elif exorcist_route_mode == "AUTO" and path_watchdog_ready(exorcist_path_started_at) and path_watchdog("EXORCIST", nudge_and_retry_exorcist_path, exorcist_path_retries, EXORCIST_AUTO_PATH_MAX_RETRIES):
            return
        elif exorcist_route_mode == "AUTO" and exorcist_path_started_at > 0.0:
            if time.time() - exorcist_path_started_at >= EXORCIST_AUTO_PATH_TIMEOUT:
                if exorcist_path_retries < EXORCIST_AUTO_PATH_MAX_RETRIES:
                    nudge_and_retry_exorcist_path()
                elif exorcist_route_fallback:
                    zlog("PATH EXORCIST falhou apos retry; fallback para rota manual.")
                    stop_script()
                    start_exorcist_manual_route(exorcist_route_fallback)
                else:
                    zlog("PATH EXORCIST falhou apos nudges; capture manual necessario.")
                    capture_on()
                    set_state(STATE_DONE)
        return

    if state == STATE_EXORCIST_AUTO_RETRY:
        start_exorcist_auto_path("Recalculando path automatico para Exorcist.", exorcist_route_fallback, False)
        return

    if state == STATE_GO_BUDDHA:
        dist = get_distance_to(BUDDHA_X, BUDDHA_Y)
        if dist <= BUDDHA_ARRIVAL_DISTANCE:
            zlog("CHEGOU no Buddhist Priest Jeonghye | REGION=%d X=%.1f Y=%.1f | distancia=%.1f" %
                 (BUDDHA_REGION, BUDDHA_X, BUDDHA_Y, dist))
            stop_script()
            qdef = current_quest()
            status = quest_status()
            if qdef and qdef["order"] == 3 and status in ("ACTIVE", "COMPLETED", "OBJECTIVES_COMPLETED"):
                zlog("Q3 no Buda -> entregando com OK + Reward.")
                set_state(STATE_HANDIN, 0.50)
            elif qdef and qdef["order"] == 4:
                if status in ("COMPLETED", "OBJECTIVES_COMPLETED"):
                    zlog("Q4 completa -> indo para Exorcist entregar.")
                    go_exorcist(None)
                elif status == "ACTIVE":
                    zlog("Q4 ativa -> indo para Tombstone.")
                    go_q4_tomb()
                else:
                    zlog("Q4 nao ativa -> aceitando Spirit's Shell no Buda.")
                    set_state(STATE_ACCEPT, 0.50)
            else:
                zlog("Buda pronto, mas a quest atual nao encaixou neste bloco | STATUS=%s" % status)
                set_state(STATE_DONE)
        elif path_watchdog_ready(buddha_path_started_at) and path_watchdog("BUDDHA", retry_buddha_path, buddha_path_retries, AUTO_PATH_MAX_RETRIES):
            return
        elif buddha_path_started_at > 0.0 and time.time() - buddha_path_started_at >= AUTO_PATH_TIMEOUT:
            if buddha_path_retries < AUTO_PATH_MAX_RETRIES:
                retry_buddha_path()
            else:
                zlog("PATH BUDDHA falhou apos retry; capture/manual necessario.")
                capture_on()
                set_state(STATE_DONE)
        return

    if state == STATE_BUDDHA_AUTO_RETRY:
        start_buddha_auto_path(buddha_retry_reason, False)
        return

    if state == STATE_GO_HUNTER:
        dist = get_distance_to(HUNTER_X, HUNTER_Y)
        if dist <= HUNTER_ARRIVAL_DISTANCE:
            zlog("CHEGOU no Hunter Associate Gwakwi | REGION=%d X=%.1f Y=%.1f | distancia=%.1f" %
                 (HUNTER_REGION, HUNTER_X, HUNTER_Y, dist))
            stop_script()
            qdef = current_quest()
            status = quest_status()
            if qdef and qdef["order"] == 5 and status in ("ACTIVE", "COMPLETED", "OBJECTIVES_COMPLETED"):
                zlog("Q5 no Hunter -> abrindo dialogo para Reward direto.")
                begin_q5_hunter_handin()
            elif qdef and qdef["order"] == 6:
                if status == "NOT_FOUND":
                    zlog("Q6 no Hunter -> aceitando The Spirit.")
                    set_state(STATE_ACCEPT, 0.50)
                else:
                    zlog("Q6 ja ativa -> traps/captura manual; fechando Hunter e parando.")
                    close_npc_dialog(HUNTER_NAME)
                    stop_for_q6_manual_capture("Hunter Associate Gwakwi")
            else:
                zlog("Hunter pronto, mas a quest atual nao encaixou neste bloco | STATUS=%s" % status)
                set_state(STATE_DONE)
        elif path_watchdog_ready(hunter_path_started_at) and path_watchdog("HUNTER", retry_hunter_path, hunter_path_retries, AUTO_PATH_MAX_RETRIES):
            return
        elif hunter_path_started_at > 0.0 and time.time() - hunter_path_started_at >= HUNTER_AUTO_PATH_TIMEOUT:
            if hunter_path_retries < AUTO_PATH_MAX_RETRIES:
                retry_hunter_path()
            else:
                zlog("PATH HUNTER falhou apos retry; capture/manual necessario.")
                capture_on()
                set_state(STATE_DONE)
        return

    if state == STATE_HUNTER_AUTO_RETRY:
        start_hunter_auto_path(hunter_retry_reason, False)
        return

    if state == STATE_Q5_HUNTER_SELECT:
        if select_npc(HUNTER_NAME, "Q5 HUNTER SELECT"):
            set_state(STATE_Q5_HUNTER_OPEN, 0.50)
        else:
            capture_on()
            set_state(STATE_DONE)
        return

    if state == STATE_Q5_HUNTER_OPEN:
        if open_npc(HUNTER_NAME, "Q5 HUNTER OPEN"):
            set_state(STATE_Q5_HUNTER_TALK, DELAY_AFTER_OPEN_SECOND_DIALOG)
        else:
            capture_on()
            set_state(STATE_DONE)
        return

    if state == STATE_Q5_HUNTER_TALK:
        if send_dialog_choice(Q5_HUNTER_TALK_OPTION, "Q5 HUNTER TALK/LISTA"):
            set_state(STATE_Q5_HUNTER_REWARD, Q5_HUNTER_REWARD_DELAY)
        else:
            capture_on()
            set_state(STATE_DONE)
        return

    if state == STATE_Q5_HUNTER_REWARD:
        zlog("Q5 Hunter -> enviando Reward direto apos lista de quests.")
        if send_quest_reward():
            set_state(STATE_HANDIN_CLOSE, DELAY_BEFORE_REWARD_CLOSE)
        else:
            zlog("Q5 Reward nao enviado; validando status para evitar loop.")
            set_state(STATE_WAIT_HANDIN, DELAY_AFTER_REWARD)
        return

    if state == STATE_INVENTORY_GO_NPC:
        target = inventory_target or inventory_target_pos("NPC")
        dist = get_distance_to(target[1], target[2]) if target else 999999.0
        if dist <= INVENTORY_NPC_ARRIVAL_DISTANCE:
            qdef = current_quest()
            status = quest_status()
            zlog("CHEGOU no NPC Inventory | Q%d | distancia=%.1f | STATUS=%s" %
                 (int(qdef["order"]) if qdef else 0, dist, status))
            stop_script()
            if status in ("COMPLETED", "OBJECTIVES_COMPLETED"):
                set_state(STATE_HANDIN, 0.50)
            elif status == "ACTIVE":
                start_inventory_path("MOB", "Inventory ativa/incompleta -> area de mob.")
            else:
                set_state(STATE_ACCEPT, 0.50)
        elif inventory_path_progress_watchdog(retry_inventory_path, inventory_path_retries, AUTO_PATH_MAX_RETRIES):
            return
        elif path_watchdog_ready(inventory_path_started_at) and path_watchdog("INVENTORY NPC", retry_inventory_path, inventory_path_retries, AUTO_PATH_MAX_RETRIES):
            return
        elif (inventory_path_started_at > 0.0 and
              time.time() - inventory_path_started_at >= AUTO_PATH_TIMEOUT and
              time.time() - inventory_last_progress_at >= AUTO_PATH_TIMEOUT):
            if inventory_path_retries < AUTO_PATH_MAX_RETRIES:
                retry_inventory_path()
            else:
                zlog("PATH INVENTORY NPC falhou apos retry; capture/manual necessario.")
                capture_on()
                set_state(STATE_DONE)
        return

    if state == STATE_INVENTORY_GO_MOB:
        target = inventory_target or inventory_target_pos("MOB")
        dist = get_distance_to(target[1], target[2]) if target else 999999.0
        if dist <= INVENTORY_MOB_ARRIVAL_DISTANCE:
            qdef = current_quest()
            zlog("CHEGOU na area mob Inventory | Q%d | distancia=%.1f" %
                 (int(qdef["order"]) if qdef else 0, dist))
            start_inventory_training()
        elif inventory_path_progress_watchdog(retry_inventory_path, inventory_path_retries, AUTO_PATH_MAX_RETRIES):
            return
        elif path_watchdog_ready(inventory_path_started_at) and path_watchdog("INVENTORY MOB", retry_inventory_path, inventory_path_retries, AUTO_PATH_MAX_RETRIES):
            return
        elif (inventory_path_started_at > 0.0 and
              time.time() - inventory_path_started_at >= AUTO_PATH_TIMEOUT and
              time.time() - inventory_last_progress_at >= AUTO_PATH_TIMEOUT):
            if inventory_path_retries < AUTO_PATH_MAX_RETRIES:
                retry_inventory_path()
            else:
                zlog("PATH INVENTORY MOB falhou apos retry; capture/manual necessario.")
                capture_on()
                set_state(STATE_DONE)
        return

    if state == STATE_INVENTORY_TRAIN:
        try:
            char = get_character_data()
            if char and bool(char.get("dead", False)):
                stop_bot()
                zlog("INVENTORY TRAIN -> morto; parando bloco.")
                set_state(STATE_IDLE)
                return
        except:
            pass
        status = quest_status()
        if status in ("COMPLETED", "OBJECTIVES_COMPLETED"):
            stop_bot()
            qdef = current_quest()
            if qdef and int(qdef.get("order", 0)) == 4:
                zlog("Inventory Q4 objetivo completo -> voltando a pe para o NPC.")
                start_inventory_path("NPC", "Inventory Q4 completa -> voltar andando ao NPC de entrega.")
                return
            zlog("Inventory Q%d objetivo completo -> Return Scroll selecionado." %
                 (int(qdef["order"]) if qdef else 0))
            set_state(STATE_INVENTORY_RETURN_SCROLL, INVENTORY_RETURN_SCROLL_DELAY)
        else:
            set_state(STATE_INVENTORY_TRAIN, INVENTORY_TRAIN_CHECK_DELAY)
        return

    if state == STATE_INVENTORY_RETURN_SCROLL:
        use_return_scroll(STATE_INVENTORY_WAIT_TOWN, "INVENTORY", INVENTORY_TOWN_CHECK_DELAY, selected_return_scroll_command())
        return

    if state == STATE_INVENTORY_WAIT_TOWN:
        zlog("Waiting for Inventory return teleport...")
        retry_return_scroll_if_needed()
        return

    if state == STATE_INVENTORY_REVERSE_WIND:
        zlog("INVENTORY Q4 -> using reverse,location,Wind Town.")
        try:
            start_script(INVENTORY_REVERSE_WIND_COMMAND + "\n")
            set_state(STATE_INVENTORY_AFTER_REVERSE, INVENTORY_AFTER_REVERSE_DELAY)
        except Exception as ex:
            zlog("INVENTORY Q4 REVERSE ERRO: %s" % str(ex))
            start_inventory_path(inventory_reverse_next_kind, "Inventory Q4 reverse failed -> direct %s path." % inventory_reverse_next_kind)
        return

    if state == STATE_INVENTORY_AFTER_REVERSE:
        zlog("Inventory Q4 reverse wait done -> starting %s path." % inventory_reverse_next_kind)
        start_inventory_path(inventory_reverse_next_kind, "Inventory Q4 after reverse -> %s path." % inventory_reverse_next_kind)
        return

    if state == STATE_GO_Q3_DUNGEON:
        dist = get_distance_to(Q3_DUNGEON_X, Q3_DUNGEON_Y)
        if dist <= Q3_DUNGEON_ARRIVAL_DISTANCE:
            zlog("CHEGOU no B2 Stone Beast | REGION=%d X=%.1f Y=%.1f | distancia=%.1f" %
                 (Q3_DUNGEON_REGION, Q3_DUNGEON_X, Q3_DUNGEON_Y, dist))
            start_q3_training()
        return

    if state == STATE_Q4_TOMB_PREFIX_WAIT:
        dist = get_distance_to(Q4_PREFIX_TARGET_X, Q4_PREFIX_TARGET_Y)
        elapsed = time.time() - q4_tomb_prefix_started_at
        if dist <= Q4_PREFIX_ARRIVAL_DISTANCE:
            zlog("Q4 prefix manual OK | distancia=%.1f; calculando path." % dist)
            stop_script()
            set_state(STATE_Q4_TOMB_START_PATH, 0.10)
        elif elapsed >= Q4_PREFIX_TIMEOUT:
            zlog("Q4 prefix timeout %.1fs | distancia=%.1f; calculando path mesmo assim." %
                 (elapsed, dist))
            stop_script()
            set_state(STATE_Q4_TOMB_START_PATH, 0.10)
        else:
            set_state(STATE_Q4_TOMB_PREFIX_WAIT, 0.50)
        return

    if state == STATE_Q4_TOMB_START_PATH:
        start_q4_tomb_auto_path()
        return

    if state == STATE_GO_Q4_TOMB:
        dist = get_distance_to(Q4_TOMB_X, Q4_TOMB_Y)
        if dist <= Q4_TOMB_ARRIVAL_DISTANCE:
            zlog("CHEGOU no Tombstone | REGION=%d X=%.1f Y=%.1f | distancia=%.1f" %
                 (Q4_TOMB_REGION, Q4_TOMB_X, Q4_TOMB_Y, dist))
            stop_script()
            set_state(STATE_Q4_USE_BELL, 0.50)
        elif q4_tomb_path_is_progressing(dist):
            set_state(STATE_GO_Q4_TOMB, 0.50)
        elif path_watchdog_ready(q4_tomb_path_started_at) and path_watchdog("Q4 TOMB", retry_q4_tomb_path, q4_tomb_path_retries, AUTO_PATH_MAX_RETRIES):
            return
        elif q4_tomb_path_started_at > 0.0 and time.time() - q4_tomb_path_started_at >= AUTO_PATH_TIMEOUT:
            if q4_tomb_path_retries < AUTO_PATH_MAX_RETRIES:
                retry_q4_tomb_path()
            else:
                wait_q4_tomb_arrival("PATH Q4 TOMB falhou apos retry.")
        return

    if state == STATE_Q4_TOMB_AUTO_RETRY:
        start_q4_tomb_auto_path()
        return

    if state == STATE_Q4_WAIT_MANUAL_TOMB:
        dist = q4_tomb_arrival_distance()
        if dist <= Q4_TOMB_MANUAL_DISTANCE:
            zlog("Q4 manual/TP chegou no Tombstone | REGION=%d | distancia=%.1f -> usando Spirit's Bell." %
                 (current_region(), dist))
            capture_off()
            stop_script()
            set_state(STATE_Q4_USE_BELL, 0.50)
        else:
            set_state(STATE_Q4_WAIT_MANUAL_TOMB, 1.0)
        return

    if state == STATE_Q4_USE_BELL:
        use_spirit_bell()
        return

    if state == STATE_Q4_START_TRAIN:
        zlog("Q4 -> summon deve estar ativo; iniciando combate local.")
        start_q4_training()
        return

    if state == STATE_Q3_TRAIN:
        try:
            char = get_character_data()
            if char and bool(char.get("dead", False)):
                stop_bot()
                zlog("Q3 TRAIN -> morto; parando bloco.")
                set_state(STATE_IDLE)
                return
        except:
            pass

        status = quest_status()
        zlog("Q3 STATUS TREINO -> %s" % status)
        if status in ("COMPLETED", "OBJECTIVES_COMPLETED"):
            stop_bot()
            zlog("Q3 objetivo completo -> Return Scroll.")
            set_state(STATE_Q3_RETURN_SCROLL, Q3_RETURN_SCROLL_DELAY)
        else:
            set_state(STATE_Q3_TRAIN, Q3_TRAIN_CHECK_DELAY)
        return

    if state == STATE_Q4_TRAIN:
        try:
            char = get_character_data()
            if char and bool(char.get("dead", False)):
                stop_bot()
                zlog("Q4 TRAIN -> morto; parando bloco.")
                set_state(STATE_IDLE)
                return
        except:
            pass

        status = quest_status()
        zlog("Q4 STATUS TREINO -> %s" % status)
        if status in ("COMPLETED", "OBJECTIVES_COMPLETED"):
            stop_bot()
            zlog("Q4 objetivo completo -> Return Scroll selecionado.")
            set_state(STATE_Q4_RETURN_SCROLL, Q4_RETURN_SCROLL_DELAY)
        else:
            set_state(STATE_Q4_TRAIN, Q4_TRAIN_CHECK_DELAY)
        return

    if state == STATE_Q3_RETURN_SCROLL:
        use_return_scroll(STATE_Q3_WAIT_TOWN, "Q3", Q3_TOWN_CHECK_DELAY, selected_return_scroll_command())
        return

    if state == STATE_Q3_WAIT_TOWN:
        zlog("Waiting for Q3 return teleport...")
        retry_return_scroll_if_needed()
        return

    if state == STATE_Q4_RETURN_SCROLL:
        use_return_scroll(STATE_Q4_WAIT_TOWN, "Q4", Q4_TOWN_CHECK_DELAY, selected_return_scroll_command())
        return

    if state == STATE_Q4_WAIT_TOWN:
        zlog("Waiting for Q4 return teleport...")
        retry_return_scroll_if_needed()
        return

    if state == STATE_Q6_WAIT_TOWN:
        zlog("Waiting for return teleport to turn in at Exorcist...")
        retry_return_scroll_if_needed()
        return

    if state == STATE_ACCEPT_NEXT:
        qdef = current_quest()
        if not qdef:
            zlog("Sem proxima quest configurada.")
            set_state(STATE_DONE)
            return
        zlog("ACEITANDO PROXIMA QUEST -> %s | %s" %
             (qdef["name"], qdef["servername"]))
        if accept_current_quest():
            confirm_ok_attempts = 0
            set_state(STATE_CONFIRM_NEXT_OK, DELAY_AFTER_QUEST_CMD)
        return

    if state == STATE_CONFIRM_NEXT_OK:
        qid, active = find_current_active_quest()
        if active is not None:
            zlog("PROXIMA QUEST ATIVA | ID=%s | NAME=%s | SERVERNAME=%s" %
                 (qid, active.get("name"), active.get("servername")))
            stop_script()
            set_state(STATE_DONE)
            return

        if confirm_ok_attempts < MAX_CONFIRM_OK_ATTEMPTS:
            confirm_ok_attempts += 1
            zlog("CONFIRM OK PROXIMA QUEST -> tentativa %d/%d" %
                 (confirm_ok_attempts, MAX_CONFIRM_OK_ATTEMPTS))
            if confirm_accept_ok():
                set_state(STATE_WAIT_NEXT_ACCEPT, DELAY_AFTER_CONFIRM_OK)
            else:
                set_state(STATE_CONFIRM_NEXT_OK, DELAY_RETRY_CONFIRM_OK)
            return

        zlog("PROXIMA QUEST ainda nao ativa; aguardando atualizacao.")
        set_state(STATE_WAIT_NEXT_ACCEPT, DELAY_AFTER_CONFIRM_OK)
        return

    if state == STATE_WAIT_NEXT_ACCEPT:
        qid, active = find_current_active_quest()
        if active is not None:
            zlog("PROXIMA QUEST ACEITA | ID=%s | NAME=%s | SERVERNAME=%s" %
                 (qid, active.get("name"), active.get("servername")))
            stop_script()
            set_state(STATE_DONE)
        elif confirm_ok_attempts < MAX_CONFIRM_OK_ATTEMPTS:
            zlog("Proxima quest ainda nao ativa; repetindo OK extra.")
            set_state(STATE_CONFIRM_NEXT_OK, DELAY_RETRY_CONFIRM_OK)
        else:
            zlog("Nao confirmou a proxima quest; deixando para captura manual.")
            capture_on()
            set_state(STATE_DONE)
        return

zlog("===== ZERK QUEST v0.84-ZERK105-MAP CARREGADO =====")
zlog("Q1 arena: ao entrar, fixa treino local 50/50 e liga o bot ate TP de saida.")
zlog("PATH WATCHDOG: aguarda 12s de path; se ficar parado 5s -> retry/manual.")
zlog("Reward final: 0x7515 + close NPC 0x704B com fallback de UID salvo.")
zlog("Reward close: 0x704B usa primeiro o UID salvo da janela aberta.")
zlog("Reward close: espera 0.6s apos 0x7515 antes de fechar janela.")
zlog("Status: DONE salvo por personagem + inferencia pela quest ativa do phBot.")
zlog("Botoes: DONE bloqueia como finalizada; LOCKED bloqueia ate concluir anteriores.")
zlog("Blue Zerk 95 usa somente Q1-Q8; Army Test 2 fica fora desta cadeia.")
zlog("Q4 Tombstone: distancia ao destino controla progresso; se path falhar, aguarda chegada manual/TP para tocar sino.")
zlog("Return Scroll: escolha Normal/Special/Instant nos checkboxes.")
zlog("Q5 Hunter usa rotina real do NPC: SELECT > OPEN > TALK 06 > REWARD.")
zlog("Q6/Q7 completas fora de Jangan usam o scroll selecionado e entregam OK + Reward.")
zlog("Inventory Q4 volta andando ao NPC depois do farm; reverse Wind Town so ajuda a iniciar perto do NPC.")
zlog("Zerk 105: aba/lista mapeada com 21 prerequisitos; automacao sera adicionada por blocos.")
zlog("Q7 aceita Piece of Spirit e para com ClientNotice para zerk manual.")
zlog("Q8 final: Exorcist Miaoryeong -> General Sonhyeon -> OK + Reward.")
zlog("Inventory Expansion Q1-Q4: NPC -> mob area R25/PICK50 -> return -> Reward.")
zlog("Inventory Q4: opcional reverse,location,Wind Town antes da area de mob.")
run_auto_quest_mob_fix("LOAD")
show_ui_page("blue")
log_chain()
