import os
from functools import wraps

from flask import Blueprint, render_template, request, redirect, url_for, session, flash

from app import db
from app.models import Item


admin = Blueprint("admin", __name__, url_prefix="/admin")


def admin_required(view_function):
    @wraps(view_function)
    def wrapper(*args, **kwargs):
        if not session.get("admin_logged_in"):
            return redirect(url_for("admin.login"))

        return view_function(*args, **kwargs)

    return wrapper


@admin.route("/login", methods=["GET", "POST"])
def login():
    if session.get("admin_logged_in"):
        return redirect(url_for("admin.dashboard"))

    if request.method == "POST":
        password = request.form.get("password", "")

        if password == os.getenv("ADMIN_PASSWORD"):
            session["admin_logged_in"] = True
            flash("Вхід виконано успішно.", "success")
            return redirect(url_for("admin.dashboard"))

        flash("Неправильний пароль.", "danger")

    return render_template("admin/login.html")


@admin.route("/logout")
def logout():
    session.pop("admin_logged_in", None)
    flash("Ви вийшли з адмінки.", "info")
    return redirect(url_for("admin.login"))


@admin.route("/")
@admin_required
def dashboard():
    items = Item.query.order_by(
        Item.is_featured.desc(),
        Item.created_at.desc()
    ).all()

    return render_template("admin/dashboard.html", items=items)


@admin.route("/items/new", methods=["GET", "POST"])
@admin_required
def create_item():
    if request.method == "POST":
        item, errors = build_item_from_form()

        if not errors:
            db.session.add(item)
            db.session.commit()

            flash("Новий запис успішно створено.", "success")
            return redirect(url_for("admin.dashboard"))

        return render_template(
            "admin/item_form.html",
            item=item,
            errors=errors,
            form_title="Створити новий запис",
            submit_label="Створити"
        )

    empty_item = Item(
        title="",
        short_description="",
        full_description="",
        city="",
        category="",
        price_level="",
        tags="",
        image_url="",
        address="",
        contact_url="",
        is_featured=False
    )

    return render_template(
        "admin/item_form.html",
        item=empty_item,
        errors={},
        form_title="Створити новий запис",
        submit_label="Створити"
    )


@admin.route("/items/<int:item_id>/edit", methods=["GET", "POST"])
@admin_required
def edit_item(item_id):
    item = Item.query.get_or_404(item_id)

    if request.method == "POST":
        updated_item, errors = build_item_from_form(existing_item=item)

        if not errors:
            db.session.commit()

            flash("Запис успішно оновлено.", "success")
            return redirect(url_for("admin.dashboard"))

        return render_template(
            "admin/item_form.html",
            item=updated_item,
            errors=errors,
            form_title="Редагувати запис",
            submit_label="Зберегти зміни"
        )

    return render_template(
        "admin/item_form.html",
        item=item,
        errors={},
        form_title="Редагувати запис",
        submit_label="Зберегти зміни"
    )


@admin.route("/items/<int:item_id>/delete", methods=["GET", "POST"])
@admin_required
def delete_item(item_id):
    item = Item.query.get_or_404(item_id)

    if request.method == "POST":
        db.session.delete(item)
        db.session.commit()

        flash("Запис видалено.", "info")
        return redirect(url_for("admin.dashboard"))

    return render_template("admin/delete_confirm.html", item=item)


@admin.route("/items/<int:item_id>/toggle-featured", methods=["POST"])
@admin_required
def toggle_featured(item_id):
    item = Item.query.get_or_404(item_id)

    item.is_featured = not item.is_featured
    db.session.commit()

    if item.is_featured:
        flash(f'"{item.title}" тепер Featured.', "success")
    else:
        flash(f'Featured знято з "{item.title}".', "info")

    return redirect(url_for("admin.dashboard"))


def build_item_from_form(existing_item=None):
    item = existing_item or Item()

    title = request.form.get("title", "").strip()
    short_description = request.form.get("short_description", "").strip()
    full_description = request.form.get("full_description", "").strip()
    city = request.form.get("city", "").strip()
    category = request.form.get("category", "").strip()
    price_level = request.form.get("price_level", "").strip()
    tags = request.form.get("tags", "").strip()
    image_url = request.form.get("image_url", "").strip()
    address = request.form.get("address", "").strip()
    contact_url = request.form.get("contact_url", "").strip()
    is_featured = request.form.get("is_featured") == "on"

    errors = {}

    if len(title) < 3:
        errors["title"] = "Назва має містити мінімум 3 символи."

    if not short_description:
        errors["short_description"] = "Короткий опис обов’язковий."
    elif len(short_description) > 180:
        errors["short_description"] = "Короткий опис має бути максимум 180 символів."

    if len(full_description) < 30:
        errors["full_description"] = "Повний опис має містити мінімум 30 символів."

    if not city:
        errors["city"] = "Місто обов’язкове."

    if not category:
        errors["category"] = "Категорія обов’язкова."

    if not price_level:
        errors["price_level"] = "Цінова категорія обов’язкова."

    if not tags:
        errors["tags"] = "Додай хоча б один тег."

    if not image_url.startswith(("http://", "https://")):
        errors["image_url"] = "Фото має бути URL і починатися з http:// або https://."

    if not address:
        errors["address"] = "Адреса обов’язкова."

    if contact_url and not contact_url.startswith(("http://", "https://")):
        errors["contact_url"] = "Контактне посилання має починатися з http:// або https://."

    item.title = title
    item.short_description = short_description
    item.full_description = full_description
    item.city = city
    item.category = category
    item.price_level = price_level
    item.tags = tags
    item.image_url = image_url
    item.address = address
    item.contact_url = contact_url or None
    item.is_featured = is_featured

    return item, errors