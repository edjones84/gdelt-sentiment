from behave import given, when, then
from behave.runner import Context
import requests
import json
import jsonschema



API_URL = "http://localhost:8000"


@given('the API is running')
def step_given_api_running(context):
    pass


@when('I make a GET request to "{endpoint}"')
def step_when_get_request(context, endpoint):
    response = requests.get(f"{API_URL}{endpoint}")
    context.response = response


@then('the response status code should be {status_code}')
def step_then_check_status_code(context: Context, status_code):
    assert context.response.status_code == int(status_code)


@then('the response body should contain valid JSON')
def step_then_check_valid_json(context):
    try:
        json.loads(context.response.text)
    except json.JSONDecodeError:
        assert False, "Response body is not valid JSON"


@when('the query input is "{query_input}"')
def step_given_query_input(context, query_input):
    context.query_input = query_input
    response = requests.get(f"{API_URL}/endpoint?queryInput={query_input}")
    context.response = response


@then('the response body should contain sentiment scores')
def step_then_check_sentiment_scores(context):
    response_body = json.loads(context.response.text)
    # Define the expected schema
    expected_schema = {
        "type": "object",
        "properties": {
            "scores": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "neg": {"type": "number"},
                        "neu": {"type": "number"},
                        "pos": {"type": "number"},
                        "compound": {"type": "number"},
                        "original_title": {"type": "string"},
                        "title": {"type": "string"},
                        "origin_language": {"type": "string"}
                    },
                    "required": ["neg", "neu", "pos", "compound", "original_title", "title", "origin_language"]
                }
            }
        },
        "required": ["scores"]
    }

    # Validate the response body against the expected schema
    jsonschema.validate(instance=response_body, schema=expected_schema)


@when('I make a GET request to "/" with query input')
def step_when_get_request_with_query_input(context):
    params = {"queryInput": context.query_input}
    context.response = requests.get(f"{API_URL}/endpoint", params=params)


@then('stop the API')
def step_then_stop_api(context):
    context.process.kill()
