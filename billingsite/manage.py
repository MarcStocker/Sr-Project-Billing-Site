#!/cygdrive/c/Dropbox/Websites/Sr-Project-Billing-Site/codingenv/bin/env python3.4
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "billingsite.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError:
        # The above import may fail for some other reason. Ensure that the
        # issue is really that Django is missing to avoid masking other
        # exceptions on Python 2.
        import django
        raise
    execute_from_command_line(sys.argv)
