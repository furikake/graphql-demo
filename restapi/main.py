# flask
from flask import Flask, request, session, g, redirect, url_for, abort, \
    render_template, flash, make_response
from flask_negotiate import consumes, produces

from urllib.parse import urlparse
import io, json, logging, os, sqlite3, sys
import testdata

app = Flask(__name__)
app.config.from_object(__name__)

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'db/demo.db'),
    SECRET_KEY='development key'
))

def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

def init_db():
    """Inits the database"""
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

@app.cli.command('initdb')
def initdb_command():
    """Flask command line command to init the database."""
    init_db()
    print('initialized the database.')
    generate_test_data()
    print('generated demo data.')

def generate_test_data():
    """loads test data for the demo into the database"""

    no_records = 20000
    batch_size = 10000
    db = get_db()

    sql_address = """INSERT INTO address (location_id, 
        rollout_region_id, distribution_area_id,
        road_number, road_name,
        road_type_code, locality_name, 
        state_territory_code, full_address) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"""

    rec_no = 0

    for record in testdata.generate_test_address_data(no_records):
        rec_no = rec_no + 1
        c = db.execute(sql_address, (record["location_id"], 
            record["rollout_region_id"], record["distribution_area_id"], 
            record["road_number"], record["road_name"], 
            record["road_type_code"], record["locality_name"], 
            record["state_territory_code"], record["full_address"]))
        if rec_no % batch_size == 0:
            db.commit()
            print('writing address: {}'.format(rec_no))

    sql_service_qual = """INSERT INTO service_qualification (location_id, 
        service_class, service_class_desc, 
        service_class_reason, service_type, 
        expected_date_of_rfs) VALUES (?, ?, ?, ?, ?, ?)"""

    rec_no = 0

    for record in testdata.generate_test_sevice_qual_data(no_records):
        rec_no = rec_no + 1
        c = db.execute(sql_service_qual, (record["location_id"], 
            record["service_class"], record["service_class_desc"], 
            record["service_class_reason"], record["service_type"], 
            record["rfs_date"]))
        if rec_no % batch_size == 0:
            db.commit()
            print('writing service qual: {}'.format(rec_no))

    sql_medical_alarm = """INSERT INTO medical_alarm (location_id, 
        description, contact_crm_id) VALUES (?, ?, ?)"""

    rec_no = 0

    for record in testdata.generate_test_medical_alarm_data(no_records):
        rec_no = rec_no + 1
        c = db.execute(sql_medical_alarm, (record["location_id"],
            record["description"], record["contact_crm_id"]))
        if rec_no % batch_size == 0:
            db.commit()
            print('writing medical alarm: {}'.format(rec_no))

    sql_contact = """INSERT INTO contact (crm_id,
        name, email,
        phone) VALUES (?, ?, ?, ?)"""

    rec_no = 0

    for record in testdata.generate_test_contact(no_records):
        rec_no = rec_no + 1
        c = db.execute(sql_contact, (record["crm_id"],
            record["name"], record["email"],
            record["phone"]))
        if rec_no % batch_size == 0:
            db.commit()
            print('writing contact: {}'.format(rec_no))

    print('finished generating data -> committing') 
    db.commit()
    print('committed')

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format='%(asctime)s [%(levelname)s] %(message)s')

@app.route("/")
def hello():
    logging.info("GET /")
    return "The API is up"

@app.route("/addresses/<location_id>")
@produces("application/json")
def get_address(location_id):
    
    logging.info("GET /addresses/{}".format(location_id))

    db = get_db()

    c = db.execute("SELECT location_id, rollout_region_id, distribution_area_id, road_number, road_name, road_type_code, locality_name, state_territory_code, full_address FROM address WHERE location_id = ?", (location_id,))

    # won't actually retrieve more than one record due to unique constraint
    row = c.fetchone()

    if None == row:
        return json.dumps({}), 200
    else:
        resp = { "location_id": row["location_id"], 
            "rollout_region_id": row["rollout_region_id"],
            "distribution_area_id": row["distribution_area_id"],
            "road_number": row["road_number"],
            "road_name": row["road_name"],
            "road_type_code": row["road_type_code"],
            "locality_name": row["locality_name"],
            "state_territory_code": row["state_territory_code"],
            "full_address": row["full_address"] }
        return json.dumps(resp), 200

@app.route("/addresses")
@produces("application/json")
def get_addresses():
    
    logging.info("GET /addresses")
    logging.info(str(dir(request)))

    logging.info("start=" + request.args.get('start'))

    limit = request.args.get('limit')
    if not limit.isdigit():
        return "limit must be a number", 400

    db = get_db()

    c = db.execute("SELECT location_id, rollout_region_id, distribution_area_id, road_number, road_name, road_type_code, locality_name, state_territory_code, full_address FROM address WHERE location_id = ? ORDER BY location_id LIMIT ?", (location_id, limit))

    return "", 200

"""
Get the service-qualifications
"""
@app.route("/service-qualifications/<location_id>")
@produces("application/json")
def get_service_qualification(location_id):

    logging.info("GET /service-qualifications/{}".format(location_id))

    db = get_db()

    c = db.execute("SELECT location_id, service_class, service_class_desc, service_class_reason, service_type, expected_date_of_rfs FROM service_qualification WHERE location_id = ?", (location_id,))

    # won't actually retrieve more than one record due to unique constraint
    row = c.fetchone()

    if None == row:
        return json.dumps({}), 200
    else:
        resp = { "location_id": row["location_id"], 
            "service_class": row["service_class"],
            "service_class_desc": row["service_class_desc"],
            "service_class_reason": row["service_class_reason"],
            "service_type": row["service_type"],
            "expected_date_of_rfs": row["expected_date_of_rfs"] }
        return json.dumps(resp), 200
    
"""
Get the medical alarms
"""
@app.route("/medical-alarms/<location_id>")
@produces("application/json")
def get_medical_alarm(location_id):

    logging.info("GET /medical-alarms/{}".format(location_id))

    db = get_db()

    c = db.execute("SELECT location_id, description, contact_crm_id FROM medical_alarm WHERE location_id = ?", (location_id,))

    resp = []

    for record in c:
        resp.append({ "location_id": record["location_id"], 
            "description": record["description"], 
            "contact_crm_id": record["contact_crm_id"] })

    return json.dumps(resp), 200

"""
Get the contact
"""
@app.route("/contacts/<contact_id>")
@produces("application/json")
def get_contact(contact_id):

    logging.info("GET /contacts/{}".format(contact_id))

    db = get_db()

    c = db.execute("SELECT crm_id, name, email, phone FROM contact WHERE crm_id = ?", (contact_id,))

    # won't actually retrieve more than one record due to unique constraint
    row = c.fetchone()

    resp = []

    if None == row:
        return json.dumps({}), 200
    else:
        resp = { "crm_id": row["crm_id"], 
            "name": row["name"],
            "email": row["email"],
            "phone": row["phone"] }
        return json.dumps(resp), 200


if __name__ == "__main__":
    app.run()
