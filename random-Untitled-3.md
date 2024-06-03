# TLDR:
# first and third element of a three element tuple are operands (exception: two element tuple, which has a default operation of '==')
# second element of a three element tuple is the operator
# one element tuple: truthy check
# two element tuple: comparison
# three element tuple: logical operation

(True,)
('True',)
(foo,) # truthy check on variable foo at subscribe-time # type: ignore
('foo',) # truthy check on event property at emission-time
('user.id', 12) # evaluate `event.user.id == 12` at emission-time
('user.score', '>=', 100) # evaluate `event.user.score >= 100` at emission-time
('user', 'and', 'user.enrolled') # evaluate `event.user and event.user.enrolled` at emission-time
( ('request.method', '!=', 'POST'), 'or' ('resource.create', 'in', 'user.permissions') ) # nested evaluation
