import requests
import logging


def check_third_party_service(service_name, service_url, timeout=5):
    """
    Helper function to check the health of a third-party service.

    Args:
        service_name (str): The name of the service.
        service_url (str): The endpoint to check.
        timeout (int): Timeout in seconds.

    Returns:
        dict: The health status of the service.
    """
    try:
        response = requests.get(service_url, timeout=timeout)
        response.raise_for_status()
        return {service_name: {"status": "healthy"}}
    except requests.exceptions.RequestException as e:
        logging.error(f"{service_name} error: {e}")
        return {service_name: {"status": "unhealthy", "error": str(e)}}
