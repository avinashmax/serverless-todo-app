# 🧩 Serverless To-Do Application (AWS Lambda + API Gateway + DynamoDB)

A fully **serverless To-Do API** built with **AWS Lambda**, **API Gateway**, and **DynamoDB** — designed for beginners learning AWS Cloud & Python integration.  
This app supports **Create, Read, Update, and Delete (CRUD)** operations using **a single Lambda function**.

---

## ⚙️ Features
- Single Lambda function handles all CRUD operations  
- DynamoDB for To-Do storage  
- API Gateway provides REST endpoints  
- 100 % Serverless — no servers to manage  
- Written in Python using `boto3`

---

## 🧱 Architecture Diagram
```
                 ┌────────────────────────────┐
                 │     Client (Postman / UI)   │
                 └──────────────┬──────────────┘
                                │ HTTPS
                                ▼
                 ┌────────────────────────────┐
                 │     Amazon API Gateway      │
                 │  Routes: /todos , /todos/{id} │
                 └──────────────┬──────────────┘
                                │
                                ▼
                 ┌────────────────────────────┐
                 │     AWS Lambda (Python)     │
                 │  Single Function: CRUD Ops  │
                 └──────────────┬──────────────┘
                                │
                                ▼
                 ┌────────────────────────────┐
                 │     Amazon DynamoDB Table   │
                 │  Table: TodoTable (id: str) │
                 └────────────────────────────┘
```

---

## 🪣 AWS Console Setup (Recommended)

### **Step 1 – Create DynamoDB Table**
1. Go to **AWS Console → DynamoDB → Tables → Create table**
2. Table name → `TodoTable`
3. Partition key → `id` (String)
4. Leave defaults → **Create Table**

---

### **Step 2 – Create Lambda Function**
1. Go to **AWS Console → Lambda → Create function**
2. Choose **Author from scratch**
3. Function name → `ServerlessToDoFunction`
4. Runtime → **Python 3.9 or later**
5. Permissions → Attach **AmazonDynamoDBFullAccess**
6. Click **Create Function**
7. Paste your `lambda_function.py` code in the editor
8. Click **Deploy**

> 🧩 This one function handles all 4 methods (POST, GET, PUT, DELETE)

---

### **Step 3 – Create API Gateway**
1. **API Gateway → Create API → HTTP API → Build**
2. Name → `ToDoAPI`
3. Create these routes:

| Method | Path | Description |
|--------|------|-------------|
| POST | `/todos` | Create To-Do |
| GET | `/todos` | Get all To-Dos |
| PUT | `/todos/{id}` | Update To-Do |
| DELETE | `/todos/{id}` | Delete To-Do |

4. For **each route**, choose:
   - Integration type → **Lambda**
   - Function → `ServerlessToDoFunction`
5. Deploy the API → Create a stage called `prod`
6. Copy your **Invoke URL** — example:
   ```
   https://abc123.execute-api.ap-south-1.amazonaws.com/prod
   ```

---

### **Step 4 – Test with Postman**

| Operation | Method | Endpoint | Body Example |
|------------|---------|-----------|---------------|
| Create | POST | `/todos` | `{ "task": "Learn AWS Lambda" }` |
| Read | GET | `/todos` | — |
| Update | PUT | `/todos/{id}` | `{ "status": "completed" }` |
| Delete | DELETE | `/todos/{id}` | — |

Example URL:  
```
https://abc123.execute-api.ap-south-1.amazonaws.com/prod/todos
```

---

## 💻 Local Setup (For VS Code Users)

If you prefer to test or modify the API locally before deploying to AWS:

### **1. Create and activate a virtual environment**
```bash
python -m venv venv
venv\Scripts\activate   # On Windows
source venv/bin/activate  # On Mac/Linux
```

### **2. Install Dependencies**
```bash
pip install -r requirements.txt
```

### **3. Set AWS credentials**
```bash
aws configure
```

### **4. Run the script locally**
```bash
python lambda_function.py
```

