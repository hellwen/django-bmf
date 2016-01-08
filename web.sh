#!/bin/bash

# Give the database time to spin up
sleep 5

python manage.py migrate --noinput || exit 1

python manage.py loaddata \
    fixtures/sites.json \
    fixtures/users.json \
    fixtures/demodata.json \
    fixtures/contrib_accounting.json \
    fixtures/contrib_invoice.json \
    fixtures/contrib_project.json \
    fixtures/contrib_quotation.json \
    fixtures/contrib_task.json \
    fixtures/contrib_team.json \
    fixtures/admin_dashboard.json \
    || exit 1

uwsgi \
  --http :8000 \
  --module sandbox.wsgi \
  --enable-threads \
  --master \
  --workers 4 \
  --threads 2 \
  --vacuum \
  --die-on-term \
  --need-app \
  --reload-on-exception \
  --no-threads-wait \
  --disable-logging \
  --python-autoreload 5
