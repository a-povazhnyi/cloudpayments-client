from marshmallow import Schema, fields
from marshmallow.validate import OneOf, Range


CURRENCY_CHOICES = ('RUB', 'USD', 'EUR', 'GBP')
CULTURE_NAME_CHOICES = ('ru-RU', 'en-US', 'lv', 'az',
                        'kk', 'uk', 'pl', 'vi', 'tr')


class PayerDataSchema(Schema):
    FirstName = fields.String()
    LastName = fields.String()
    MiddleName = fields.String()
    Address = fields.String()
    Birth = fields.String()
    City = fields.String()
    Country = fields.String()
    Phone = fields.String()
    Postcode = fields.String()


class JSONDataSchema(Schema):
    name = fields.String()
    firstName = fields.String()
    middleName = fields.String()
    lastName = fields.String()
    nick = fields.String()
    phone = fields.String()
    address = fields.String()
    comment = fields.String()
    birthDate = fields.String()


class CardChargeRequestSchema(Schema):
    Amount = fields.Number(required=True, validate=Range(min=0.01))
    Currency = fields.String(validate=OneOf(CURRENCY_CHOICES))
    IpAddress = fields.IP(required=True)
    CardCryptogramPacket = fields.String(required=True)
    Name = fields.String()
    PaymentUrl = fields.URL()
    InvoiceId = fields.String()
    Description = fields.String()
    CultureName = fields.String(validate=OneOf(CULTURE_NAME_CHOICES))
    AccountId = fields.String()
    Email = fields.Email()
    Payer = fields.Nested(PayerDataSchema)
    JsonData = fields.Nested(JSONDataSchema)
