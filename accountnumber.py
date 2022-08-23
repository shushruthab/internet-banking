from faker import Faker

fake = Faker()

def account():
    return fake.credit_card_number(card_type = 'visa16')