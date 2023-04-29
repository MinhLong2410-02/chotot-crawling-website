def execute(cursor, query, values=None, multi=False):
    if values is None:
        cursor.execute(query, multi=multi)
    else:
        cursor.execute(query, values, multi=multi)
    result_set = cursor.fetchall()
    return result_set


def update_cud(cursor, status):
    query = "SELECT * FROM cud"
    cud = execute(cursor, query)
    cud = cud[-1]
    cud[status] += 1
    
    query = "INSERT INTO cud (number_of_created, number_of_updated, number_of_deleted) VALUES (%s, %s, %s)"
    values = (cud['number_of_created'], cud['number_of_updated'], cud['number_of_deleted'])
    execute(cursor, query, values)

