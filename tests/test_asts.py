from quiche.ast_quiche_tree import ASTQuicheTree
from quiche.egraph import EGraph

def setup_tree():
    tree_root = ASTQuicheTree()
    tree_root.from_file("tests/test_sqrt.py")
    return tree_root


def make_rule_1():
    # test rule where body is a variable
    return ASTQuicheTree.make_rule(
        "while True:\n\t__quiche__body", "while 1:\n\t__quiche__body"
    )


def make_rule_2():
    # test rule where body is a string
    return ASTQuicheTree.make_rule(
        "while True:\n\t'__quiche__body'", "while 1:\n\t'__quiche__body'"
    )


def test_make_rule1():
    rule = make_rule_1()
    # Verify LHS type
    assert isinstance(rule.lhs, ASTQuicheTree)
    assert rule.lhs.value() == "While"
    assert len(rule.lhs.children()) == 3

    # Verify LHS "True" structure: (NameConstant bool, value = True)
    assert rule.lhs.children()[0].value() == "NameConstant"
    assert rule.lhs.children()[0].children()[0].value() == "bool"
    assert rule.lhs.children()[1].children()[0].root.value

    # Verify LHS (StmtSequence (Expr (Name __quiche__body))) structure
    stmt_sequence = rule.lhs.children()[1]
    assert stmt_sequence.value() == "StmtSequence"
    assert len(stmt_sequence.children()) == 1
    assert stmt_sequence.children()[0].value() == "Expr"
    assert stmt_sequence.children()[0].children()[0].value() == "Name"
    assert stmt_sequence.children()[0].children()[0].root.id == "__quiche__body"

    # Verify RHS type
    assert isinstance(rule.rhs, ASTQuicheTree)
    assert rule.rhs.value() == "While"
    assert len(rule.rhs.children()) == 3

    # Verify RHS "1" structure: (Num int, value = 1)
    assert rule.rhs.children()[0].value() == "Num"
    assert rule.rhs.children()[0].children()[0].value() == "int"
    assert rule.rhs.children()[0].children()[0].root == 1

    # Verify RHS (StmtSequence (Expr (Name __quiche__body))) structure
    stmt_sequence = rule.rhs.children()[1]
    assert stmt_sequence.value() == "StmtSequence"
    assert len(stmt_sequence.children()) == 1
    assert stmt_sequence.children()[0].value() == "Expr"
    assert stmt_sequence.children()[0].children()[0].value() == "Name"
    assert stmt_sequence.children()[0].children()[0].root.id == "__quiche__body"


def test_make_rule2():
    rule = make_rule_2()
    # Verify LHS type
    assert isinstance(rule.lhs, ASTQuicheTree)
    assert rule.lhs.value() == "While"
    assert len(rule.lhs.children()) == 3

    # Verify LHS "True" structure: (NameConstant bool, value = True)
    assert rule.lhs.children()[0].value() == "NameConstant"
    assert rule.lhs.children()[0].children()[0].value() == "bool"
    assert rule.lhs.children()[1].children()[0].root.value

    # Verify LHS (StmtSequence (Expr (Str __quiche__body))) structure
    stmt_sequence = rule.lhs.children()[1]
    assert stmt_sequence.value() == "StmtSequence"
    assert len(stmt_sequence.children()) == 1
    assert stmt_sequence.children()[0].value() == "Expr"
    assert stmt_sequence.children()[0].children()[0].value() == "Str"
    assert stmt_sequence.children()[0].children()[0].root.s == "__quiche__body"

    # Verify RHS type
    assert isinstance(rule.rhs, ASTQuicheTree)
    assert rule.rhs.value() == "While"
    assert len(rule.rhs.children()) == 3

    # Verify RHS "1" structure: (Num int, value = 1)
    assert rule.rhs.children()[0].value() == "Num"
    assert rule.rhs.children()[0].children()[0].value() == "int"
    assert rule.rhs.children()[0].children()[0].root == 1

    # Verify RHS (StmtSequence (Expr (Str __quiche__body))) structure
    stmt_sequence = rule.rhs.children()[1]
    assert stmt_sequence.value() == "StmtSequence"
    assert len(stmt_sequence.children()) == 1
    assert stmt_sequence.children()[0].value() == "Expr"
    assert stmt_sequence.children()[0].children()[0].value() == "Str"
    assert stmt_sequence.children()[0].children()[0].root.s == "__quiche__body"


def test_ematch_rule1():
    quiche_tree = setup_tree()
    actual = EGraph(quiche_tree)
    rule = make_rule_1()

    match = actual.ematch(rule.lhs, actual.eclasses())
    key = list(actual.eclasses().keys())[42]
    assert match
    assert len(match) == 1
    assert key in match[0]


def test_ematch_rule2():
    quiche_tree = setup_tree()
    actual = EGraph(quiche_tree)
    rule = make_rule_2()

    match = actual.ematch(rule.lhs, actual.eclasses())
    key = list(actual.eclasses().keys())[42]
    assert match
    assert len(match) == 1
    assert key in match[0]


def test_apply_rule1():
    quiche_tree = setup_tree()
    actual = EGraph(quiche_tree)
    rule = make_rule_1()

    actual.apply_rules([rule])
    assert actual.version == 93
