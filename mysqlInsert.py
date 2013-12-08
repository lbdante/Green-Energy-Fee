import MySQLdb as mdb
import conf
def insert_data(data):
    try:
        # Replace the parameters here for using a different mysql server
        conn = mdb.connect(host=conf.server, user=conf.writer_username, passwd=conf.writer_password, db=conf.db)
        cur = conn.cursor()
        for row in data:
            #Insert each row of the array into the database
            cur.execute("INSERT INTO Entry (source, date, type, cost, units_total, total_cost) VALUES (%s, %s, %s, %s, %s, %s)", (row['source'], row['date'], row['type'], row['cost'], row['units_total'], row['total_cost']))
        conn.commit()
        conn.close()
    except mdb.Error, e:
        #Print any mysql errors.
        print "Error %d: %s" % (e.args[0],e.args[1])
