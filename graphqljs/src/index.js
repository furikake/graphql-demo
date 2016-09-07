import DataLoader from 'dataloader';
import express from 'express';
import fetch from 'node-fetch';
import graphqlHTTP from 'express-graphql';
import GraphQLSchema from 'graphql';
import schema from './schema';

console.log('starting graphqljs app');

const BASE_URL = 'http://restapi:8000';

function getJSONFromRelativeURL(relativeURL) {
  var url = `${BASE_URL}${relativeURL}`;
  console.log('HTTP: ' + url);
  return fetch(url, { 
    headers: { 
      Accept: 'application/json', 
      'Content-Type': 'application/json' }})
  .then(res => {
    console.log('Response is ' + res.status);
    return res.json();
  });
}

function getAddress(locationId) {
  console.log('getAddress(' + locationId + ')');  
  return getJSONFromRelativeURL(`/addresses/${locationId}`);
}

function getMedicalAlarms(locationId) {
  console.log('getMedicalAlarms(' + locationId + ')');
  return getJSONFromRelativeURL(`/medical-alarms/${locationId}`);
}

function getServiceQual(locationId) {
  console.log('getServiceQual(' + locationId + ')');
  return getJSONFromRelativeURL(`/service-qualifications/${locationId}`);
}

function getContact(contactId) {
  console.log('getContact(' + contactId + ')');
  return getJSONFromRelativeURL(`/contacts/${contactId}`);
}

function getAddressByURL(relativeURL) {
  return getJSONFromRelativeURL(relativeURL);
}

const app = express();

app.use('/graphql', graphqlHTTP(req => {
  const addressCacheMap = new Map();
  const medicalAlarmMap = new Map();
  const serviceQualMap = new Map();
  const contactMap = new Map();

  const locationLoader =
    new DataLoader(keys => Promise.all(keys.map(getAddress)), {addressCacheMap});
  const medicalAlarmLoader = 
    new DataLoader(keys => Promise.all(keys.map(getMedicalAlarms)), {medicalAlarmMap});
  const serviceQualLoader = 
    new DataLoader(keys => Promise.all(keys.map(getServiceQual)), {serviceQualMap});
  const contactLoader = 
    new DataLoader(keys => Promise.all(keys.map(getContact)), {contactMap});

  const loaders = {
    location: locationLoader, 
    medicalAlarm: medicalAlarmLoader,
    serviceQual: serviceQualLoader,
    contact: contactLoader,
  };

  return {
    context: {loaders},
    graphiql: true,
    schema,
    formatError: error => ({
      message: error.message,
      locations: error.locations,
      stack: error.stack
    }),
  };
}));

app.listen(
  5000,
  () => console.log('GraphQL Server running at http://localhost:5000')
);