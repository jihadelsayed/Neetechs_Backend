prod = {
    "active": true,
    "attributes": [],
    "created": 1622590352,
    "description": null,
    "id": "prod_Jasq4hztjKKqsR",
    "images": [],
    "livemode": false,
    "metadata": {},
    "name": "fdgfdg",
    "object": "product",
    "package_dimensions": null,
    "shippable": null,
    "statement_descriptor": null,
    "type": "service",
    "unit_label": null,
    "updated": 1622590352,
    "url": null
}

ds = {
    "address": null,
    "balance": 0,
    "created": 1622595476,
    "currency": null,
    "default_source": null,
    "delinquent": false,
    "description": null,
    "discount": null,
    "email": "jihad.safffffhhgjfggffffhffffggyed.1hgjhg996@gmafffil.com",
    "id": "cus_JauDyJAWDO5scB",
    "invoice_prefix": "0DDE9A8E",
    "invoice_settings": {
        "custom_fields": null,
        "default_payment_method": "pm_1IxiPAIR19rXEZpR03IqqpiB",
        "footer": null
    },
    "livemode": false,
    "metadata": {},
    "name": null,
    "object": "customer",
    "phone": null,
    "preferred_locales": [],
    "shipping": null,
    "tax_exempt": "none"
}

SubscriptionOptionssubscriptionType = (
    ('groundplan', 'GroundPlan'),
    ('premiumplanmonthly', 'premiumplanMonthly'),
    ('premiumplanyearly', 'PremiumPlanYearly'),
)

sor = {'object': {
  'id': 'cs_test_a1PnKX8hIzCalSPMUUfuSYsUvaOeK86kZoNnVicttuhSuwdaIZ0Zyv9QCL', 'object': 'checkout.session', 'allow_promotion_codes': None, 'amount_subtotal': 49900, 'amount_total': 49900

, 'billing_address_collection': None, 'cancel_url': 'https://www.neetechs.com/CheckoutUnsuccess', 'client_reference_id': None, 'currency': 'sek', 'customer': 'cus_Je3mpoTyimQ8Z2', 'customer_details': {'email': 'david.pales1@gmail.com', 'tax_exempt': 'none', 'tax_ids': []},
                  'customer_email': 'david.pales1@gmail.com', 'livemode': False, 'locale': None, 'metadata': {}
                  
                  , 'mode': 'subscription', 'payment_intent': None, 'payment_method_options': {}
                  , 'payment_method_types': ['card']
                  , 'payment_status': 'paid'
                  , 'setup_intent': None
                  , 'shipping': None
                  , 'shipping_address_collection': None
                  , 'submit_type': None
                  , 'subscription': 'sub_Je3mwzxR1TnM2K'
                  , 'success_url': 'https://www.neetechs.com/CheckoutSuccess'
                  , 'total_details': {'amount_discount': 0, 'amount_shipping': 0, 'amount_tax': 0}}}
hello = {
  'object': 
    {
      'id': 'in_1J0lfPIR19rXEZpR4zlSGTJf', 'object': 'invoice', 'account_country': 'SE', 'account_name': 'neetechs', 'account_tax_ids': None, 'amount_due': 49900, 'amount_paid': 49900, 'amount_remaining': 0, 'application_fee_amount': None, 'attempt_count': 1, 'attempted': True, 'auto_advance': False, 'billing_reason': 'subscription_create', 'charge': 'ch_1J0lfQIR19rXEZpRUP9rAs4E', 'collection_method': 'charge_automatically', 'created': 1623322999, 'currency': 'sek', 'custom_fields': None, 'customer': 'cus_Je3mpoTyimQ8Z2', 'customer_address': None, 'customer_email': 'david.pales1@gmail.com', 'customer_name': 'dfgfdfdg', 'customer_phone': None, 'customer_shipping': None, 'customer_tax_exempt': 'none', 'customer_tax_ids': [], 'default_payment_method': None, 'default_source': None, 'default_tax_rates': [], 'description': None, 'discount': None, 'discounts': [], 'due_date': None, 'ending_balance': 0, 'footer': None, 'hosted_invoice_url': 'https://invoice.stripe.com/i/acct_1IwTvvIR19rXEZpR/invst_Je3mi6RKKBmt37GOvnC4OwQsGFN0IDm', 'invoice_pdf': 'https://pay.stripe.com/invoice/acct_1IwTvvIR19rXEZpR/invst_Je3mi6RKKBmt37GOvnC4OwQsGFN0IDm/pdf', 'last_finalization_error': None, 'lines': 
      {'object': 'list', 'data': 
      [{
        'id': 'il_1J0lfPIR19rXEZpRLHt1XezK', 'object': 'line_item', 'amount': 49900, 'currency': 'sek', 'description': '1 × Premie Plan årlig (at 499.00 kr / year)', 'discount_amounts': [], 'discountable': True, 'discounts': [], 'livemode': False, 'metadata': {}, 'period': {'end': 1654858999, 'start': 1623322999}, 'plan': {'id': 'price_1J0BvUIR19rXEZpRxx9XjMLu', 'object': 'plan', 'active': True, 'aggregate_usage': None, 'amount': 49900, 'amount_decimal': '49900', 'billing_scheme': 'per_unit', 'created': 1623185612, 'currency': 'sek', 'interval': 'year', 'interval_count': 1, 'livemode': False
      , 'metadata': {} , 'nickname': None, 'product': 'prod_JdSrhXGYWZ1SRd', 'tiers_mode': None, 'transform_usage': None, 'trial_period_days': None, 'usage_type': 'licensed'}
, 'price': {'id': 'price_1J0BvUIR19rXEZpRxx9XjMLu', 'object': 'price', 'active': True, 'billing_scheme': 'per_unit', 'created': 1623185612, 'currency': 'sek', 'livemode': False, 'lookup_key': None, 'metadata': {}, 'nickname': None, 'product': 'prod_JdSrhXGYWZ1SRd', 'recurring': {'aggregate_usage': None, 'interval': 'year', 'interval_count': 1, 'trial_period_days': None, 'usage_type': 'licensed'}, 'tiers_mode': None, 'transform_quantity': None, 'type': 'recurring', 'unit_amount': 49900, 'unit_amount_decimal': '49900'}, 'proration': False, 'quantity': 1, 'subscription': 'sub_Je3mwzxR1TnM2K', 'subscription_item': 'si_Je3mIJOjYVZk5L', 'tax_amounts': [], 'tax_rates': [], 'type': 'subscription'}], 'has_more': False, 'total_count': 1, 'url': '/v1/invoices/in_1J0lfPIR19rXEZpR4zlSGTJf/lines'}, 'livemode': False, 'metadata': {}, 'next_payment_attempt': None, 'number': '02C67453-0007', 'on_behalf_of': None, 'paid': True, 'payment_intent': 'pi_1J0lfPIR19rXEZpRBHxVkq4v', 'payment_settings': {'payment_method_options': None, 'payment_method_types': None}, 'period_end': 1623322999, 'period_start': 1623322999, 'post_payment_credit_notes_amount': 0, 'pre_payment_credit_notes_amount': 0, 'receipt_number': None, 'starting_balance': 0, 'statement_descriptor': None, 'status': 'paid', 'status_transitions': {'finalized_at': 1623322999, 'marked_uncollectible_at': None, 'paid_at': 1623323000, 'voided_at': None}
, 'subscription': 'sub_Je3mwzxR1TnM2K', 'subtotal': 49900, 'tax': None, 'total': 49900, 'total_discount_amounts': [], 'total_tax_amounts': [], 'transfer_data': None, 'webhooks_delivered_at': 1623322999
}
}
