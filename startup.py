

def build_config_template():

    code = '''

db_data = {
'host': '',
'port': '',
'database': '',
'user': '',
'password': ''
}

    '''


    with open('config.py', 'w') as f:
        f.write(code)
    
    print('Config.py template built')


if __name__ =="__main__":

    build_config_template()