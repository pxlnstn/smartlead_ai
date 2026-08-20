import unittest
from unittest.mock import AsyncMock, patch

from fastapi.testclient import TestClient

from app import create_app
from app.database import get_db


class FakeDatabaseSession:
    def __init__(self) -> None:
        self.added = []

    def add(self, item) -> None:
        self.added.append(item)

    async def flush(self) -> None:
        for index, item in enumerate(self.added, start=1):
            item.id = index


async def fake_db_dependency():
    yield FakeDatabaseSession()


class ApiContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.app = create_app()
        self.app.dependency_overrides[get_db] = fake_db_dependency
        self.client = TestClient(self.app)

    def tearDown(self) -> None:
        self.client.close()
        self.app.dependency_overrides.clear()

    def test_health_contract(self) -> None:
        response = self.client.get('/health')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'healthy')

    def test_chat_contract(self) -> None:
        with (
            patch('app.security.WIX_API_KEY', 'wix-secret'),
            patch(
                'app.routes.ai_service.generate_response',
                new=AsyncMock(return_value='ino yüz şeklini analiz ederek öneriler sunar.'),
            ),
        ):
            response = self.client.post(
                '/api/chat',
                json={'message': 'ino nasıl çalışır?', 'history': []},
                headers={'X-Wix-Key': 'wix-secret'},
            )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], True)
        self.assertIn('yüz şeklini', response.json()['response'])

    def test_contact_contract(self) -> None:
        with patch('app.security.WIX_API_KEY', 'wix-secret'):
            response = self.client.post(
                '/api/contact',
                json={
                    'name': 'Pelin',
                    'number': '+90 555 123 45 67',
                    'note': 'Demo talep ediyorum.',
                },
                headers={'X-Wix-Key': 'wix-secret'},
            )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()['success'], True)

    def test_chat_and_contact_are_not_directly_public(self) -> None:
        with patch('app.security.WIX_API_KEY', 'wix-secret'):
            chat_response = self.client.post('/api/chat', json={'message': 'Merhaba'})
            contact_response = self.client.post(
                '/api/contact',
                json={'name': 'Pelin', 'number': '+90 555 123 45 67'},
            )
        self.assertEqual(chat_response.status_code, 401)
        self.assertEqual(contact_response.status_code, 401)

    def test_leads_are_not_public(self) -> None:
        with patch('app.security.ADMIN_API_KEY', 'server-secret'):
            response = self.client.get('/api/leads')
        self.assertEqual(response.status_code, 401)


if __name__ == '__main__':
    unittest.main()
