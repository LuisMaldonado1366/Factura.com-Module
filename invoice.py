# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# invoice.py

"""
Description: This script is used to manipulate the API Rest for the site 'factura.com',
    it intends to create, update and retrieve all clients data stored by the site.
    It is capable of interacting with production and sandbox development.
Author: Luis Maldonado
Created on: Tue Apr 30 11:36:52 2024
Modified on: Thu May  02 15:21:16 2024
Version: 1.0.0
Dependencies: http.client, json.
"""

################################## Libraries ##################################
# Standard.
import http.client
import json

################################### Classes ###################################

class Invoice:
    """
    A class for connection and managment of factura.com API Rest

    Attributes:
        _endpoint (str): 
        _url (str): 
        _headers (dict): 
        _endpoint (str): 
        __client_clean__ (dict): 
            
    """

    def __init__(self, api_key: str, api_secret: str, mode: str) -> None:
        """
        Resume: Class constructor.
        Description: Creates an object of the class associating the API Rest
            Credentials and endpoint accordingly to the declared mode.
        Args:
            api_key (str): 
            api_secret (str): 
            mode (str): 
            
        Returns:
            None
        """
        if mode == 'Live':
            self._endpoint = 'api.factura.com'
            self._url = ''
        else:
            self._endpoint = 'sandbox.factura.com'
            self._url = '/api'
        self._headers = {'Content-Type': 'application/json',
                         'F-PLUGIN': '9d4095c8f7ed5785cb14c0e3b033eeb8252416ed',
                         'F-Api-Key': f'{api_key}',
                         'F-Secret-Key': f'{api_secret}'}
        self.__client_clean__ = {
            'calle': '',
            'colonia': '',
            'numero_exterior': '',
            'numero_interior': '',
            'ciudad': '',
            'delegacion': '',
            'localidad': '',
            'estado': '',
            'numregidtrib': '',
            'usdocfdi': ''
        }


    def update_client(self, uid: str, **kwargs: dict) -> dict:
        """
        Resume: Updates the client's data by using the uid and a payload.
        Description: Updates the client's data using the API Rest of the site
            'factura.com' by using the uid, if any data is present in the keyword
            arguments, it sends it along with the default data __client_clean__,
            otherwise it acts as a cleaning tool for the client.
        Args:
            uid (str): 'factura.com' unique identifier for a client.
            **kwargs: Additional keyword arguments:
                - client_data (dict): data to be sent to the client, if so gets
                    updated, otherwise, it just cleans the current client's garbage info.
            
        Returns:
            dict: Response from the operation.
        """
        if 'client_data' in kwargs:
            _payload = json.dumps({**kwargs['client_data'], **self.__client_clean__})
        else:
            _payload = json.dumps(obj = self.__client_clean__)

        _connection = http.client.HTTPSConnection(self._endpoint)
        _url = self._url + f'/v1/clients/{uid}/update'
        _connection.request(method = 'POST',
                            url = _url,
                            body = _payload,
                            headers = self._headers)
        _response = _connection.getresponse()
        _data = _response.read()

        return json.loads(_data.decode('UTF-8'))


    def create_client(self, client_data: dict) -> dict:
        """
        Resume: Creates a client with the given data.
        Description: Creates a client using the API Rest of the site 'factura.com'
            by pasing the client's data.
        Args:
            client_data (dict): data to be sent to the API.
            
        Returns:
            dict: Response from the operation.
        """
        _payload = json.dumps({**{
          'email': f'{client_data["email"]}',
          'razons': f'{client_data["nombre"]}',
          'rfc': f'{client_data["rfc"]}',
          'regimen': f'{client_data["id_regimen_fiscal"]}',
          'codpos': f'{client_data["codpos"]}'
        }, **self.__client_clean__})
        _connection = http.client.HTTPSConnection(self._endpoint)
        _url = self._url + '/v1/clients/create'
        _connection.request(method = 'POST',
                            url = _url,
                            body = _payload,
                            headers = self._headers)
        _response = _connection.getresponse()
        _data = _response.read()

        return json.loads(_data.decode('UTF-8'))


    def get_clients(self) -> dict:
        """
        Resume: List all clients registered to the site.
        Description: List all existing clients using the API Rest of the site
            'factura.com'.
        Args:
            None.
            
        Returns:
            dict: Response from the operation.
        """
        _connection = http.client.HTTPSConnection(self._endpoint)
        _url = self._url + '/v1/clients'
        _connection.request(method = 'GET',
                            body = '',
                            url = _url,
                            headers = self._headers)
        _response = _connection.getresponse()
        _data = _response.read()

        return json.loads(_data.decode('UTF-8'))
