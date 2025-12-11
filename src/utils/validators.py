def validate_query(query):
    """Validate user query"""
    if not query or not query.strip():
        return False, "Query cannot be empty"
    
    if len(query) > 500:
        return False, "Query too long (max 500 characters)"
    
    return True, "Valid"