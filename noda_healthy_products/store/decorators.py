from django.contrib.auth.decorators import user_passes_test


def verification_required(f):
    return user_passes_test(lambda u: u.is_active, login_url='/verify')(f)