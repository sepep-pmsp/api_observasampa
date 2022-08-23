

def build_conn_str(user, password, host, port, 
                       database, dbms='postgresql'):
    
    conn_str = f'{dbms}://{user}:{password}@{host}:{port}/{database}'
    
    return conn_str