import json
import boto3
from datetime import datetime

# Initialize DynamoDB client (optional - for data persistence)
dynamodb = boto3.resource('dynamodb')
# table = dynamodb.Table('YourTableName')

def lambda_handler(event, context):
    """
    Main Lambda handler for API Gateway requests
    """
    
    # Get HTTP method and path
    http_method = event.get('httpMethod')
    path = event.get('path')
    
    # CORS headers
    headers = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Allow-Methods': 'GET,POST,PUT,DELETE,OPTIONS'
    }
    
    try:
        # Route based on HTTP method and path
        if http_method == 'OPTIONS':
            return create_response(200, {'message': 'OK'}, headers)
        
        elif http_method == 'GET' and path == '/items':
            return handle_get_items(event, headers)
        
        elif http_method == 'GET' and path.startswith('/items/'):
            return handle_get_item(event, headers)
        
        elif http_method == 'POST' and path == '/items':
            return handle_create_item(event, headers)
        
        elif http_method == 'PUT' and path.startswith('/items/'):
            return handle_update_item(event, headers)
        
        elif http_method == 'DELETE' and path.startswith('/items/'):
            return handle_delete_item(event, headers)
        
        else:
            return create_response(404, {'error': 'Not Found'}, headers)
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return create_response(500, {'error': 'Internal Server Error'}, headers)


def handle_get_items(event, headers):
    """Get all items"""
    # Mock data - replace with actual database query
    items = [
        {'id': '1', 'name': 'Item 1', 'description': 'First item'},
        {'id': '2', 'name': 'Item 2', 'description': 'Second item'}
    ]
    return create_response(200, {'items': items}, headers)


def handle_get_item(event, headers):
    """Get a single item by ID"""
    item_id = event['path'].split('/')[-1]
    
    # Mock data - replace with actual database query
    item = {'id': item_id, 'name': f'Item {item_id}', 'description': 'Sample item'}
    return create_response(200, item, headers)


def handle_create_item(event, headers):
    """Create a new item"""
    body = json.loads(event.get('body', '{}'))
    
    # Validate input
    if not body.get('name'):
        return create_response(400, {'error': 'Name is required'}, headers)
    
    # Mock creation - replace with actual database insert
    new_item = {
        'id': str(datetime.now().timestamp()),
        'name': body['name'],
        'description': body.get('description', ''),
        'createdAt': datetime.now().isoformat()
    }
    
    return create_response(201, new_item, headers)


def handle_update_item(event, headers):
    """Update an existing item"""
    item_id = event['path'].split('/')[-1]
    body = json.loads(event.get('body', '{}'))
    
    # Mock update - replace with actual database update
    updated_item = {
        'id': item_id,
        'name': body.get('name', 'Updated Item'),
        'description': body.get('description', ''),
        'updatedAt': datetime.now().isoformat()
    }
    
    return create_response(200, updated_item, headers)


def handle_delete_item(event, headers):
    """Delete an item"""
    item_id = event['path'].split('/')[-1]
    
    # Mock deletion - replace with actual database delete
    return create_response(200, {'message': f'Item {item_id} deleted successfully'}, headers)


def create_response(status_code, body, headers):
    """Create HTTP response"""
    return {
        'statusCode': status_code,
        'headers': headers,
        'body': json.dumps(body)
    }