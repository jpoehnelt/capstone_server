import pytest
from StringIO import StringIO
from capstone_server import Record

@pytest.mark.parametrize("contents, filename, valid", [
    ('0,', "something.csv", False),
    ("0,0,0,0,0,0,0,0,0,0,0,0", "something.gif", False),
    ("somebytesformacid,1460322897002,0,0,0,0,0,0,0,0,0,0", "something.csv", True)
])
def test_upload(client, contents, filename, valid, session):
    data = {
        'file': (StringIO(contents), filename),
    }
    r = client.post('/upload', data=data)
    print(r.data)
    if valid:
        assert r.status_code == 200
        assert session.query(Record).count() > 0
    else:
        assert r.status_code == 400
        assert session.query(Record).count() == 0
