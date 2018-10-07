import tailjournal
import json

def test_import():
  assert dir(tailjournal)
  assert "main" in dir(tailjournal)

def count_fixture_journal_entries():
  with open("tests/fixtures/test-journal.json", "r") as file:
    counter = 0
    for _ in file:
      counter += 1
    return counter

def generate_fixture_journal_entries():
  with open ("tests/fixtures/test-journal.json", "r") as file:
    for line in file:
      yield line

def test_convert_to_json():
    events = generate_fixture_journal_entries()
    events = tailjournal.convert_to_json(events)
    counter = 0
    for event in events:
      counter += 1
      assert json.dumps(event)
    assert counter == count_fixture_journal_entries()

def test_filter_events():
    events = generate_fixture_journal_entries()
    events = tailjournal.convert_to_json(events)
    events = tailjournal.filter_events(events)
    counter = 0
    for event in events:
      counter += 1
      assert json.dumps(event)
 
    assert counter == count_fixture_journal_entries()
