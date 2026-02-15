import hashlib
import time

def calculate_status(physical_progress, expenditure, planned_cost):
    """
    Determines the status of the project based on progress and cost.
    
    Args:
        physical_progress (float): Physical progress in percentage (0-100).
        expenditure (float): Expenditure till date.
        planned_cost (float): Total planned cost.
        
    Returns:
        str: Status string (ON_TRACK, DELAYED, COST_OVERRUN, or combination).
    """
    status_flags = []
    
    if physical_progress is not None and physical_progress < 50:
        status_flags.append("DELAYED")
        
    if expenditure is not None and planned_cost is not None and expenditure > planned_cost:
        status_flags.append("COST_OVERRUN")
        
    if not status_flags:
        return "ON_TRACK"
    
    return " | ".join(status_flags)

def generate_project_id(project_name):
    """
    Generates a deterministic project ID based on the project name.
    
    Args:
        project_name (str): Name of the project.
        
    Returns:
        str: A short hash identifying the project.
    """
    if not project_name:
        return f"UNK-{int(time.time())}"
    
    # Create a short hash of the project name
    hash_object = hashlib.md5(project_name.encode())
    return f"PROJ-{hash_object.hexdigest()[:6].upper()}"
