# -*- encoding=utf-8 -*-

__all__ = ['HOTP']

import hashlib
import hmac
import unittest


class HOTP(object):
    """
        Implementation of RFC4226
        HOTP: An HMAC-Based One-Time Password Algorithm

        The algorithm requires a shared secret and a clock value
        It calculates an integer number, the one time password.

        Example:

        hotp = HOTP(secret=b'12345678901234567890', digits=6)
        password = hotp.value(clock)

    """
    # The index value of the byte in the
    # calculated hash sequence to use as offset byte
    offset_index = -1
    # the MASK to apply to the offset value
    # before indexing the hash byte sequence
    offset_mask = 0x0f

    # the number of bytes to use as
    extract_length = 4
    # the HMAC to use. RFC4226 requires SHA1
    digest = hashlib.sha1

    def __init__(self, secret, digits):
        """
            Parameters:

            - SECRET: The HOTP shared secret
            - DIGITS: The maximum number of decimal digits for the
              final HOTP value.
              The value is calculated module (10 ** DIGITS)
        """
        self.secret = secret
        self.digits = digits

    def dynamic_truncate(self, s):
        offset = s[self.offset_index] & self.offset_mask
        p = int.from_bytes(s[offset:offset + self.extract_length], 'big')
        return p & 0x7fffffff

    def hmac(self, clock):
        """
            calculate the intermediate HOTP HMAC.

            This is mainly a separate method since
            the hmac values are needed for testing.

            Parameters:

            - CLOCK: the clock value.
              This must either be an 8 byte sequence (suitable for
              passing to `bytes()`) or an integer value.

            Returns:
            - The raw HMAC digest value.
        """
        if isinstance(clock, int):
            clock = clock.to_bytes(8, 'big')
        else:
            clock = bytes(clock)
        if len(clock) != 8:
            raise ValueError('Clock must have length 8')

        mac = hmac.HMAC(self.secret, clock, digestmod=self.digest)
        hs = mac.digest()
        return hs

    def value(self, clock, digest=None):
        """
            Parameters:

            - CLOCK: the clock value.
              This must either be an 8 byte sequence (suitable for
              passing to `bytes()`) or an integer value.

            Returns:

            An integer (modulo DIGITS) representing the calculated HOTP value.
        """
        hs = self.hmac(clock)
        d = self.dynamic_truncate(hs)
        return d % (10 ** self.digits)


class TestHOTP(unittest.TestCase):
    secret = b'12345678901234567890'
    digits = 6

    def test_rfc4226_hmac(self):
        # these are the HMAC test values from RFC4226
        clock_hmac = [
            (0, 'cc93cf18508d94934c64b65d8ba7667fb7cde4b0'),
            (1, '75a48a19d4cbe100644e8ac1397eea747a2d33ab'),
            (2, '0bacb7fa082fef30782211938bc1c5e70416ff44'),
            (3, '66c28227d03a2d5529262ff016a1e6ef76557ece'),
            (4, 'a904c900a64b35909874b33e61c5938a8e15ed1c'),
            (5, 'a37e783d7b7233c083d4f62926c7a25f238d0316'),
            (6, 'bc9cd28561042c83f219324d3c607256c03272ae'),
            (7, 'a4fb960c0bc06e1eabb804e5b397cdc4b45596fa'),
            (8, '1b3c89f65e6c9e883012052823443f048b4332db'),
            (9, '1637409809a679dc698207310c8c7fc07290d9e5'),
        ]
        hotp = HOTP(self.secret, self.digits)
        for clock, hex_hmac in clock_hmac:
            self.assertEqual(hex_hmac, hotp.hmac(clock).hex())

    def test_rfc4226_hotp(self):
        # these are the HOTP test values from RFC4226
        clock_hotp = [
            (0, 755224),
            (1, 287082),
            (2, 359152),
            (3, 969429),
            (4, 338314),
            (5, 254676),
            (6, 287922),
            (7, 162583),
            (8, 399871),
            (9, 520489),
        ]
        hotp = HOTP(self.secret, self.digits)
        for clock, value in clock_hotp:
            self.assertEqual(value, hotp.value(clock))


if __name__ == '__main__':
    unittest.main()
