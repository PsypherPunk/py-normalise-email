import pytest

from normalise.email import normalise_email


@pytest.mark.parametrize(
    "email,expected",
    [
        ("test@me.com", "test@me.com"),
        ("some.name@gmail.com", "somename@gmail.com"),
        ("some.name@googleMail.com", "somename@gmail.com"),
        ("some.name+extension@gmail.com", "somename@gmail.com"),
        ("some.Name+extension@GoogleMail.com", "somename@gmail.com"),
        ("some.name.middleName+extension@gmail.com", "somenamemiddlename@gmail.com"),
        (
            "some.name.middleName+extension@GoogleMail.com",
            "somenamemiddlename@gmail.com",
        ),
        ("some.name.midd.leNa.me.+extension@gmail.com", "somenamemiddlename@gmail.com"),
        (
            "some.name.midd.leNa.me.+extension@GoogleMail.com",
            "somenamemiddlename@gmail.com",
        ),
        ("some.name+extension@unknown.com", "some.name+extension@unknown.com"),
        ("hans@m端ller.com", "hans@m端ller.com"),
        (
            "some.name.midd..leNa...me...+extension@GoogleMail.com",
            "somenamemidd..lena...me...@gmail.com",
        ),
        ("matthew..example@gmail.com", "matthew..example@gmail.com"),
        ('"foo@bar"@baz.com', '"foo@bar"@baz.com'),
        ("test@ya.ru", "test@yandex.ru"),
        ("test@yandex.kz", "test@yandex.ru"),
        ("test@yandex.ru", "test@yandex.ru"),
        ("test@yandex.ua", "test@yandex.ru"),
        ("test@yandex.com", "test@yandex.ru"),
        ("test@yandex.by", "test@yandex.ru"),
        ("@gmail.com", False),
        ("@icloud.com", False),
        ("@outlook.com", False),
        ("@yahoo.com", False),
    ],
)
def test_normalise_email(email: str, expected: str):
    """
    Tests taken from here:
    https://github.com/validatorjs/validator.js/blob/master/test/sanitizers.js#L288
    """
    assert normalise_email(email) == expected


@pytest.mark.parametrize(
    "email,expected",
    [
        ("test@foo.com", "test@foo.com"),
        ("hans@m端ller.com", "hans@m端ller.com"),
        ("test@FOO.COM", "test@foo.com"),  # Hostname is always lowercased
        ("blAH@x.com", "blAH@x.com"),
        # In case of domains that are known to be case-insensitive, there's a separate switch
        ("TEST@me.com", "test@me.com"),
        ("TEST@ME.COM", "test@me.com"),
        ("SOME.name@GMAIL.com", "somename@gmail.com"),
        (
            "SOME.name.middleName+extension@GoogleMail.com",
            "somenamemiddlename@gmail.com",
        ),
        ("SOME.name.midd.leNa.me.+extension@gmail.com", "somenamemiddlename@gmail.com"),
        ("SOME.name@gmail.com", "somename@gmail.com"),
        ("SOME.name@yahoo.ca", "some.name@yahoo.ca"),
        ("SOME.name@outlook.ie", "some.name@outlook.ie"),
        ("SOME.name@me.com", "some.name@me.com"),
        ("SOME.name@yandex.ru", "some.name@yandex.ru"),
    ],
)
def test_normalise_email_all_lowercase_false(email: str, expected: str):
    """
    Tests taken from here:
    https://github.com/validatorjs/validator.js/blob/master/test/sanitizers.js#L320

    "Testing all_lowercase switch, should apply to domains not known to
    be case-insensitive."
    """
    normalised = normalise_email(
        email,
        all_lowercase=False,
    )
    assert normalised == expected


