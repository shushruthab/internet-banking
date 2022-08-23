## Satoz Bank Internet Banking App
Full-stack internet banking app.

![Final App](/static/demo.gif)

This project uses the following technologies:

- HTML, CSS, Materialize CSS for the frontend
- Python, Flask for the backend
- Postgresql for the database
- Testing and Validation tool such as insomnia to simulate purchases. 

## Configuration
Add your own [Flask] key in

1. `/app.py`

```
app.config["SECRET_KEY"] = "your_key"
```

## Quick Start
 
```python
# Install dependencies for server & client
pip install -r requirements.txt

# Run server
flask --debug run 

# Server runs on http://localhost:5000 
```

## Credentials for testing
To test the app, use any of the following credentials.

1. username: testuser1, password: 123456
2. username: testuser2, password: 123456
3. username: testuser3, password: 123456

## Simulate Purchases
To simulate a purchase, send a post request to `http://localhost:5000/<username>/purchase` using a tool like insomnia. Following is an example of a sample request.

![Final App](/static/purchase_demo.png)