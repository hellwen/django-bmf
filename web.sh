#!/bin/bash

python develop.py migrate --noinput

python develop.py loaddata \
    fixtures/sites.json \
    fixtures/users.json \
    fixtures/demodata.json \
    fixtures/contrib_accounting.json \
    fixtures/contrib_invoice.json \
    fixtures/contrib_project.json \
    fixtures/contrib_quotation.json \
    fixtures/contrib_task.json \
    fixtures/contrib_team.json \
    fixtures/admin_dashboard.json 

python develop.py runserver rebuild_index --noinput

python develop.py runserver 0.0.0.0:8000
