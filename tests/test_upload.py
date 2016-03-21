import pytest
from StringIO import StringIO


@pytest.mark.parametrize("contents, filename, valid", [
    ('asdfadsfasdfa', "something.csv", False),
    ("0,0,0,0,0,0", "something.csv", True),
    ("0,0,0,0,0,0", "something.gif", False)
])
def test_upload(client, contents, filename, valid):
    data = {
        'file': (StringIO(contents), filename),
    }
    r = client.post('/upload', data=data)

    if valid:
        assert r.status_code == 200
    else:
        assert r.status_code == 400