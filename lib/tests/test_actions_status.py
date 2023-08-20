from state_manager.actions_status import ActionsStatus

def test_disable_actions():
    """Test if the actions are disabled correctly"""
    actions_status = ActionsStatus()
    actions_status.disable_actions()
    assert actions_status.get_actions_status() == [False, False, False, False]
    assert len(actions_status.get_saved_actions()) == 4

def test_illegal_renable_actions():
    """Test what happend when you set illegaly a button"""
    actions_status = ActionsStatus()
    actions_status.disable_actions()
    actions_status.set_buy_property(True)
    actions_status.set_pass_turn(True)
    actions_status.renable_actions()
    assert actions_status.get_actions_status() == [False, False, False, False]
    assert len(actions_status.get_saved_actions()) == 0

def test_renable_actions():
    """Test if the actions are renabled correctly"""
    actions_status = ActionsStatus()
    actions_status.set_buy_property(True)
    actions_status.set_pass_turn(True)
    actions_status.disable_actions()
    actions_status.renable_actions()
    assert actions_status.get_actions_status() == [False, True, False, True]
    assert len(actions_status.get_saved_actions()) == 0

def test_call_twice_renable_actions():
    """Test if the actions are renabled correctly"""
    actions_status = ActionsStatus()
    actions_status.set_buy_property(True)
    actions_status.set_pass_turn(True)
    actions_status.disable_actions()
    actions_status.renable_actions()
    actions_status.renable_actions()
    assert actions_status.get_actions_status() == [False, True, False, True]
    assert len(actions_status.get_saved_actions()) == 0

def test_call_twice_disable_actions():
    """Test if the actions are renabled correctly"""
    actions_status = ActionsStatus()
    actions_status.set_buy_property(True)
    actions_status.set_pass_turn(True)
    actions_status.disable_actions()
    actions_status.disable_actions()
    actions_status.renable_actions()
    assert actions_status.get_actions_status() == [False, True, False, True]
    assert len(actions_status.get_saved_actions()) == 0