@pytest.mark.parametrize(
    "email,expected",
    [
        ("TEST@FOO.COM", "TEST@foo.com"),  # all_lowercase
        ("ME@gMAil.com", "ME@gmail.com"),  # gmail_lowercase
        ("ME@me.COM", "ME@me.com"),  # icloud_lowercase
        ("ME@icloud.COM", "ME@icloud.com"),  # icloud_lowercase
        ("ME@outlook.COM", "ME@outlook.com"),  # outlookdotcom_lowercase
        ("JOHN@live.CA", "JOHN@live.ca"),  # outlookdotcom_lowercase
        ("ME@ymail.COM", "ME@ymail.com"),  # yahoo_lowercase
        ("ME@yandex.RU", "ME@yandex.ru"),  # yandex_lowercase
    ],
)
def test_normalise_email_every_lowercase_false(email: str, expected: str):
    """
    Tests taken from here:
    https://github.com/validatorjs/validator.js/blob/master/test/sanitizers.js#L343

    "Testing *_lowercase."
    """
    normalised = normalise_email(
        email,
        all_lowercase=False,
        gmail_lowercase=False,
        icloud_lowercase=False,
        outlookdotcom_lowercase=False,
        yahoo_lowercase=False,
        yandex_lowercase=False,
    )
    assert normalised == expected


@pytest.mark.parametrize(
    "email,expected",
    [
        ("TEST@FOO.COM", "test@foo.com"),  # all_lowercase
        ("ME@gMAil.com", "me@gmail.com"),  # gmail_lowercase
        ("ME@me.COM", "me@me.com"),  # icloud_lowercase
        ("ME@icloud.COM", "me@icloud.com"),  # icloud_lowercase
        ("ME@outlook.COM", "me@outlook.com"),  # outlookdotcom_lowercase
        ("JOHN@live.CA", "john@live.ca"),  # outlookdotcom_lowercase
        ("ME@ymail.COM", "me@ymail.com"),  # yahoo_lowercase
    ],
)
def test_normalise_email_every_lowercase_override(email: str, expected: str):
    """
    Tests taken from here:
    https://github.com/validatorjs/validator.js/blob/master/test/sanitizers.js#L367

    "Should overwrite all the *_lowercase options."
    """
    normalised = normalise_email(
        email,
        all_lowercase=True,
        gmail_lowercase=False,
        icloud_lowercase=False,
        outlookdotcom_lowercase=False,
        yahoo_lowercase=False,
    )
    assert normalised == expected


@pytest.mark.parametrize(
    "email,expected",
    [
        ("SOME.name@GMAIL.com", "some.name@gmail.com"),
        ("SOME.name+me@GMAIL.com", "some.name@gmail.com"),
        ("my.self@foo.com", "my.self@foo.com"),
    ],
)
def test_normalise_email_remove_dots_false(email: str, expected: str):
    """
    Tests taken from here:
    https://github.com/validatorjs/validator.js/blob/master/test/sanitizers.js#L388
    """
    normalised = normalise_email(
        email,
        gmail_remove_dots=False,
    )
    assert normalised == expected


@pytest.mark.parametrize(
    "email,expected",
    [
        ("SOME.name@GMAIL.com", "somename@gmail.com"),
        ("SOME.name+me@GMAIL.com", "somename@gmail.com"),
        ("some.name..multiple@gmail.com", "somename..multiple@gmail.com"),
        ("my.self@foo.com", "my.self@foo.com"),
    ],
)
def test_normalise_email_remove_dots_true(email: str, expected: str):
    """
    Tests taken from here:
    https://github.com/validatorjs/validator.js/blob/master/test/sanitizers.js#L400
    """
    normalised = normalise_email(
        email,
        gmail_remove_dots=True,
    )
    assert normalised == expected


