# -*- encoding=utf-8 -*-

import pytest

from normalize import normalize

#
# These tests are the reference tests for URI normalization
# from google.
#
# https://developers.google.com/safe-browsing/v4/urls-hashing
#
# Some of the test cases do not contain valid URIs
# and are not handled by our normalizer. These have been modified.
#


def test_normalize_google_0():
    assert 'http://host/%25' == normalize('http://host/%25%32%35')


def test_normalize_google_1():
    assert 'http://host/%25%25' == normalize('http://host/%25%32%35%25%32%35')


def test_normalize_google_2():
    assert 'http://host/%25' == normalize('http://host/%2525252525252525')


def test_normalize_google_3():
    assert 'http://host/asdf%25asd' == normalize('http://host/asdf%25%32%35asd')


def test_normalize_google_4():
    assert 'http://host/%25%25%25asd%25%25' == normalize('http://host/%%%25%32%35asd%%')


def test_normalize_google_5():
    assert 'http://www.google.com/' == normalize('http://www.google.com/')


def test_normalize_google_6():
    assert 'http://168.188.99.26/.secure/www.ebay.com/' == normalize('http://%31%36%38%2e%31%38%38%2e%39%39%2e%32%36/%2E%73%65%63%75%72%65/%77%77%77%2E%65%62%61%79%2E%63%6F%6D/') # noqa: 501


def test_normalize_google_7():
    assert 'http://195.127.0.11/uploads/%20%20%20%20/.verify/.eBaysecure=updateuserdataxplimnbqmn-xplmvalidateinfoswqpcmlx=hgplmcx/' == normalize('http://195.127.0.11/uploads/%20%20%20%20/.verify/.eBaysecure=updateuserdataxplimnbqmn-xplmvalidateinfoswqpcmlx=hgplmcx/') # noqa: 501


def test_normalize_google_8():
    with pytest.raises(ValueError):
        assert 'http://host%23.com/~a!b@c%23d$e%25f^00&11*22(33)44_55+' == normalize('http://host%23.com/%257Ea%2521b%2540c%2523d%2524e%25f%255E00%252611%252A22%252833%252944_55%252B') # noqa: 501


def test_normalize_google_8_mod():
    assert 'http://host.com/~a!b@c%23d$e%25f^00&11*22(33)44_55+' == normalize('http://host.com/%257Ea%2521b%2540c%2523d%2524e%25f%255E00%252611%252A22%252833%252944_55%252B') # noqa: 501


def test_normalize_google_9():
    assert 'http://195.127.0.11/blah' == normalize('http://3279880203/blah')


def test_normalize_google_10():
    assert 'http://www.google.com/' == normalize('http://www.google.com/blah/..')


def test_normalize_google_11():
    assert 'http://www.google.com/' == normalize('www.google.com/')


def test_normalize_google_12():
    assert 'http://www.google.com/' == normalize('www.google.com')


def test_normalize_google_13():
    assert 'http://www.evil.com/blah' == normalize('http://www.evil.com/blah#frag')


def test_normalize_google_14():
    assert 'http://www.google.com/' == normalize('http://www.GOOgle.com/')


def test_normalize_google_15():
    assert 'http://www.google.com/' == normalize('http://www.google.com.../')


def test_normalize_google_16():
    assert 'http://www.google.com/foobarbaz2' == normalize('http://www.google.com/foo\tbar\rbaz\n2')


def test_normalize_google_17():
    # assert 'http://www.google.com/q?' == normalize('http://www.google.com/q?')
    assert 'http://www.google.com/q' == normalize('http://www.google.com/q?')


def test_normalize_google_18():
    assert 'http://www.google.com/q?r?' == normalize('http://www.google.com/q?r?')


def test_normalize_google_19():
    assert 'http://www.google.com/q?r?s' == normalize('http://www.google.com/q?r?s')


def test_normalize_google_20():
    assert 'http://evil.com/foo' == normalize('http://evil.com/foo#bar#baz')


def test_normalize_google_21():
    assert 'http://evil.com/foo' == normalize('http://evil.com/foo')


def test_normalize_google_22():
    assert 'http://evil.com/foo?bar' == normalize('http://evil.com/foo?bar')


def test_normalize_google_23():
    # '%01%80' is not a valid hostname and our normalizer recognizes that.
    with pytest.raises(ValueError):
        assert 'http://%01%C2%80.com/' == normalize('http://\x01\x80.com/')


def test_normalize_google_24():
    assert 'http://notrailingslash.com/' == normalize('http://notrailingslash.com')


def test_normalize_google_25():
    assert 'http://www.gotaport.com/' == normalize('http://www.gotaport.com:1234/')


def test_normalize_google_26():
    assert 'http://www.google.com/' == normalize('  http://www.google.com/  ')


def test_normalize_google_27():
    # ' leadingspace.com' is not a valid hostname and our normalizer recognizes that.
    with pytest.raises(ValueError):
        assert 'http://%20leadingspace.com/' == normalize('http:// leadingspace.com/')


def test_normalize_google_28():
    # ' leadingspace.com' is not a valid hostname and our normalizer recognizes that.
    with pytest.raises(ValueError):
        assert 'http://%20leadingspace.com/' == normalize('http://%20leadingspace.com/')


def test_normalize_google_29():
    # ' leadingspace.com' is not a valid hostname and our normalizer recognizes that.
    with pytest.raises(ValueError):
        assert 'http://%20leadingspace.com/' == normalize('%20leadingspace.com/')


def test_normalize_google_30():
    assert 'https://www.securesite.com/' == normalize('https://www.securesite.com/')


def test_normalize_google_31():
    assert 'http://host.com/ab%23cd' == normalize('http://host.com/ab%23cd')


def test_normalize_google_32():
    assert 'http://host.com/twoslashes?more//slashes' == normalize('http://host.com//twoslashes?more//slashes')
