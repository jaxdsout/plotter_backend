from agent.models import Client, List, Option, Deal, Card
from property.models import Property
from datetime import date, timedelta


def seed_test_account(user):
    Client.objects.filter(agent=user).delete()
    List.objects.filter(agent=user).delete()
    Deal.objects.filter(agent=user).delete()
    Card.objects.filter(agent=user).delete()

    properties = Property.objects.all()[:3]

    clients = [
        {"first_name": "John", "last_name": "Doe", "email": "john.doe@example.com", "phone_number": "1234567890"},
        {"first_name": "Jane", "last_name": "Smith", "email": "jane.smith@example.com", "phone_number": "0987654321"},
        {"first_name": "Alice", "last_name": "Johnson", "email": "alice.johnson@example.com", "phone_number": "5555555555"},
    ]

    client_instances = [Client.objects.create(agent=user, **client) for client in clients]

    lists = [
        {"client": client_instances[0], "uuid": "list-1"},
        {"client": client_instances[1], "uuid": "list-2"},
        {"client": client_instances[2], "uuid": "list-3"},
        {"client": client_instances[0], "uuid": "list-4"},
        {"client": client_instances[1], "uuid": "list-5"},
    ]

    list_instances = [List.objects.create(agent=user, **list_data) for list_data in lists]

    options = [
        {"property_id": 1, "price": 1200.00, "unit_number": "A1", "layout": "1 Bed", "sq_ft": "750",
         "available": "2025-02-01", "notes": "Pool view", "list": list_instances[0]},
        {"property_id": 2, "price": 1500.00, "unit_number": "B2", "layout": "2 Bed", "sq_ft": "1100",
         "available": "2025-02-10", "notes": "Close to parking", "list": list_instances[0]},
        {"property_id": 3, "price": 900.00, "unit_number": "C3", "layout": "Studio", "sq_ft": "500",
         "available": "2025-01-20", "notes": "Special offer", "list": list_instances[0]},
        {"property_id": 1, "price": 1300.00, "unit_number": "D4", "layout": "1 Bed", "sq_ft": "800",
         "available": "2025-03-01", "notes": None, "list": list_instances[1]},
        {"property_id": 2, "price": 1400.00, "unit_number": "E5", "layout": "1 Bed", "sq_ft": "750",
         "available": "2025-01-30", "notes": "Newly renovated", "list": list_instances[1]},
        {"property_id": 3, "price": 2000.00, "unit_number": "F6", "layout": "3 Bed", "sq_ft": "1500",
         "available": "2025-02-15", "notes": "Top floor", "list": list_instances[2]},
        {"property_id": 1, "price": 1100.00, "unit_number": "G7", "layout": "Studio", "sq_ft": "600",
         "available": "2025-02-20", "notes": "Discount available", "list": list_instances[3]},
        {"property_id": 2, "price": 1700.00, "unit_number": "H8", "layout": "2 Bed", "sq_ft": "1000",
         "available": "2025-02-05", "notes": "Pet friendly", "list": list_instances[4]},
    ]

    for option_data in options:
        Option.objects.create(**option_data)

    deals = [
        {
            "property": properties[0],
            "rent": 2000,
            "rate": 100,
            "commission": 2000.00,
            "status": "over",
            "flat_fee": None,
            "move_date": date.today() + timedelta(days=-75),
            "unit_no": "101A",
            "lease_term": "12 months",
            "agent": user,
            "client": client_instances[0],
            "deal_date": date.today() + timedelta(days=-105),
            "invoice_date": date.today() + timedelta(days=-45),
            "overdue_date": date.today() + timedelta(days=-15),
            "lease_end_date": date.today() + timedelta(days=290),
        },
        {
            "property": properties[1],
            "rent": 1650,
            "rate": 50,
            "commission": 825.00,
            "status": "pend",
            "flat_fee": None,
            "move_date": date.today() + timedelta(days=-5),
            "unit_no": "202B",
            "lease_term": "12 months",
            "agent": user,
            "client": client_instances[1],
            "deal_date": date.today() + timedelta(days=-15),
            "invoice_date": None,
            "overdue_date": None,
            "lease_end_date": date.today() + timedelta(days=360),
        },
        {
            "property": properties[2],
            "rent": 1800,
            "rate": 150,
            "commission": 2700.00,
            "status": "paid",
            "flat_fee": None,
            "move_date": date.today() + timedelta(days=-65),
            "unit_no": "303C",
            "lease_term": "12 months",
            "agent": user,
            "client": client_instances[2],
            "deal_date": date.today() + timedelta(days=-90),
            "invoice_date": date.today() + timedelta(days=-35),
            "overdue_date": None,
            "lease_end_date": date.today() + timedelta(days=760),
        },
    ]

    for deal_data in deals:
        Deal.objects.create(**deal_data)

    print(f"Seeded {len(clients)} clients for user: {user.email}")