@pytest.mark.parametrize(
    "email,expected",
    [
        ("foo+bar@unknown.com", "foo+bar@unknown.com"),
        ("foo+bar@gmail.com", "foo+bar@gmail.com"),  # gmail_remove_subaddress
        ("foo+bar@me.com", "foo+bar@me.com"),  # icloud_remove_subaddress
        ("foo+bar@icloud.com", "foo+bar@icloud.com"),  # icloud_remove_subaddress
        ("foo+bar@live.fr", "foo+bar@live.fr"),  # outlookdotcom_remove_subaddress
        (
            "foo+bar@hotmail.co.uk",
            "foo+bar@hotmail.co.uk",
        ),  # outlookdotcom_remove_subaddress
        ("foo-bar@yahoo.com", "foo-bar@yahoo.com"),  # yahoo_remove_subaddress
        ("foo+bar@yahoo.com", "foo+bar@yahoo.com"),  # yahoo_remove_subaddress
    ],
)
def test_normalise_email_remove_subaddress_false(email: str, expected: str):
    """
    Tests taken from here:
    https://github.com/validatorjs/validator.js/blob/master/test/sanitizers.js#L413
    """
    normalised = normalise_email(
        email,
        gmail_remove_subaddress=False,
        icloud_remove_subaddress=False,
        outlookdotcom_remove_subaddress=False,
        yahoo_remove_subaddress=False,
    )
    assert normalised == expected


@pytest.mark.parametrize(
    "email,expected",
    [
        ("foo+bar@unknown.com", "foo+bar@unknown.com"),
        ("foo+bar@gmail.com", "foo@gmail.com"),  # gmail_remove_subaddress
        ("foo+bar@me.com", "foo@me.com"),  # icloud_remove_subaddress
        ("foo+bar@icloud.com", "foo@icloud.com"),  # icloud_remove_subaddress
        ("foo+bar@live.fr", "foo@live.fr"),  # outlookdotcom_remove_subaddress
        (
            "foo+bar@hotmail.co.uk",
            "foo@hotmail.co.uk",
        ),  # outlookdotcom_remove_subaddress
        ("foo-bar@yahoo.com", "foo@yahoo.com"),  # yahoo_remove_subaddress
        ("foo+bar@yahoo.com", "foo+bar@yahoo.com"),  # yahoo_remove_subaddress
    ],
)
def test_normalise_email_remove_subaddress_true(email: str, expected: str):
    """
    Tests taken from here:
    https://github.com/validatorjs/validator.js/blob/master/test/sanitizers.js#L434
    """
    normalised = normalise_email(
        email,
        gmail_remove_subaddress=True,
        icloud_remove_subaddress=True,
        outlookdotcom_remove_subaddress=True,
        yahoo_remove_subaddress=True,
    )
    assert normalised == expected


@pytest.mark.parametrize(
    "email,expected",
    [
        ("SOME.name@GMAIL.com", "somename@gmail.com"),
        ("SOME.name+me@GMAIL.com", "somename@gmail.com"),
        ("SOME.name+me@googlemail.com", "somename@googlemail.com"),
        ("SOME.name+me@googlemail.COM", "somename@googlemail.com"),
        ("SOME.name+me@googlEmail.com", "somename@googlemail.com"),
        ("my.self@foo.com", "my.self@foo.com"),
    ],
)
def test_normalise_email_gmail_convert_googlemaildotcom_false(
    email: str, expected: str
):
    """
    Tests taken from here:
    https://github.com/validatorjs/validator.js/blob/master/test/sanitizers.js#L454
    """
    normalised = normalise_email(
        email,
        gmail_convert_googlemaildotcom=False,
    )
    assert normalised == expected


@pytest.mark.parametrize(
    "email,expected",
    [
        ("SOME.name@GMAIL.com", "somename@gmail.com"),
        ("SOME.name+me@GMAIL.com", "somename@gmail.com"),
        ("SOME.name+me@googlemail.com", "somename@gmail.com"),
        ("SOME.name+me@googlemail.COM", "somename@gmail.com"),
        ("SOME.name+me@googlEmail.com", "somename@gmail.com"),
        ("my.self@foo.com", "my.self@foo.com"),
    ],
)
def test_normalise_email_gmail_convert_googlemaildotcom_true(email: str, expected: str):
    """
    Tests taken from here:
    https://github.com/validatorjs/validator.js/blob/master/test/sanitizers.js#L470
    """
    normalised = normalise_email(
        email,
        gmail_convert_googlemaildotcom=True,
    )
    assert normalised == expected
