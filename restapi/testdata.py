import datetime, random, string, uuid

def generate_test_address_data(records=10000):
    """yields a generator with x number of address data records in a dictionary"""

    postcode_state_suburb_tuple = (("0800", "NT", "Darwin"),
        ("0870", "NT", "Alice Springs"),
        ("2000", "NSW", "Sydney"),
        ("2000", "NSW", "Darling Harbour"),
        ("2000", "NSW", "Dawes Point"),
        ("2037", "NSW", "Forest Lodge"),
        ("2037", "NSW", "Glebe"),
        ("2087", "NSW", "Forestville"),
        ("2145", "NSW", "Girraween"),
        ("2145", "NSW", "Greystanes"),
        ("2259", "NSW", "Alison"),
        ("2259", "NSW", "Cedar Brush Creek"),
        ("2604", "ACT", "Causeway"),
        ("3000", "VIC", "Melbourne"),
        ("3015", "VIC", "Newport"),
        ("3015", "VIC", "Spotswood"),
        ("3019", "VIC", "Braybrook"),
        ("3251", "VIC", "Beeac"),
        ("3251", "VIC", "Cundare North"),
        ("3251", "VIC", "Eurack"),
        ("3251", "VIC", "Weering"),
        ("3377", "VIC", "Ararat"),
        ("3378", "VIC", "Yalla-y-poora"),
        ("5000", "SA", "Adelaide"),
        ("5017", "SA", "Osborne"),
        ("5017", "SA", "Taperoo"),
        ("5074", "SA", "Campbelltown"),
        ("5112", "SA", "Elizabeth"),
        ("6000", "WA", "Perth"),
        ("6027", "WA", "Beldon"),
        ("6027", "WA", "Connolly"),
        ("6081", "WA", "Parkerville"),
        ("6149", "WA", "Bull Creek"),
        ("6149", "WA", "Leeming"),
        ("6169", "WA", "Safety Bay"),
        ("6169", "WA", "Shoalwater"),
        ("6625", "WA", "Allanson"),
        ("6625", "WA", "Bowelling"),
        ("7000", "TAS", "Glebe"),
        ("7000", "TAS", "Hobart"),
    )

    road_names = ("Alpha", "Beta", "Charlie", "Delta", 
        "Echo", "Foxtrot", "Golf", "Hotel", "India", 
        "Juliet", "Kilo", "Lima", "Mike", "November", 
        "Oscar", "Papa", "Quebec", "Romeo", "Sierra", 
        "Tango", "Uniform", "Victor", "Whiskey", "X-Ray", 
        "Yankee", "Zulu")

    road_type_codes = ("Ave", "Cres", "Hwy", "Lane", "Pde", "Pl", "Rd", "St", "View")
    
    for i in range(1, records+1):
        location_id = ('LOC{0:012d}'.format(i))
        rollout_region_id, distribution_area_id = _gen_random_rollout_region_and_distribution_area_id()
        road_number, road_name, road_type_code, locality_name, state_territory_code, postcode, full_address = _gen_random_address(road_names, road_type_codes, postcode_state_suburb_tuple)
        yield { "location_id": location_id, 
            "rollout_region_id": rollout_region_id, 
            "distribution_area_id": distribution_area_id, 
            "road_number": road_number, 
            "road_name": road_name, 
            "road_type_code": road_type_code, 
            "locality_name": locality_name, 
            "state_territory_code": state_territory_code, 
            "full_address": full_address }

def generate_test_sevice_qual_data(records=10000):
    """yields a generator with x number of service qualification records in a dictionary"""

    service_list = ((0, "Planned to be serviced by fibre (as yet not serviceable)", "Bespoke Connection Required", "Brownfields Fibre"),
        (0, "Planned to be serviced by fibre (as yet not serviceable)", "Under Construction", "Brownfields Fibre"),
        (0, "Planned to be serviced by fibre (as yet not serviceable)", "Frustrated Premises Access Denied", "Brownfields Fibre"),
        (0, "Planned to be serviced by fibre (as yet not serviceable)", None, "Brownfields Fibre"),
        (0, "Planned to be serviced by fibre (as yet not serviceable)", None, "Greenfields Fibre"),
        (1, "Serviceable by fibre, no Drop in place, no NTD", None, "Greenfields Fibre"),
        (2, "Serviceable by fibre, Drop in place, no NTD", None, "Greenfields Fibre"),
        (3, "Serviceable by fibre, Drop and NTD in place", None, "Greenfields Fibre"),
        (4, "Within Wireless Boundary (Wireless not in service)", None, "Wireless"),
        (5, "Serviceable by Wireless, NTD not installed", None, "Wireless"),
        (6, "Serviceable by Wireless, NTD installed", None, "Wireless"),
        (7, "Planned to be serviced by satellite (as yet not serviceable)", None, "Satellite"),
        (10, "Planned to be serviced by Copper (as yet not serviceable)", None, "FTTB-Copper"),
        (11, "Serviceable by Copper, no existing Copper Pair in-place, lead-in required", None, "FTTN-Copper"),
        (12, "Serviceable by Copper, Existing Copper Pair in-place not active with NBN Co.", None, "FTTN-Copper"),
        (13, "Serviceable by Copper, Existing Copper Pair in-place active with NBN Co.", None, "FTTN-Copper"),
    )

    # "Urban", "Major Rural", "Minor Rural", "Rural", TBA", "Remote"

    for i in range(1, records+1):
        location_id = ('LOC{0:012d}'.format(i))
        service_class, service_class_desc, service_class_reason, service_type = random.choice(service_list)
        rfs_date = datetime.date.today() + datetime.timedelta(days=random.randint(-730, 730)) #random date within a 4 year period
        yield { "location_id": location_id, 
            "service_class": service_class, 
            "service_class_desc": service_class_desc, 
            "service_class_reason": service_class_reason, 
            "service_type": service_type, 
            "rfs_date": rfs_date }

