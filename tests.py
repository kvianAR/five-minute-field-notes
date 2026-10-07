import io
import json
import unittest

from app import make_card


class FakeResponse(io.BytesIO):
    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.close()


class CardTests(unittest.TestCase):
    def test_returns_valid_model_card(self):
        def fake_open(request, timeout):
            self.assertIn(b'"model": "gemma3:1b"', request.data)
            self.assertEqual(timeout, 90)
            answer = {"message": {"content": json.dumps({
                "title": "A quiet minute", "cues": ["Hear a distant sound.", "Hear a close sound.", "Notice a rhythm."],
                "reflection": "What changed?"})}}
            return FakeResponse(json.dumps(answer).encode())
        card = make_card("balcony", "sounds", "seated", 5, opener=fake_open)
        self.assertEqual(len(card["cues"]), 3)
        self.assertEqual(card["model"], "gemma3:1b")

    def test_rejects_incomplete_card(self):
        def fake_open(*_args, **_kwargs):
            return FakeResponse(b'{"message":{"content":"{\\"title\\":\\"X\\",\\"cues\\":[],\\"reflection\\":\\"Y\\"}"}}')
        with self.assertRaisesRegex(ValueError, "incomplete"):
            make_card("park", "colors", "walking", 10, opener=fake_open)


if __name__ == "__main__":
    unittest.main()
