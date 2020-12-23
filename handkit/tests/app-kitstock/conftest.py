import pytest


# @pytest.fixture(autouse=True)
# def enable_db_access_for_all_tests(db):
#     pass


@pytest.fixture(autouse=True)
def use_real_database(settings):
    print("use_real_database")
    settings.DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'handkit',
            'USER': 'root',
            'PASSWORD': 'nitb',
            'HOST': '127.0.0.1',
            'PORT': '3306',
        }
    }
