from flask import Blueprint, render_template, jsonify, request

from app.models import Item


main = Blueprint("main", __name__)


@main.route("/")
def index():
    category = request.args.get("category")
    city = request.args.get("city")

    query = Item.query

    if category:
        query = query.filter(Item.category == category)

    if city:
        query = query.filter(Item.city == city)

    items = query.order_by(
        Item.is_featured.desc(),
        Item.created_at.desc()
    ).all()

    categories = [
        category_name[0]
        for category_name in Item.query.with_entities(Item.category).distinct().all()
    ]

    cities = [
        city_name[0]
        for city_name in Item.query.with_entities(Item.city).distinct().all()
    ]

    return render_template(
        "index.html",
        items=items,
        categories=categories,
        cities=cities,
        selected_category=category,
        selected_city=city,
    )


@main.route("/health")
def health():
    return jsonify({"status": "ok"})