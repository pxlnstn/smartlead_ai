import unittest
from types import SimpleNamespace

from app.services.ai_service import AIService, AIServiceError


class FakeModels:
    async def generate_content(self, **_kwargs):
        return SimpleNamespace(text=None)


class FakeGeminiClient:
    def __init__(self) -> None:
        self.aio = SimpleNamespace(models=FakeModels())


class AiServiceTests(unittest.IsolatedAsyncioTestCase):
    async def test_empty_provider_response_becomes_service_error(self) -> None:
        service = AIService()
        service._gemini_client = FakeGeminiClient()

        with self.assertRaises(AIServiceError):
            await service.generate_response('Merhaba', [])


if __name__ == '__main__':
    unittest.main()
