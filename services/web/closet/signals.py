from .models import (
    ParentCategory,
    Category,
    Area,
    Prefecture,
    ClothesIndex,
    IndexCategory,
    Weather,
)

PARENT_CATEGORIES = ["outerwears", "tops", "bottoms"]
CATEGORIES = [
    [
        "insulated",
        # "down",
        "overcoat",
        "trenchcoat",
        "jacket",
        "sweater jacket",
        # "vests",
        # "cardigans",
        # "blazers",
        "rainwear",
    ],
    [
        "no sleeves",
        # "off the shoulders",
        # "tanks",
        # "cropped",
        "short sleeves",
        "long sleeves",
        "pullover",
        # "hoodies",
        # "knitwear",
        # "fleece",
    ],
    [
        "pants",
        # "jeans",
        # "leggings",
        "skirts",
        "shorts",
    ],
]

AREAS = [
    "北海道地方",
    "東北地方",
    "関東・甲信地方",
    "北陸地方",
    "東海地方",
    "近畿地方",
    "中国地方",
    "四国地方",
    "九州地方",
    "沖縄地方",
]
PREFECTURES = [
    ["道北", "道東", "道南", "道央"],
    ["青森県", "岩手県", "宮城県", "秋田県", "山形県", "福島県"],
    ["茨城県", "栃木県", "群馬県", "埼玉県", "千葉県", "東京都", "神奈川県",],
    ["新潟県", "富山県", "石川県", "福井県",],
    ["山梨県", "長野県", "岐阜県", "静岡県", "愛知県", "三重県",],
    ["滋賀県", "京都府", "大阪府", "兵庫県", "奈良県", "和歌山県",],
    ["鳥取県", "島根県", "岡山県", "広島県", "山口県",],
    ["徳島県", "香川県", "愛媛県", "高知県",],
    ["福岡県", "佐賀県", "長崎県", "熊本県", "大分県", "宮崎県", "鹿児島県",],
    ["沖縄県",],
]

CLOTHES_INDEXES = [
    {"value": 10, "description": ""},
    {"value": 20, "description": ""},
    {"value": 30, "description": "コートを着ないと結構寒いなあ。"},
    {"value": 40, "description": "裏地付きトレンチコートがおすすめ。"},
    {"value": 50, "description": "薄手のジャケットを羽織ろう。"},
    {"value": 60, "description": "長袖シャツ・カットソーで快適に。"},
    {"value": 70, "description": "半袖 + カーディガンで温度調節を。"},
    {"value": 80, "description": "半袖Tシャツ一枚で過ごせる暑さ"},
    {"value": 90, "description": "ノースリーブでもかなり暑い。"},
    {"value": 100, "description": "暑さ対策必須！何を着ていても暑い。"},
]

