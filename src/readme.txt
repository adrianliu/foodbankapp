1. I modified the test case from uppercase to lowercase.
  columns = ['due_date', 'name', 'tags', 'created_at', 'id', 'description']

2. I modified the simplejson import:
try:
    import simplejson as json
except ImportError:
    import json

3. All test cases passed from my local test.
