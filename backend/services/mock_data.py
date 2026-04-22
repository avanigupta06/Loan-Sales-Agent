"""Mock customer database — simulates CRM, Credit Bureau, and Offer Mart APIs."""

CUSTOMERS = {
    "9876543210": {
        "id": "CUST001",
        "name": "Arjun Sharma",
        "age": 34,
        "city": "Mumbai",
        "salary": 85000,
        "phone": "9876543210",
        "email": "arjun.sharma@email.com",
        "address": "Flat 4B, Lotus Heights, Andheri West, Mumbai - 400053",
        "pan": "ABCPS1234K",
        "credit_score": 762,
        "preapproved_limit": 500000,
    },
    "9123456780": {
        "id": "CUST002",
        "name": "Priya Nair",
        "age": 29,
        "city": "Bangalore",
        "salary": 120000,
        "phone": "9123456780",
        "email": "priya.nair@email.com",
        "address": "No. 12, Koramangala 4th Block, Bangalore - 560034",
        "pan": "BCQPN5678L",
        "credit_score": 810,
        "preapproved_limit": 1000000,
    },
    "9988776655": {
        "id": "CUST003",
        "name": "Rohit Verma",
        "age": 41,
        "city": "Delhi",
        "salary": 60000,
        "phone": "9988776655",
        "email": "rohit.verma@email.com",
        "address": "House 23, Sector 15, Dwarka, New Delhi - 110075",
        "pan": "CDRPV9012M",
        "credit_score": 645,
        "preapproved_limit": 300000,
    },
    "9871234560": {
        "id": "CUST004",
        "name": "Sneha Patel",
        "age": 27,
        "city": "Ahmedabad",
        "salary": 45000,
        "phone": "9871234560",
        "email": "sneha.patel@email.com",
        "address": "B/12 Patel Colony, Navrangpura, Ahmedabad - 380009",
        "pan": "DEPSP3456N",
        "credit_score": 720,
        "preapproved_limit": 200000,
    },
    "9765432100": {
        "id": "CUST005",
        "name": "Karan Mehta",
        "age": 38,
        "city": "Pune",
        "salary": 150000,
        "phone": "9765432100",
        "email": "karan.mehta@email.com",
        "address": "Row House 7, Baner Road, Pune - 411045",
        "pan": "EFKPM7890O",
        "credit_score": 835,
        "preapproved_limit": 2000000,
    },
    "9654321009": {
        "id": "CUST006",
        "name": "Divya Iyer",
        "age": 32,
        "city": "Chennai",
        "salary": 72000,
        "phone": "9654321009",
        "email": "divya.iyer@email.com",
        "address": "Flat 9C, Greenpark Apts, Anna Nagar, Chennai - 600040",
        "pan": "FGDPI2345P",
        "credit_score": 698,
        "preapproved_limit": 400000,
    },
    "9543210098": {
        "id": "CUST007",
        "name": "Amit Joshi",
        "age": 45,
        "city": "Hyderabad",
        "salary": 200000,
        "phone": "9543210098",
        "email": "amit.joshi@email.com",
        "address": "Villa 3, Jubilee Hills, Hyderabad - 500033",
        "pan": "GHAJP6789Q",
        "credit_score": 790,
        "preapproved_limit": 3000000,
    },
    "9432100987": {
        "id": "CUST008",
        "name": "Meera Reddy",
        "age": 26,
        "city": "Kolkata",
        "salary": 38000,
        "phone": "9432100987",
        "email": "meera.reddy@email.com",
        "address": "Flat 2A, Salt Lake City, Sector III, Kolkata - 700097",
        "pan": "HIMPR0123R",
        "credit_score": 580,
        "preapproved_limit": 150000,
    },
    "9321009876": {
        "id": "CUST009",
        "name": "Vikram Singh",
        "age": 36,
        "city": "Jaipur",
        "salary": 95000,
        "phone": "9321009876",
        "email": "vikram.singh@email.com",
        "address": "Plot 45, Vaishali Nagar, Jaipur - 302021",
        "pan": "IJVPS4567S",
        "credit_score": 745,
        "preapproved_limit": 700000,
    },
    "9210098765": {
        "id": "CUST010",
        "name": "Ananya Krishnan",
        "age": 31,
        "city": "Kochi",
        "salary": 55000,
        "phone": "9210098765",
        "email": "ananya.krishnan@email.com",
        "address": "TC 14/1234, Pattom, Thiruvananthapuram - 695004",
        "pan": "JKAKP8901T",
        "credit_score": 710,
        "preapproved_limit": 350000,
    },
}


def get_customer_by_phone(phone: str) -> dict | None:
    return CUSTOMERS.get(phone)


def get_kyc_data(phone: str) -> dict | None:
    customer = get_customer_by_phone(phone)
    if not customer:
        return None
    return {
        "id": customer["id"],
        "name": customer["name"],
        "phone": customer["phone"],
        "address": customer["address"],
        "pan": customer["pan"],
        "email": customer["email"],
        "city": customer["city"],
        "age": customer["age"],
        "kyc_verified": True,
    }


def get_credit_score(phone: str) -> dict | None:
    customer = get_customer_by_phone(phone)
    if not customer:
        return None
    return {
        "phone": phone,
        "credit_score": customer["credit_score"],
        "bureau": "CIBIL",
        "report_date": "2025-01-10",
    }


def get_preapproved_offer(phone: str) -> dict | None:
    customer = get_customer_by_phone(phone)
    if not customer:
        return None
    return {
        "phone": phone,
        "preapproved_limit": customer["preapproved_limit"],
        "interest_rate": 12.5,
        "max_tenure_months": 60,
    }


def get_salary(phone: str) -> float | None:
    customer = get_customer_by_phone(phone)
    return customer["salary"] if customer else None
