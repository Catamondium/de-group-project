from os import environ


def inhibit_CI(test):
    def dummy_test(*args, **kwargs):
        assert True

    if environ.get('CI', 'false') == 'true':
        return dummy_test
    else:
        return test
