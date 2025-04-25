from fastapi import Request

# @app.middleware('http')
async def log_client_ip(request: Request, call_next):
    client_ip = request.client.host
    print(f"Client IP: {client_ip}")

    response = await call_next(request)
    return response