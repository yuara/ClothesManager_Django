from .models import ParentCategory, Category

parent_categories = ["outerwears", "tops", "bottoms"]
categories = [
    [
        "down",
        "insulated",
        "overcoat",
        "trenchcoat",
        "rainwear",
        "vests",
        "cardigans",
        "blazers",
    ],
    [
        "off the shoulders",
        "tanks",
        "cropped",
        "short sleeves",
        "long sleeves",
        "hoodies",
        "sweats",
        "knitwear",
        "fleece",
    ],
    ["pants", "jeans", "leggings", "skirts", "shorts"],
]


def create_default_category(sender, **kwargs):
    if len(parent_categories) != len(categories):
        raise Exception("Error. Length of categories don't match.")

    p_cates = []

    for p_category in parent_categories:
        p_cate = ParentCategory.objects.get_or_create(name=p_category)
        p_cates.append(p_cate)

    for i in range(len(parent_categories)):
        for category in categories[i]:
            Category.objects.get_or_create(name=category, parent=p_cates[i][0])
