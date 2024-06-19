# tests/test_zbrick.py
import pytest
from zbricks.base import zAttachableMixin
from zbricks.core import zBrick
# from zbricks.base import _zAttachment
from rich import print

class zTestBrick(zBrick):
    def _attach_parent(self, parent: zAttachableMixin) -> None:
        return super()._attach_parent(parent)
    
    def _attach_child(self, child: zAttachableMixin) -> None:
        return super()._attach_child(child)

# Tests for _zAttachment dataclass
# @pytest.mark.skip
# class Test_zAttachment:
#     _123_foo = {'id':"123", 'value':"foo"}
#     _123_bar = {'id':"123", 'value':"bar"}
#     _456_foo = {'id':"456", 'value':"foo"}
#     _none_foo = {'id':None, 'value':"foo"}
#     _none_bar = {'id':None, 'value':"bar"}

#     tests = {
#         "positive case: ids match": (_123_foo, _123_bar, True), # ignores value
#         "negative case: ids do not match (set/set)": [_123_foo, _456_foo, False], # ignores value
#         "negative case: ids do not match (set/none)": [_123_foo, _none_foo, False], # ignores value
#         "positive case: no ids, values match": [_none_foo, _none_foo, True], # ignores ids
#         "negative case: no ids, values do not match": [_none_foo, _none_bar, False], # ignores ids
#     }

#     @pytest.mark.parametrize(
#             "one, two, expected", [ v for v in tests.values() ], ids = [K for K in tests.keys()])
#     def test_equality(self, one, two, expected):
#         a1 = _zAttachment(**one)
#         a2 = _zAttachment(**two)
#         # print(f"\nComparing {a1} to {a2}, expecting {expected}")
#         assert (a1 == a2) == expected  

@pytest.fixture(scope='class')
def brick() -> zAttachableMixin:
    return zTestBrick()

@pytest.fixture(scope='class')
def child() -> zAttachableMixin:
    child = zTestBrick(name='foo')
    return child

@pytest.fixture(scope='class')
def brick_with_child(brick: zAttachableMixin, child: zAttachableMixin) -> zAttachableMixin:
    brick.attach(child)
    return brick

# zBricks can exist, and have attachments as they exist
class Test_zBrick_Instance:

    def test_exists(self, brick: zAttachableMixin):
        assert brick is not None
    
    def test_default_children(self, brick: zAttachableMixin):
        assert len(brick.children) == 0
    
    def test_declared_attachments(self, brick_with_child: zAttachableMixin, child: zAttachableMixin):
        assert child in brick_with_child
        assert brick_with_child['foo'] == child

# zBrick attachments may be accessed using dictionary-style syntax by label 
class Test_zBrick_Dict_by_Label:

    # @pytest.fixture(scope='class')
    # def empty_brick(self):
    #     return zAttachableMixin()

    # @pytest.fixture(scope='class')
    # def brick_with_children(self):
    #     return zAttachableMixin(children={'test': 'value'})

    def test_raises_exception(self, brick):
        with pytest.raises(KeyError):
            _ = brick['missing']

    def test_returns_value(self, brick_with_child, child):
        assert brick_with_child['foo'] == child
    
    def test_sets_value(self, brick: zAttachableMixin):
        tmp = zTestBrick()
        assert len(tmp.children) == 0
        tmp['test'] = brick
        assert len(tmp.children) == 1
        assert brick in tmp.children

# zBrick attachments may be accessed using dictionary-style syntax by type
class Test_zBrick_Dict_by_Type:

    def test_raises_exception(self, brick):
        with pytest.raises(KeyError):
            _ = brick[str]

    def test_returns_list_of_instances(self, brick_with_child, child):
        assert brick_with_child[zTestBrick] == [child]

# zBrick attachments may be membership checked using the 'in' operator by label
class Test_zBrick_Contains_by_Label:

    def test_returns_false_if_not_found(self, brick):
        assert 'missing' not in brick

    def test_returns_true_if_found(self, brick_with_child):
        assert 'foo' in brick_with_child

# zBrick attachments may be membership checked using the 'in' operator by type
class Test_zBrick_Contains_by_Type:

    def test_returns_false_if_not_found(self, brick):
        assert str not in brick

    def test_returns_true_if_found(self, brick_with_child):
        assert zAttachableMixin in brick_with_child

# zBrick attachments may be membership checked using the 'in' operator by instance
class Test_zBrick_Contains_by_Instance:

    def test_returns_false_if_not_found(self, brick_with_child):
        other = zTestBrick()
        assert other not in brick_with_child

    def test_returns_true_if_found(self, brick_with_child, child):
        assert child in brick_with_child

# TODO: 
# attaching a zBrick to a zBrick sets the 'parent' key in the child's attachments
class Test_zBrick_Parent:

    def test_parent_key(self, brick: zAttachableMixin):
        tmp = zTestBrick()
        assert 'child' not in brick
        brick['child'] = tmp
        assert tmp.parent == brick
        assert tmp in brick.children
