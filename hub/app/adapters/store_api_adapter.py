import json
import logging
from typing import List

import requests

from app.entities.processed_agent_data import ProcessedAgentData
from app.interfaces.store_gateway import StoreGateway


class StoreApiAdapter(StoreGateway):
    def __init__(self, api_base_url):
        self.api_base_url = api_base_url

    def save_data(self, processed_agent_data_batch: List[ProcessedAgentData]) -> bool:
        """
        Save the processed road data to the Store API.
        Parameters:
            processed_agent_data_batch (dict): Processed road data to be saved.
        Returns:
            bool: True if the data is successfully saved, False otherwise.
        """
        if isinstance(processed_agent_data_batch, dict):
            # Case 1: If input is a dictionary, assume it's already formatted and send directly
            data = processed_agent_data_batch
        elif isinstance(processed_agent_data_batch, list):
            # Case 2: If input is a list, assume it needs to be processed and serialized
            data = [json.loads(item.json()) if hasattr(item, 'json') else item for item in processed_agent_data_batch]
        else:
            # Handle other cases or raise an exception based on your specific requirements
            logging.error(f"Unsupported data type: {type(processed_agent_data_batch)}")
            return False

        try:
            response = requests.post(f"{self.api_base_url}/processed_agent_data/", json=data)
            response.raise_for_status()
        except requests.RequestException as e:
            logging.error(f"Error while saving data to Store API: {e}. Data : {data}")
            return False

        return response.status_code == requests.codes.ok