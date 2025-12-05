# logging_config.py

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,

    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },

    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
        'accounts.views_otp': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    }
}
