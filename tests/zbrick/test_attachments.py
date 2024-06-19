# tests/test_zbrick.py
import pytest
from zbricks import zBrick
from zbricks.core import _zAttachment
from rich import print

# Tests for _zAttachment dataclass
class Test_zAttachment:
    _123_foo = {'id':"123", 'value':"foo"}
    _123_bar = {'id':"123", 'value':"bar"}
    _456_foo = {'id':"456", 'value':"foo"}
    _none_foo = {'id':None, 'value':"foo"}
    _none_bar = {'id':None, 'value':"bar"}

    tests = {
        "positive case: ids match": (_123_foo, _123_bar, True), # ignores value
        "negative case: ids do not match (set/set)": [_123_foo, _456_foo, False], # ignores value
        "negative case: ids do not match (set/none)": [_123_foo, _none_foo, False], # ignores value
        "positive case: no ids, values match": [_none_foo, _none_foo, True], # ignores ids
        "negative case: no ids, values do not match": [_none_foo, _none_bar, False], # ignores ids
    }

    @pytest.mark.parametrize(
            "one, two, expected", [ v for v in tests.values() ], ids = [K for K in tests.keys()])
    def test_equality(self, one, two, expected):
        a1 = _zAttachment(**one)
        a2 = _zAttachment(**two)
        print(f"\nComparing {a1} to {a2}, expecting {expected}")
        assert (a1 == a2) == expected  

# zBricks can exist, and have attachments as they exist
class Test_zBrick_Instance:

    @pytest.fixture(scope='class')
    def brick_with_attachments(self):
        return zBrick(attachments={'foo': 'bar'})

    def test_exists(self):
        assert zBrick() is not None
    
    def test_default_attachments(self):
        brick = zBrick()
        assert len(brick._attachments) == 0
    
    def test_declared_attachments(self, brick_with_attachments):
        assert 'foo' in brick_with_attachments
        assert brick_with_attachments['foo'] == 'bar'

# zBrick attachments may be accessed using dictionary-style syntax by label 
class Test_zBrick_Dict_by_Label:

    @pytest.fixture(scope='class')
    def empty_brick(self):
        return zBrick()

    @pytest.fixture(scope='class')
    def brick_with_attachments(self):
        return zBrick(attachments={'test': 'value'})

    def test_raises_exception(self, empty_brick):
        with pytest.raises(KeyError):
            _ = empty_brick['missing']

    def test_returns_value(self, brick_with_attachments):
        assert brick_with_attachments['test'] == 'value'
    
    def test_sets_value(self, empty_brick):
        assert len(empty_brick._attachments) == 0
        empty_brick['test'] = 'value'
        assert len(empty_brick._attachments) == 1
        assert empty_brick['test'] == 'value'

# zBrick attachments may be accessed using dictionary-style syntax by type
class Test_zBrick_Dict_by_Type:

    @pytest.fixture(scope='class')
    def empty_brick(self):
        return zBrick()

    @pytest.fixture(scope='class')
    def brick_with_attachments(self):
        brick = zBrick()
        brick['test'] = 'value'
        return brick

    def test_raises_exception(self, empty_brick):
        with pytest.raises(KeyError):
            _ = empty_brick[str]

    def test_returns_list_of_instances(self, brick_with_attachments):
        assert brick_with_attachments[str] == ['value']

# zBrick attachments may be membership checked using the 'in' operator by label
class Test_zBrick_Contains_by_Label:

    @pytest.fixture(scope='class')
    def empty_brick(self):
        return zBrick()

    @pytest.fixture(scope='class')
    def brick_with_attachments(self):
        return zBrick(attachments={'test': 'value'})

    def test_returns_false_if_not_found(self, empty_brick):
        assert 'missing' not in empty_brick

    def test_returns_true_if_found(self, brick_with_attachments):
        assert 'test' in brick_with_attachments

# zBrick attachments may be membership checked using the 'in' operator by type
class Test_zBrick_Contains_by_Type:

    @pytest.fixture(scope='class')
    def empty_brick(self):
        return zBrick()

    @pytest.fixture(scope='class')
    def brick_with_attachments(self):
        return zBrick(attachments={'test': 'value'})

    def test_returns_false_if_not_found(self, empty_brick):
        assert str not in empty_brick

    def test_returns_true_if_found(self, brick_with_attachments):
        assert str in brick_with_attachments

# zBrick attachments may be membership checked using the 'in' operator by instance
class Test_zBrick_Contains_by_Instance:

    @pytest.fixture(scope='function')
    def child(self) -> zBrick:
        return zBrick()

    @pytest.fixture(scope='function')
    def parent(self, child) -> zBrick:
        parent = zBrick([child])
        assert child in parent.children
        assert child in parent
        return parent
    
    @pytest.fixture(scope='function')
    def other(self) -> zBrick:
        return zBrick()

    def test_returns_false_if_not_found(self, parent, other):
        assert other not in parent

    def test_returns_true_if_found(self, parent, child):
        assert child in parent

# TODO: 
# attaching a zBrick to a zBrick sets the 'parent' key in the child's attachments
class Test_zBrick_Parent:

    @pytest.fixture(scope='function')
    def parent(self) -> zBrick:
        return zBrick()

    @pytest.fixture(scope='function')
    def child(self) -> zBrick:
        return zBrick()

    def test_parent_key(self, parent, child):
        parent['child'] = child
        assert child._parent == parent
        assert child in parent.children
