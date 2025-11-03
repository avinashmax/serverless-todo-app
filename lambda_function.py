import json
import boto3
import uuid
from datetime import datetime

# Initialize DynamoDB
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('TodoTable')

# -----------------------------
# 1 CREATE ToDo
# -----------------------------
def create_todo(event):
    body = json.loads(event.get('body') or '{}')
    task = body.get('task')
    if not task:
        return {'statusCode': 400, 'body': json.dumps({'error': 'task is required'})}

    todo_item = {
        'id': str(uuid.uuid4()),
        'task': task,
        'status': body.get('status', 'pending'),
        'created_at': datetime.utcnow().isoformat()
    }

    table.put_item(Item=todo_item)
    return {'statusCode': 201, 'body': json.dumps({'message': 'ToDo created', 'item': todo_item})}


# -----------------------------
# 2 GET All ToDos
# -----------------------------
def get_todos(event):
    response = table.scan()
    items = response.get('Items', [])
    return {'statusCode': 200, 'body': json.dumps(items)}


# -----------------------------
# 3 UPDATE ToDo by ID
# -----------------------------
def update_todo(event):
    todo_id = event.get('pathParameters', {}).get('id')
    body = json.loads(event.get('body') or '{}')
    new_status = body.get('status')
    new_task = body.get('task')

    if not todo_id:
        return {'statusCode': 400, 'body': json.dumps({'error': 'id (in path) is required'})}

    update_expression = []
    expression_values = {}
    expression_names = {}

    if new_status:
        update_expression.append('#s = :s')
        expression_values[':s'] = new_status
        expression_names['#s'] = 'status'

    if new_task:
        update_expression.append('#t = :t')
        expression_values[':t'] = new_task
        expression_names['#t'] = 'task'

    if not update_expression:
        return {'statusCode': 400, 'body': json.dumps({'error': 'No fields to update'})}

    response = table.update_item(
        Key={'id': todo_id},
        UpdateExpression='SET ' + ', '.join(update_expression),
        ExpressionAttributeNames=expression_names,
        ExpressionAttributeValues=expression_values,
        ReturnValues='ALL_NEW'
    )

    return {'statusCode': 200, 'body': json.dumps({'message': 'ToDo updated', 'item': response['Attributes']})}


# -----------------------------
# 4 DELETE ToDo by ID
# -----------------------------
def delete_todo(event):
    todo_id = event.get('pathParameters', {}).get('id')

    if not todo_id:
        return {'statusCode': 400, 'body': json.dumps({'error': 'id is required'})}

    table.delete_item(Key={'id': todo_id})
    return {'statusCode': 200, 'body': json.dumps({'message': 'ToDo deleted', 'deleted_id': todo_id})}


# -----------------------------
#  Main Lambda Handler
# -----------------------------
def lambda_handler(event, context):
    """
    Handles API Gateway requests for CRUD operations.
    Routes based on HTTP method.
    """
    http_method = event.get('httpMethod', '')

    try:
        if http_method == 'POST':
            return create_todo(event)
        elif http_method == 'GET':
            return get_todos(event)
        elif http_method == 'PUT':
            return update_todo(event)
        elif http_method == 'DELETE':
            return delete_todo(event)
        else:
            return {'statusCode': 405, 'body': json.dumps({'error': 'Method Not Allowed'})}
    except Exception as e:
        return {'statusCode': 500, 'body': json.dumps({'error': str(e)})}