### **5. Test locally using Postman or curl**
```bash
curl -X POST http://localhost:8000/todos -H "Content-Type: application/json" -d '{"task": "Test local To-Do", "status": "pending"}'
```

---

## 📦 Example Inputs and Outputs

### ➕ Create To-Do (POST)
**Input**
```json
{
  "task": "Complete AWS Serverless To-Do App",
  "status": "pending"
}
```
**Output**
```json
{
  "message": "ToDo created",
  "item": {
    "id": "e43664c5-6ebc-4d28-987a-cc2c99b5fdee",
    "task": "Complete AWS Serverless To-Do App",
    "status": "pending",
    "created_at": "2025-11-03T10:51:40.727920"
  }
}
```

### 📋 Get All To-Dos (GET)
**Output**
```json
[
  {
    "id": "e43664c5-6ebc-4d28-987a-cc2c99b5fdee",
    "task": "Complete AWS Serverless To-Do App",
    "status": "pending",
    "created_at": "2025-11-03T10:51:40.727920"
  }
]
```

### ✏️ Update To-Do (PUT)
**Input**
```json
{
  "status": "completed"
}
```
**Output**
```json
{
  "message": "ToDo updated",
  "item": {
    "id": "e43664c5-6ebc-4d28-987a-cc2c99b5fdee",
    "task": "Complete AWS Serverless To-Do App",
    "status": "completed",
    "created_at": "2025-11-03T10:51:40.727920"
  }
}
```

### ❌ Delete To-Do (DELETE)
**Output**
```json
{
  "message": "ToDo deleted successfully",
  "deleted_id": "e43664c5-6ebc-4d28-987a-cc2c99b5fdee"
}
```

---

## 🧩 How to Run This Project Locally

This project’s Lambda function can be tested in two ways — **connected to AWS** or **offline**.

### 🟢 Option 1: AWS-Connected Local Test (Real DynamoDB)
If you have AWS CLI configured (`aws configure`), and a DynamoDB table named `TodoTable`, follow these steps:
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python lambda_function.py
```
You’ll see the simulated event result printed in your terminal.

Example output:
```json
{
  "statusCode": 201,
  "body": "{\"message\": \"ToDo created\", \"item\": {\"id\": \"abc123\", \"task\": \"Learn AWS Serverless\", \"status\": \"pending\"}}"
}
```

---

### 🔵 Option 2: Offline Mock Test (No AWS Required)
To test without AWS:

1. Open `lambda_function.py`
2. Add this code block **before** your DynamoDB initialization:
   ```python
   class MockTable:
       def __init__(self):
           self.storage = {}

       def put_item(self, Item):
           self.storage[Item["id"]] = Item

       def scan(self):
           return {"Items": list(self.storage.values())}

       def update_item(self, Key, UpdateExpression=None, ExpressionAttributeNames=None, ExpressionAttributeValues=None, ReturnValues=None):
           item = self.storage.get(Key["id"])
           if not item:
               return {"Attributes": {}}
           if ":s" in ExpressionAttributeValues:
               item["status"] = ExpressionAttributeValues[":s"]
           if ":t" in ExpressionAttributeValues:
               item["task"] = ExpressionAttributeValues[":t"]
           self.storage[Key["id"]] = item
           return {"Attributes": item}

       def delete_item(self, Key):
           self.storage.pop(Key["id"], None)

   # Uncomment below line for offline testing
   # table = MockTable()
   ```
3. Comment out your DynamoDB line:
   ```python
   # table = dynamodb.Table('TodoTable')
   ```
4. Run:
   ```bash
   python lambda_function.py
   ```

Example output:
```json
{
  "statusCode": 201,
  "body": "{\"message\": \"ToDo created (mock)\", \"item\": {\"id\": \"1234\", \"task\": \"Test offline mode\", \"status\": \"pending\"}}"
}
```

---

## 👨‍💻 Author
**Avinash S**  
AWS Cloud Engineer | Python Developer  
📂 GitHub: [https://github.com/avinashmax](https://github.com/avinashmax)