def _gen_random_rollout_region_and_distribution_area_id():
    the_type = random.randint(0,1)
    if 0 == the_type:
        rollout_region_id = "2ARM-%s" % (str(random.randint(0, 99)).zfill(2),)
        distribution_area_id = "%s-%s" % (rollout_region_id, str(random.randint(0, 99)).zfill(2))
        return (rollout_region_id, distribution_area_id)
    elif 1 == the_type:
        rollout_region_id = "7BUI-%s-%s-ROUN-%s-%s" % (str(random.randint(0, 99)).zfill(2), str(random.randint(0, 99)).zfill(2), str(random.randint(0, 99)).zfill(2), str(random.randint(0, 99)).zfill(2),)
        return (rollout_region_id, None)

def _gen_random_address(road_names, road_type_codes, postcode_state_suburb_tuple):
    road_number = str(random.randint(1, 400))
    road_name = random.choice(road_names)
    road_type_code = random.choice(road_type_codes)
    postcode, state_territory_code, locality_name = random.choice(postcode_state_suburb_tuple)
    full_address = "%s %s %s, %s %s %s" % (road_number, road_name, road_type_code, locality_name, state_territory_code, postcode)
    return (road_number, road_name, road_type_code, locality_name, state_territory_code, postcode, full_address)

def generate_test_medical_alarm_data(records=2000, percent=5):
    """Generates medical alarm records for a percentage of locations. Default to 5%"""
    if percent < 1 or percent > 100:
        raise ValueError("percent is between 1 and 100")
    count = 0 # number of records generated
    i = 0 # loop counter
    number_of_alarm_choices = [0,1,2,3]
    while count < records:
        i = i + 1
        modulus = i % 100
        if modulus >= 0 and modulus < percent:
            # generate a medical alarm for this location
            if records - count <= 3:
                # generate just enough to complete the requisite number of records
                no_alarms = (records - count)
            else:
                # generate a random number of alarms
                no_alarms = random.choice(number_of_alarm_choices)
            # print("%s will have %s alarm(s). Total so far %s" % (i, no_alarms, count))
            count = count + no_alarms
            for alarm in range(no_alarms): 
                location_id = ('LOC{0:012d}'.format(i))
                crm_id = ('CRM{0:012d}'.format(i))
                description = "alarm %s of %s - serial number %s" % ((alarm + 1), no_alarms, uuid.uuid4())
                yield { "location_id": location_id, 
                    "description": description,
                    "contact_crm_id": crm_id }

def generate_test_contact(records=2000):
    """Generates contacts"""
    domain_name_list = ("example.org", "example.com", "mailinator.com", "trashcanmail.com")
    first_name_list = ("donald", "mickey", "minnie", "pluto", "elsa", "anna", "peppa", "george", "winnie", "christopher")
    last_name_list = ("duck", "mouse", "sloth", "donkey", "tiger", "owl", "rabbit", "piglet", "bear", "ant", "bat")

    for i in range(1, records+1):

        crm_id = ('CRM{0:012d}'.format(i))
        name = "{} {}".format(random.choice(first_name_list).title(), random.choice(last_name_list).title())
        email = _gen_random_email(string.ascii_lowercase, domain_name_list)
        phone = ""

        yield { "crm_id": crm_id,
            "name": name,
            "email": email,
            "phone": phone }

def _gen_random_email(local_part_char_tuple, domain_name_tuple):
    local_part = ''.join(random.choice(local_part_char_tuple) for i in range(7))
    return "{}@{}".format(local_part, random.choice(domain_name_tuple))
