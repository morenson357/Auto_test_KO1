import time
import AutoTest2_1pmi
import AutoTest2_2pmi
import AutoTest2_3pmi
import AutoTest2_4pmi
import AutoTest2_5pmi
import AutoTest3_1pmi
import AutoTest4_1pmi

TESTS = [
    ("AutoTest2.1", AutoTest2_1pmi.run_test),
    ("AutoTest2.2", AutoTest2_2pmi.run_test),
    ("AutoTest2.3", AutoTest2_3pmi.run_test),
    ("AutoTest2.4", AutoTest2_4pmi.run_test),
    ("AutoTest2.5", AutoTest2_5pmi.run_test),
    ("AutoTest3.1", AutoTest3_1pmi.run_test),
    ("AutoTest4.1", AutoTest4_1pmi.run_test)
]


def run_all_tests():
    for test_name, test_function in TESTS:
        print(f"\nЗапуск теста: {test_name}...")
        try:
            test_function()
        except Exception as e:
            print(f"Ошибка при выполнении теста {test_name}: {e}")

        # Пауза между запуском
        time.sleep(2)


if __name__ == "__main__":
    print("Начало выполнения всех автотестов...")
    run_all_tests()
    print("\nВсе автотесты завершены.")