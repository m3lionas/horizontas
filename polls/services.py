import subprocess
import sys


def handle_uploaded_file(f, test_cases):
    # with open('some/file/name.txt', 'wb+') as destination:
    #     for chunk in f.chunks():
    #         destination.write(chunk)
    passed_tests = True
    str_text = ''

    for line in f.chunks():
        str_text = str_text + line.decode()

    for case in test_cases:
        input_params = case.test_input.replace(',', '\n') + '\n'

        result = subprocess.run(
            [sys.executable, "-c", str_text], universal_newlines=True, input=input_params, capture_output=True,
            text=True, timeout=5
        )

        print('Expected output: ' + case.test_output)
        print('Actual output: ' + result.stdout)

        if result.stdout.lower() != (case.test_output.lower() + '\n'):
            passed_tests = False
            break

    print('Were tests passed: ' + str(passed_tests))
    return passed_tests
    # print("stdout:", result.stdout)
    # print("stderr:", result.stderr)
