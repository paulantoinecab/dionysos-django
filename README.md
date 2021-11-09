#  Dionysos Django Backend
[![Django CI](https://github.com/paulantoinecab/DionysosBack/actions/workflows/django.yml/badge.svg)](https://github.com/paulantoinecab/DionysosBack/actions/workflows/django.yml)
[![CodeQL](https://github.com/paulantoinecab/dionysos-django/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/paulantoinecab/dionysos-django/actions/workflows/codeql-analysis.yml)

Dionysos is a service made for restaurants to digitalize their menus.\
This is the backend project. It works using Python Django.\
It is easily deployable on Heroku. It works with Stripe and hosts images on Amazon S3.

# Main features
Dionysos manages Restaurants, Menus, Customers, Orders.\
Customers can order food directly after scanning a QR code associated to the table they are sitting at.

# Installation & environment variables
Install dependencies using `pip install -r requirements.txt`.\
Dionysos uses multiple environment variables : `DJANGO_SECRET_KEY`, `DATABASE_URL`, `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_STORAGE_BUCKET_NAME`, `AWS_S3_REGION_NAME`, `STRIPE_KEY`, `STRIPE_WEBHOOK_SECRET`