CATEGORY_INDEXES = [
    {"clothes_index_id": 1, "category_id": 1, "needs_outers": 0},
    {"clothes_index_id": 1, "category_id": 10, "needs_outers": 1},
    {"clothes_index_id": 1, "category_id": 11, "needs_outers": 0},
    {"clothes_index_id": 2, "category_id": 1, "needs_outers": 0},
    {"clothes_index_id": 2, "category_id": 2, "needs_outers": 0},
    {"clothes_index_id": 2, "category_id": 9, "needs_outers": 1},
    {"clothes_index_id": 2, "category_id": 10, "needs_outers": 1},
    {"clothes_index_id": 2, "category_id": 11, "needs_outers": 0},
    {"clothes_index_id": 3, "category_id": 2, "needs_outers": 0},
    {"clothes_index_id": 3, "category_id": 9, "needs_outers": 1},
    {"clothes_index_id": 3, "category_id": 10, "needs_outers": 1},
    {"clothes_index_id": 3, "category_id": 11, "needs_outers": 0},
    {"clothes_index_id": 4, "category_id": 2, "needs_outers": 0},
    {"clothes_index_id": 4, "category_id": 3, "needs_outers": 0},
    {"clothes_index_id": 4, "category_id": 9, "needs_outers": 1},
    {"clothes_index_id": 4, "category_id": 10, "needs_outers": 1},
    {"clothes_index_id": 4, "category_id": 11, "needs_outers": 0},
    {"clothes_index_id": 5, "category_id": 3, "needs_outers": 0},
    {"clothes_index_id": 5, "category_id": 4, "needs_outers": 0},
    {"clothes_index_id": 5, "category_id": 5, "needs_outers": 0},
    {"clothes_index_id": 5, "category_id": 9, "needs_outers": 1},
    {"clothes_index_id": 5, "category_id": 10, "needs_outers": 0},
    {"clothes_index_id": 5, "category_id": 11, "needs_outers": 0},
    {"clothes_index_id": 6, "category_id": 4, "needs_outers": 0},
    {"clothes_index_id": 6, "category_id": 5, "needs_outers": 0},
    {"clothes_index_id": 6, "category_id": 8, "needs_outers": 1},
    {"clothes_index_id": 6, "category_id": 9, "needs_outers": 0},
    {"clothes_index_id": 6, "category_id": 10, "needs_outers": 0},
    {"clothes_index_id": 6, "category_id": 11, "needs_outers": 0},
    {"clothes_index_id": 7, "category_id": 4, "needs_outers": 0},
    {"clothes_index_id": 7, "category_id": 5, "needs_outers": 0},
    {"clothes_index_id": 7, "category_id": 8, "needs_outers": 1},
    {"clothes_index_id": 7, "category_id": 11, "needs_outers": 0},
    {"clothes_index_id": 8, "category_id": 8, "needs_outers": 0},
    {"clothes_index_id": 8, "category_id": 11, "needs_outers": 0},
    {"clothes_index_id": 8, "category_id": 12, "needs_outers": 0},
    {"clothes_index_id": 8, "category_id": 13, "needs_outers": 0},
    {"clothes_index_id": 9, "category_id": 7, "needs_outers": 0},
    {"clothes_index_id": 9, "category_id": 8, "needs_outers": 0},
    {"clothes_index_id": 9, "category_id": 11, "needs_outers": 0},
    {"clothes_index_id": 9, "category_id": 12, "needs_outers": 0},
    {"clothes_index_id": 9, "category_id": 13, "needs_outers": 0},
    {"clothes_index_id": 10, "category_id": 7, "needs_outers": 0},
    {"clothes_index_id": 10, "category_id": 8, "needs_outers": 0},
    {"clothes_index_id": 10, "category_id": 11, "needs_outers": 0},
    {"clothes_index_id": 10, "category_id": 12, "needs_outers": 0},
    {"clothes_index_id": 10, "category_id": 13, "needs_outers": 0},
]

WEATHER = [
    {"name": "晴", "icon": '<i class="fas fa-sun"></i>'},
    {"name": "曇", "icon": '<i class="fas fa-cloud"></i>'},
    {"name": "雨", "icon": '<i class="fas fa-umbrella"></i>'},
    {
        "name": "曇時々晴",
        "icon": '<i class="fas fa-cloud"></i> <i class="fas fa-sun"></i>',
    },
    {
        "name": "曇のち晴",
        "icon": '<i class="fas fa-cloud"></i> <i class="fas fa-sun"></i>',
    },
    {
        "name": "曇一時雨",
        "icon": '<i class="fas fa-cloud"></i> <i class="fas fa-umbrella"></i>',
    },
    {
        "name": "雨時々曇",
        "icon": '<i class="fas fa-umbrella"></i> <i class="fas fa-cloud"></i>',
    },
    {
        "name": "雨のち晴",
        "icon": '<i class="fas fa-umbrella"></i> <i class="fas fa-sun"></i>',
    },
]

POPULATE_DATA = [
    [PARENT_CATEGORIES, CATEGORIES, ParentCategory, Category],
    [AREAS, PREFECTURES, Area, Prefecture],
]


def create_category_location(sender, **kwargs):
    for data in POPULATE_DATA:
        if len(data[0]) != len(data[1]):
            raise Exception(f"Error. Length of {data[0]} and {data[1]} don't match.")

        p_list = []

        for p_category in data[0]:
            p_data = data[2].objects.get_or_create(name=p_category)
            p_list.append(p_data)

        for i in range(len(data[0])):
            for category in data[1][i]:
                data[3].objects.get_or_create(name=category, parent=p_list[i][0])


def create_clothes_index(sender, **kwargs):
    for index in CLOTHES_INDEXES:
        index_data = ClothesIndex.objects.get_or_create(
            value=index["value"], description=index["description"]
        )


def create_category_index(sender, **kwargs):
    for data in CATEGORY_INDEXES:
        index = ClothesIndex.objects.get(id=data["clothes_index_id"])
        category = Category.objects.get(id=data["category_id"])
        index_category = IndexCategory.objects.get_or_create(
            clothes_index=index, category=category, needs_outers=data["needs_outers"]
        )


def create_weather(sender, **kwargs):
    for data in WEATHER:
        weather = Weather.objects.get_or_create(name=data["name"], icon=data["icon"])
