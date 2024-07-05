from apps.utils.decorators import response_builder, example_function  # Replace with your actual module

def test_response_builder_decorator():
    @response_builder('result')
    def test_function():
        return [4, 5, 6]

    expected_output = {
        "responseCode": 200,
        "responseMessage": "OK",
        "result": [4, 5, 6]
    }
    assert test_function() == expected_output

def test_example_function():
    expected_output = {
        "responseCode": 200,
        "responseMessage": "OK",
        "result": [1, 2, 3]
    }
    assert example_function() == expected_output
