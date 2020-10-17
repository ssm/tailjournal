import pytest
import tailjournal
import json

@pytest.fixture
def num_entries():
  with open("tests/fixtures/test-journal.json", "r") as file:
    counter = 0
    for _ in file:
      counter += 1
    return counter

@pytest.fixture
def journal_entries():
  with open ("tests/fixtures/test-journal.json", "r") as file:
    yield file.readlines()

def test_import():
  assert dir(tailjournal)

def test_convert_to_json(journal_entries,num_entries):
  json_lines = tailjournal.convert_to_json(journal_entries)
  line_counter = 0

  for line in json_lines:
    line_counter += 1
    assert json.dumps(line)

  assert line_counter == num_entries

def test_filter_events(journal_entries,num_entries):
  json_lines = tailjournal.convert_to_json(journal_entries)
  filtered_lines = tailjournal.filter_events(json_lines)
  line_counter = 0

  for line in filtered_lines:
    line_counter += 1
    assert json.dumps(line)

  assert line_counter == num_entries
