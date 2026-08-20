import unittest
from unittest.mock import patch

from fastapi import HTTPException

from app.security import require_admin_api_key, require_wix_api_key


class AdminSecurityTests(unittest.IsolatedAsyncioTestCase):
    async def test_missing_server_key_fails_closed(self) -> None:
        with patch("app.security.ADMIN_API_KEY", None):
            with self.assertRaises(HTTPException) as raised:
                await require_admin_api_key("anything")
        self.assertEqual(raised.exception.status_code, 503)

    async def test_missing_or_wrong_header_is_unauthorized(self) -> None:
        with patch("app.security.ADMIN_API_KEY", "expected-secret"):
            for supplied in (None, "wrong-secret"):
                with self.subTest(supplied=supplied):
                    with self.assertRaises(HTTPException) as raised:
                        await require_admin_api_key(supplied)
                    self.assertEqual(raised.exception.status_code, 401)

    async def test_matching_header_is_allowed(self) -> None:
        with patch("app.security.ADMIN_API_KEY", "expected-secret"):
            result = await require_admin_api_key("expected-secret")
        self.assertIsNone(result)

    async def test_wix_key_fails_closed_and_accepts_only_match(self) -> None:
        with patch("app.security.WIX_API_KEY", None):
            with self.assertRaises(HTTPException) as missing:
                await require_wix_api_key("anything")
        self.assertEqual(missing.exception.status_code, 503)

        with patch("app.security.WIX_API_KEY", "wix-secret"):
            with self.assertRaises(HTTPException) as wrong:
                await require_wix_api_key("wrong")
            allowed = await require_wix_api_key("wix-secret")
        self.assertEqual(wrong.exception.status_code, 401)
        self.assertIsNone(allowed)


if __name__ == "__main__":
    unittest.main()
