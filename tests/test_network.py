from app.services.tdx.network import signature

from unittest import TestCase


class TestNetwork(TestCase):
    async def test_signature(self):
        self.assertEqual(
            signature(
                'bodystring',
                'secret_key'
            ),
            'lwSWI7Dl0gv2vrUxPYBgDj1qvlY='
        )
