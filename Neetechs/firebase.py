# import os
# comment
# from firebase_admin import initialize_app
# from httplib2 import Credentials

# from Neetechs.settings import BASE_DIR

# PROJECT_APP = os.path.basename(BASE_DIR)
# cred = Credentials.Certificate(os.path.join(BASE_DIR, 'neetechs-c15eb-firebase-adminsdk-felkr-67494d9fd2.json'))
# """ asd
# cred = credentials.Certificate({
#     "type": "service_account",
#     "project_id": "fcm-test-88425",
#     "private_key_id": "7e066160a478354bf295ceb29d5e85451d1fdf0e",
#     "private_key": "notasecret",
#     "client_email": " neetechs@neetechs.iam.gserviceaccount.com",
#     "client_id": "102195091675521854172",
#     "auth_uri": "https://accounts.google.com/o/oauth2/auth",
#     "token_uri": "https://oauth2.googleapis.com/token",
#     "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
#     "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/neetechs@neetechs.iam.gserviceaccount.com"
# 	# "token_uri": "https://accounts.google.com/o/oauth2/token", 
# })"""
# FIREBASE_APP = initialize_app(cred)
# # Application definition
# GDAL_LIBRARY_PATH = '/app/.heroku/vendor/lib/libgdal.so'  # or os.getenv('...') and overriding it in Heroku app configuration

# FCM_DJANGO_SETTINGS = {
#      # default: _('FCM Django')
#     "APP_VERBOSE_NAME": "com.neetechs.neetechs",
#     "FCM_SERVER_KEY": "AAAAMcRsH18:APA91bHUFkxjF6_1TUxPp7xKbYqc0kJE8-7VHFW7wphsKGVmVSx_4f0caC9Hj-gs-ZOLLLKtT2GkkpBNru_F65NEnYiDXN5SKemokOxx8kveCrkhQDxfVkX0UnFHRTqtsyl-d73fMD44",

#      # true if you want to have only one active device per registered user at a time
#      # default: False
#     "ONE_DEVICE_PER_USER": False,
#      # devices to which notifications cannot be sent,
#      # are deleted upon receiving error response from FCM
#      # default: False
#     "DELETE_INACTIVE_DEVICES": True,
#     # Transform create of an existing Device (based on registration id) into
#                 # an update. See the section
#     # "Update of device with duplicate registration ID" for more details.
#     #"UPDATE_ON_DUPLICATE_REG_ID": True/False,
# }
# """
# PUSH_NOTIFICATIONS_SETTINGS = {
#         "FCM_API_KEY": "BNCtmc4v1pnhLS273oD48l1L-xDBLahcOfFlVuWxT3WQK85EEyPr7KkI7oFuyNfy1wt7wk5FvcD5MajaTVVxWRE",
#         "FCM_POST_URL": "https://fcm.googleapis.com/fcm/send",
#       #  "FCM_MAX_RECIPIENTS": "[your api key]",
#       #  "registration_ids ": "[your api key]",
#       #  "FCM_ERROR_TIMEOUT ": "[your api key]",
#       #  "WP_ERROR_TIMEOUT ": "[your api key]",

        
#       #  "GCM_API_KEY": "[your api key]",
#       #  "APNS_CERTIFICATE": "/path/to/your/certificate.pem",
#       #  "APNS_TOPIC": "com.example.push_test",
#       #  "WNS_PACKAGE_SECURITY_ID": "[your package security id, e.g: 'ms-app://e-3-4-6234...']",
#       #  "WNS_SECRET_KEY": "[your app secret key, e.g.: 'KDiejnLKDUWodsjmewuSZkk']",
#         "WP_PRIVATE_KEY": os.path.join(BASE_DIR, "private_key.pem"),
#         "WP_CLAIMS": {'sub': "mailto: info@neetechs.com"}
# }
# """