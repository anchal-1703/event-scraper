import validators

def is_valid_email(email):
    return validators.email(email)

def is_valid_url(url):
    return validators.url(url)
