from utils.sql import update


def update_state(id, state):
    sql = 'update file set state = %s where id = %s'
    update(sql, (state, id))
    return 1