#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    import create_admin_user
    # os.environ.setdefault("DJANGO_SETTINGS_MODULE", "schilderen_site.settings.production")
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "schilderen_site.settings.dev")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
