import unittest  # 標準モジュールを読み込みます
from back.lambda_files.GetReservableList import lambda_function    # テスト対象のファイルを読み込みます

class TestA(unittest.TestCase):  # クラスを派生させて自分用のクラスを作ります
    def test_1(self):
        # self.assertEqual(lambda_function.get_available_slots({"20240420": ["11:00","11:15","11:30","11:45","12:00","12:15"], "20240421": ["13:00","13:15","13:30","13:45","14:00","15:15"]}, "00:15"), {"20240420": ["11:00","11:15","11:30","11:45","12:00","12:15"], "20240421": ["13:00","13:15","13:30","13:45","14:00","15:15"]})     # シナリオ1
        self.assertEqual(lambda_function.get_time_intervals("11:00", "20:00", 15), ["11:00","11:15","11:30","11:45","12:00","12:15","12:30","12:45","13:00","13:15","13:30","13:45","14:00","14:15","14:30","14:45","15:00","15:15","15:30","15:45","16:00","16:15","16:30","16:45","17:00","17:15","17:30","17:45","18:00","18:15","18:30","18:45","19:00","19:15","19:30","19:45"])     # シナリオ2
        # self.assertEqual(lambda_function.get_opening_hour(-1, -2), -3)  # シナリオ3

if __name__ == '__main__':
    unittest.main()
    