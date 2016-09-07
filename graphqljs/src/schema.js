import fetch from 'node-fetch';
import {
  GraphQLID,
  GraphQLList,
  GraphQLNonNull,
  GraphQLObjectType,
  GraphQLSchema,
  GraphQLString,
} from 'graphql';
import {
  fromGlobalId,
  globalIdField,
  nodeDefinitions,
} from 'graphql-relay';

const {
  nodeField,
  nodeInterface,
} = nodeDefinitions(
  // A method that maps from a global id to an object
  (globalId, {loaders}) => {
    const {id, type} = fromGlobalId(globalId);
    if (type === 'Location') {
      return loaders.location.load(id);
    }
  },
  // A method that maps from an object to a type
  (obj) => {
    if (obj.hasOwnProperty('locationId')) {
      return LocationType;
    }
  }
);

const ContactType = new GraphQLObjectType({
  name: 'Contact',
  description: 'A CRM contact',
  fields: () => ({
    crmId: {
      type: GraphQLString,
      description: 'CRM Identifier',
      resolve: location => location.crm_id,
    },
    name: {
      type: GraphQLString,
      description: 'Contact name',
    },
    email: {
      type: GraphQLString,
      description: 'Contact email',
    },
    phone: {
      type: GraphQLString,
      description: 'Contact phone',
    },
  })
})

const ServiceQualificationType = new GraphQLObjectType({
  name: 'ServiceQualification',
  description: 'Service qualification information for the location',
  fields: () => ({
    id: globalIdField('ServiceQualification'),
    locationId: {
      type: GraphQLString,
      description: 'Location ID',
      resolve: location => location.location_id,
    },
    serviceClass: {
      type: GraphQLString,
      description: 'Service Class',
      resolve: location => location.service_class,
    },
    serviceClassDesc: {
      type: GraphQLString,
      description: 'Service Class Description',
      resolve: location => location.service_class_desc,
    },
    serviceClassReason: {
      type: GraphQLString,
      description: 'Service Class Reason',
      resolve: location => location.service_class_reason,
    },
    serviceType: {
      type: GraphQLString,
      description: 'Service Type',
      resolve: location => location.service_type,
    },
    expectedDataOfRfs: {
      type: GraphQLString,
      description: 'Expected Date of Ready for Service',
      resolve: location => location.expected_date_of_rfs,
    },
    location: {
      type: LocationType,
      description: 'The location of the medical alarm',
      resolve: (obj, args, {loaders}) => {
        return loaders.location.load(obj.location_id);
      }
    }
  })
});

const MedicalAlarmType = new GraphQLObjectType({
  name: 'MedicalAlarm',
  description: 'Medical Alarm for the location',
  fields: () => ({
    id: globalIdField('MedicalAlarm'),
    locationId: {
      type: GraphQLString,
      description: 'Location ID',
      resolve: location => location.location_id,
    },
    description: {
      type: GraphQLString,
    },
    contactCrmId: {
      type: GraphQLString,
      description: 'Contact ID',
      resolve: location => location.contact_crm_id,
    },
    contact: {
      type: ContactType,
      resolve: (obj, args, {loaders}) => {
        // console.log('query: contact; obj=' + Object.keys(obj));
        // console.log('query: contact; args=' + Object.keys(args));
        // console.log('query: contact; loaders=' + Object.keys(loaders.location)); 
        return loaders.contact.load(obj.contact_crm_id);
      }
    },
    location: {
      type: LocationType,
      description: 'The location of the medical alarm',
      resolve: (obj, args, {loaders}) => {
        return loaders.location.load(obj.location_id);
      }
    }
  })
});

const LocationType = new GraphQLObjectType({
  name: 'Location',
  description: 'A location for internet services',
  fields: () => ({
    id: globalIdField('Location'),
    locationId: {
      type: GraphQLString,
      description: 'Location ID',
      resolve: location => location.location_id,
    },
    rolloutRegionId: {
      type: GraphQLString,
      description: 'Rollout region ID',
      resolve: location => location.rollout_region_id,
    },
    distributionAreaId: {
      type: GraphQLString,
      description: 'Distribution Area ID',
      resolve: location => location.distribution_area_id,
    },
    roadNumber: {
      type: GraphQLString,
      description: 'Road number',
      resolve: location => location.road_number,
    },
    roadSuffixCode: {
      type: GraphQLString,
      description: 'Road suffix code',
      resolve: location => location.road_suffix_code,
    },
    roadTypeCode: {
      type: GraphQLString,
      description: 'Road type code',
      resolve: location => location.road_type_code,
    },
    localityName: {
      type: GraphQLString,
      description: 'Locality name',
      resolve: location => location.locality_name,
    },
    stateTerritoryCode: {
      type: GraphQLString,
      description: 'State or territory code',
      resolve: location => location.state_territory_code,
    },
    fullAddress: {
      type: GraphQLString,
      description: 'Full address',
      resolve: location => location.full_address,
    },
    medicalAlarms: {
      type: new GraphQLList(MedicalAlarmType),
      description: 'Medical alarms for the location',
      resolve: (obj, args, {loaders}) => {
        // console.log('query: medicalAlarms; obj=' + Object.keys(obj));
        // console.log('query: medicalAlarms; args=' + Object.keys(args));
        // console.log('query: medicalAlarms; loaders=' + Object.keys(loaders.location));
        return loaders.medicalAlarm.load(obj.location_id);
      }
    },
    serviceQualification: {
      type: ServiceQualificationType,
      description: 'Service Qualification for the location',
      resolve: (obj, args, {loaders}) => {
        // console.log('query: serviceQual; obj=' + Object.keys(obj));
        // console.log('query: serviceQual; args=' + Object.keys(args));
        // console.log('query: serviceQual; loaders=' + Object.keys(loaders.location));
        return loaders.serviceQual.load(obj.location_id);
      }
    },
    // cases: {
    //   type: new GraphQLList(CaseType),
    //   description: 'Cases and incidents for the location',
    //   resolve: obj => `${obj.first_name} ${obj.last_name}`,
    // },
  }),
  interfaces: [nodeInterface],
});

const QueryType = new GraphQLObjectType({
  name: 'Query',
  description: 'Query for location related data',
  fields: () => ({
    allLocations: {
      type: new GraphQLList(LocationType),
      description: 'All known locations',
      resolve: (root, args, {loaders}) => loaders.location.loadAll(),
    },
    node: nodeField,
    location: {
      type: LocationType,
      args: {
        locationId: {type: new GraphQLNonNull(GraphQLID)},
      },
      resolve: (root, args, {loaders}) => {
        console.log('=> query: location(' + args.locationId + ')');
        return loaders.location.load(args.locationId);
      }
    },
  }),
});

export default new GraphQLSchema({
  query: QueryType,
});
