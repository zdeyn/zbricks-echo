# tests/test_zbrick.py
import pytest
from zbricks import zBrick
from zbricks.core import _zAttachment

# Tests for _zAttachment dataclass
class Test_zAttachment:

    @pytest.mark.parametrize("a1, a2", [
        (_zAttachment(id="123", value="foo"), _zAttachment(id="123", value="bar")),
        (_zAttachment(value="foo"), _zAttachment(value="foo")),
        (_zAttachment(id=None, value="foo"), _zAttachment(id=None, value="foo"))
    ])
    def test_equality(self, a1, a2):
        assert a1 == a2

    @pytest.mark.parametrize("a1, a2", [
        (_zAttachment(id="123", value="foo"), _zAttachment(id="456", value="foo")),
        (_zAttachment(value="foo"), _zAttachment(value="bar")),
        (_zAttachment(id=None, value="foo"), _zAttachment(id=None, value="bar"))
    ])
    def test_inequality(self, a1, a2):
        assert a1 != a2

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
