from django.http import JsonResponse
from accounts.models import Area, Prefecture
from closet.models import Category, Clothes


def get_location(request):
    pk = request.GET.get("pk")
    # Return all categories if pk is None or empty.
    if not pk:
        pref_list = Prefecture.objects.all()

    # Return categories if geting its pk
    else:
        pref_list = Prefecture.objects.filter(area__pk=pk)

    pref_list = [
        {"pk": prefecture.pk, "name": prefecture.name} for prefecture in pref_list
    ]
    # Return as JSON
    return JsonResponse({"categoryList": pref_list})


def get_category(request):
    pk = request.GET.get("pk")
    # Return all categories if pk is None or empty.
    if not pk:
        category_list = Category.objects.all()

    # Return categories if geting its pk
    else:
        category_list = Category.objects.filter(parent__pk=pk)

    # Return a list that has dicts like this [ {'name': 'short sleeves', 'pk': '5'}, {'name': 'long sleeves', 'pk': '6'}, {...} ]
    category_list = [
        {"pk": category.pk, "name": category.name} for category in category_list
    ]

    # Return as JSON
    return JsonResponse({"categoryList": category_list})


def get_clothes(request):
    category_name = request.GET.get("category_name")
    category_name = category_name.replace("#", "").replace("-", " ").replace("-", " ")
    user = request.user
    if not category_name:
        clothes_dict = {"text": "Something is happening to get category name."}
        is_success = False

    else:
        clothes_list = Clothes.objects.filter(
            owner=user, category__name=category_name
        ).all()
        if clothes_list:
            clothes_dict = []
            for clothes in clothes_list:
                if clothes.picture:
                    img_url = clothes.picture.url
                else:
                    img_url = f"/static/img/icon/clothes/{clothes.category}.jpg"
                clothes_dict.append(
                    {"pk": clothes.pk, "name": clothes.name, "image": img_url}
                )
            is_success = True
        else:
            clothes_dict = {"text": "Not Registered Yet"}
            is_success = False

    return JsonResponse({"clothesDict": clothes_dict, "isSuccess": is_success})


def default_color(request, pk):
    # TODO:
    # if request.method == "POST":
    #     dic = QueryDict(request.body, encoding="utf-8")
    #     color_code = dic.get("color")
    #     id_name = dic.get("id_name")
    #     id = int(id_name.replace("color", "")) - 1
    #
    #     clothes = Clothes.objects.get(pk=pk)
    #     color = clothes.colors.all()[id]
    #     color.code = color_code
    #     color.save()
    return JsonResponse({"colorCode": color_code})
