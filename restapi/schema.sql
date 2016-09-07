drop table if exists service_qualification;
create table service_qualification (
    id integer primary key autoincrement NOT NULL,
    location_id text NOT NULL,
    service_class text NOT NULL,
    service_class_desc text NOT NULL,
    service_class_reason text,
    service_type text NOT NULL,
    expected_date_of_rfs text,
    CONSTRAINT unique_location_id UNIQUE (location_id)
);

drop table if exists address;
create table address (
    id integer primary key autoincrement NOT NULL,
    location_id text NOT NULL,
    rollout_region_id text NOT NULL,
    distribution_area_id text,
    road_number text NOT NULL,
    road_name text NOT NULL,
    road_type_code text NOT NULL,
    locality_name text NOT NULL,
    state_territory_code text NOT NULL,
    full_address text NOT NULL,
    CONSTRAINT unique_location_id UNIQUE (location_id)
);

drop table if exists medical_alarm;
create table medical_alarm (
    id integer primary key autoincrement NOT NULL,
    location_id text NOT NULL,
    description text,
    contact_crm_id text NOT NULL
);

drop table if exists contact;
create table contact (
    id integer primary key autoincrement NOT NULL,
    crm_id text NOT NULL,
    name text NOT NULL,
    email text,
    phone text,
    CONSTRAINT unique_crm_id UNIQUE (crm_id)
);
CREATE INDEX IF NOT EXISTS name_idx ON contact(name);
CREATE INDEX IF NOT EXISTS email_idx ON contact(email);
CREATE INDEX IF NOT EXISTS phone_idx ON contact(phone);
