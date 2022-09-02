import os


def check_for_config():

    fname = 'config.py'
    return os.path.exists(fname)

def create_code(host, port, db, user, passw):

    code = f'''

    from core.utils.utils import build_conn_str

    db_data = {{
    'host': '{host}',
    'port': '{port}',
    'database': '{db}',
    'user': '{user}',
    'password': '{passw}'
    }}

    SQLALCHEMY_DATABASE_URL = build_conn_str(**db_data)

        '''

    return code


def build_config_template():

    if check_for_config():
        print('Config already exists')
    else:
        db_data = dict(
        host = input("Digite o host: "),
        port = input("Digite a porta: "),
        db = input("Digite o nome do banco de dados: "),
        user = input("Digite o usuario: "),
        passw = input("Digite a senha: "),
        )
        print('Dados digitados:')
        print(db_data)

        code = create_code(**db_data) 
        with open('config.py', 'w') as f:
            f.write(code)
        print('Config.py criado!')

if __name__ =="__main__":

    build_config_template()