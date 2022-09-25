
from navigate import insert_data
from navigate import app

if __name__ == '__main__':
    insert_data.drop_tables()
    insert_data.insert_default_data()
    insert_data.cal_order_history()
    app.run( port=8000)