import unittest
from app.prompt.domain.model.openai_response_text import OpenaiResponseText


class OpenaiResponseTextTest(unittest.TestCase):
    def test_JSON形式の文字列を変換する(self):
        # Given
        text = "{\"result\": \"[{\\\"order\\\":1,\\\"title\\\":\\\"オープニングマッチ\\\",\\\"original_title\\\":\\\"オープニングマッチ\\\",\\\"wrestlers\\\":[\\\"上原わかな\\\",\\\"HIMAWARI\\\"]},{\\\"order\\\":2,\\\"title\\\":\\\"第二試合\\\",\\\"original_title\\\":\\\"第二試合\\\",\\\"wrestlers\\\":[\\\"上福ゆき\\\",\\\"角田奈穂\\\",\\\"桐生真弥\\\",\\\"らく\\\",\\\"猫はるな\\\",\\\"鳥喰かや\\\"]},{\\\"order\\\":3,\\\"title\\\":\\\"第三試合\\\",\\\"original_title\\\":\\\"第三試合\\\",\\\"wrestlers\\\":[\\\"宮本もか\\\",\\\"遠藤有栖\\\"]},{\\\"order\\\":4,\\\"title\\\":\\\"第四試合\\\",\\\"original_title\\\":\\\"第四試合\\\",\\\"wrestlers\\\":[\\\"荒井優希\\\",\\\"原宿ぽむ\\\"]},{\\\"order\\\":5,\\\"title\\\":\\\"第五試合\\\",\\\"original_title\\\":\\\"第五試合\\\",\\\"wrestlers\\\":[\\\"辰巳リカ\\\",\\\"愛野ユキ\\\",\\\"乃蒼ヒカリ\\\",\\\"ジャナイ・カイ\\\"]},{\\\"order\\\":6,\\\"title\\\":\\\"セミファイナル\\\",\\\"original_title\\\":\\\"セミファイナル\\\",\\\"wrestlers\\\":[\\\"坂崎ユカ\\\",\\\"瑞希\\\",\\\"渡辺未詩\\\",\\\"鈴芽\\\"]},{\\\"order\\\":7,\\\"title\\\":\\\"トーナメント決勝戦\\\",\\\"original_title\\\":\\\"メインイベント　トーナメント決勝戦\\\",\\\"wrestlers\\\":[\\\"山下実優\\\",\\\"伊藤麻希\\\",\\\"中島翔子\\\",\\\"ハイパーミサヲ\\\"]}]\"}"

        # When
        actual_json = OpenaiResponseText.from_raw_text(text).to_json()
        actual_result = actual_json["result"]

        # Then
        expected_result = "[{\"order\":1,\"title\":\"オープニングマッチ\",\"original_title\":\"オープニングマッチ\",\"wrestlers\":[\"上原わかな\",\"HIMAWARI\"]},{\"order\":2,\"title\":\"第二試合\",\"original_title\":\"第二試合\",\"wrestlers\":[\"上福ゆき\",\"角田奈穂\",\"桐生真弥\",\"らく\",\"猫はるな\",\"鳥喰かや\"]},{\"order\":3,\"title\":\"第三試合\",\"original_title\":\"第三試合\",\"wrestlers\":[\"宮本もか\",\"遠藤有栖\"]},{\"order\":4,\"title\":\"第四試合\",\"original_title\":\"第四試合\",\"wrestlers\":[\"荒井優希\",\"原宿ぽむ\"]},{\"order\":5,\"title\":\"第五試合\",\"original_title\":\"第五試合\",\"wrestlers\":[\"辰巳リカ\",\"愛野ユキ\",\"乃蒼ヒカリ\",\"ジャナイ・カイ\"]},{\"order\":6,\"title\":\"セミファイナル\",\"original_title\":\"セミファイナル\",\"wrestlers\":[\"坂崎ユカ\",\"瑞希\",\"渡辺未詩\",\"鈴芽\"]},{\"order\":7,\"title\":\"トーナメント決勝戦\",\"original_title\":\"メインイベント　トーナメント決勝戦\",\"wrestlers\":[\"山下実優\",\"伊藤麻希\",\"中島翔子\",\"ハイパーミサヲ\"]}]"
        self.assertEqual(actual_result, expected_result)
