from flask import Blueprint, render_template, jsonify, request

from app.models import Item


main = Blueprint("main", __name__)


@main.route("/")
def index():
    category = request.args.get("category")
    city = request.args.get("city")
    price_level = request.args.get("price_level")
    sort = request.args.get("sort", "newest")

    query = Item.query

    if category:
        query = query.filter(Item.category == category)

    if city:
        query = query.filter(Item.city == city)

    if price_level:
        query = query.filter(Item.price_level == price_level)

    if sort == "alphabetical":
        query = query.order_by(
            Item.is_featured.desc(),
            Item.title.asc()
        )
    elif sort == "price_low":
        query = query.order_by(
            Item.is_featured.desc(),
            Item.price_level.asc(),
            Item.created_at.desc()
        )
    else:
        query = query.order_by(
            Item.is_featured.desc(),
            Item.created_at.desc()
        )

    items = query.all()

    categories = [
        category_name[0]
        for category_name in Item.query.with_entities(Item.category).distinct().all()
    ]

    cities = [
        city_name[0]
        for city_name in Item.query.with_entities(Item.city).distinct().all()
    ]

    price_levels = [
        price_name[0]
        for price_name in Item.query.with_entities(Item.price_level).distinct().all()
    ]

    return render_template(
        "index.html",
        items=items,
        categories=categories,
        cities=cities,
        price_levels=price_levels,
        selected_category=category,
        selected_city=city,
        selected_price_level=price_level,
        selected_sort=sort,
    )


@main.route("/items/<int:item_id>")
def item_detail(item_id):
    item = Item.query.get_or_404(item_id)

    return render_template(
        "item_detail.html",
        item=item
    )


@main.route("/health")
def health():
    return jsonify({"status": "ok"})


@main.app_errorhandler(404)
def not_found(error):
    return render_template("404.html"), 404