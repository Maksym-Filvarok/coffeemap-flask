from app import create_app, db
from app.models import Item


seed_items = [
    {
        "title": "Black Bean Coffee",
        "short_description": "Затишна кав’ярня зі specialty coffee та спокійною атмосферою.",
        "full_description": "Black Bean Coffee — це незалежна кав’ярня для тих, хто цінує якісну каву, мінімалістичний інтер’єр і спокійне місце для роботи або зустрічей. У меню є класичні кавові напої, фільтр-кава, десерти та сезонні пропозиції.",
        "city": "Göttingen",
        "category": "Specialty Coffee",
        "price_level": "€€",
        "tags": "wifi, specialty, quiet",
        "image_url": "https://images.unsplash.com/photo-1501339847302-ac426a4a7cbb?auto=format&fit=crop&w=1200&q=80",
        "address": "Weender Straße 12, 37073 Göttingen",
        "contact_url": "https://example.com/black-bean",
        "is_featured": True,
    },
    {
        "title": "Morgenrot Café",
        "short_description": "Світле кафе для сніданків, кави та домашньої випічки.",
        "full_description": "Morgenrot Café спеціалізується на ранкових сніданках, свіжій випічці та каві. Це гарне місце для студентів, фрилансерів і гостей міста, які шукають приємну атмосферу в центрі.",
        "city": "Göttingen",
        "category": "Breakfast",
        "price_level": "€€",
        "tags": "breakfast, bakery, cozy",
        "image_url": "https://images.unsplash.com/photo-1554118811-1e0d58224f24?auto=format&fit=crop&w=1200&q=80",
        "address": "Kurze Straße 5, 37073 Göttingen",
        "contact_url": "https://example.com/morgenrot",
        "is_featured": False,
    },
    {
        "title": "Urban Brew",
        "short_description": "Сучасна кав’ярня з робочими місцями та швидким Wi-Fi.",
        "full_description": "Urban Brew орієнтована на людей, які хочуть поєднати каву та продуктивну роботу. Тут є зручні столики, розетки, швидкий Wi-Fi і спокійна музика.",
        "city": "Göttingen",
        "category": "Work Friendly",
        "price_level": "€€",
        "tags": "wifi, work-friendly, laptop",
        "image_url": "https://images.unsplash.com/photo-1521017432531-fbd92d768814?auto=format&fit=crop&w=1200&q=80",
        "address": "Theaterstraße 8, 37073 Göttingen",
        "contact_url": "https://example.com/urban-brew",
        "is_featured": True,
    },
    {
        "title": "Kaffeewerkstatt",
        "short_description": "Маленька обсмажувальна кав’ярня з авторськими напоями.",
        "full_description": "Kaffeewerkstatt поєднує формат кав’ярні та маленької обсмажувальні. Відвідувачі можуть спробувати різні сорти зерна, отримати рекомендації бариста і купити каву додому.",
        "city": "Göttingen",
        "category": "Specialty Coffee",
        "price_level": "€€€",
        "tags": "roastery, beans, barista",
        "image_url": "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?auto=format&fit=crop&w=1200&q=80",
        "address": "Burgstraße 21, 37073 Göttingen",
        "contact_url": "https://example.com/kaffeewerkstatt",
        "is_featured": False,
    },
    {
        "title": "Little Roastery",
        "short_description": "Кав’ярня з фокусом на свіжообсмажену каву та take-away.",
        "full_description": "Little Roastery — невелике місце для швидкої, але якісної кави. Тут зручно взяти напій із собою або купити пачку зерна для дому.",
        "city": "Göttingen",
        "category": "Takeaway",
        "price_level": "€",
        "tags": "takeaway, beans, quick",
        "image_url": "https://images.unsplash.com/photo-1442512595331-e89e73853f31?auto=format&fit=crop&w=1200&q=80",
        "address": "Goethe-Allee 3, 37073 Göttingen",
        "contact_url": "https://example.com/little-roastery",
        "is_featured": False,
    },
    {
        "title": "Café Linden",
        "short_description": "Класичне neighborhood café з десертами та терасою.",
        "full_description": "Café Linden — це спокійна кав’ярня в районі з домашніми тортами, сезонними напоями та маленькою терасою. Добре підходить для зустрічей і неспішної кави.",
        "city": "Göttingen",
        "category": "Bakery",
        "price_level": "€€",
        "tags": "cake, terrace, classic",
        "image_url": "https://images.unsplash.com/photo-1559925393-8be0ec4767c8?auto=format&fit=crop&w=1200&q=80",
        "address": "Lindenweg 14, 37075 Göttingen",
        "contact_url": "https://example.com/cafe-linden",
        "is_featured": False,
    },
    {
        "title": "Espresso Ecke",
        "short_description": "Невеликий espresso bar для швидкої кави в центрі.",
        "full_description": "Espresso Ecke — це компактний espresso bar у центрі міста. Ідеальне місце для еспресо, капучино або кави з собою під час прогулянки.",
        "city": "Göttingen",
        "category": "Takeaway",
        "price_level": "€",
        "tags": "espresso, takeaway, central",
        "image_url": "https://images.unsplash.com/photo-1511920170033-f8396924c348?auto=format&fit=crop&w=1200&q=80",
        "address": "Markt 4, 37073 Göttingen",
        "contact_url": "https://example.com/espresso-ecke",
        "is_featured": False,
    },
    {
        "title": "Paper Cup Studio",
        "short_description": "Креативна кав’ярня з місцем для роботи та подій.",
        "full_description": "Paper Cup Studio поєднує кав’ярню, робочий простір і маленьку подієву локацію. Тут часто проходять міні-виставки, зустрічі та творчі вечори.",
        "city": "Göttingen",
        "category": "Work Friendly",
        "price_level": "€€",
        "tags": "creative, events, wifi",
        "image_url": "https://images.unsplash.com/photo-1559496417-e7f25cb247f3?auto=format&fit=crop&w=1200&q=80",
        "address": "Nikolaistraße 9, 37073 Göttingen",
        "contact_url": "https://example.com/paper-cup",
        "is_featured": True,
    },
    {
        "title": "Sweet Bean Bakery",
        "short_description": "Кав’ярня-пекарня з круасанами, тортами і кавою.",
        "full_description": "Sweet Bean Bakery пропонує свіжу випічку, круасани, торти та кавові напої. Це гарний вибір для сніданку або солодкої перерви протягом дня.",
        "city": "Göttingen",
        "category": "Bakery",
        "price_level": "€€",
        "tags": "bakery, croissant, sweets",
        "image_url": "https://images.unsplash.com/photo-1485808191679-5f86510681a2?auto=format&fit=crop&w=1200&q=80",
        "address": "Prinzenstraße 17, 37073 Göttingen",
        "contact_url": "https://example.com/sweet-bean",
        "is_featured": False,
    },
    {
        "title": "Green Cup Café",
        "short_description": "Веган-френдлі кав’ярня з рослинним молоком і легкими стравами.",
        "full_description": "Green Cup Café робить акцент на vegan-friendly меню, рослинному молоці, легких сніданках і екологічній упаковці. Тут зручно замовити каву, матчу або невеликий перекус.",
        "city": "Göttingen",
        "category": "Vegan Friendly",
        "price_level": "€€",
        "tags": "vegan, oat milk, eco",
        "image_url": "https://images.unsplash.com/photo-1509042239860-f550ce710b93?auto=format&fit=crop&w=1200&q=80",
        "address": "Jüdenstraße 6, 37073 Göttingen",
        "contact_url": "https://example.com/green-cup",
        "is_featured": False,
    },
]


def seed_database():
    app = create_app()

    with app.app_context():
        if Item.query.count() > 0:
            print("Database already contains items. Seed skipped.")
            return

        for item_data in seed_items:
            item = Item(**item_data)
            db.session.add(item)

        db.session.commit()
        print("Seed completed successfully.")


if __name__ == "__main__":
    seed_database()