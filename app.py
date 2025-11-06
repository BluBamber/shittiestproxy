def handle_request(self, client_socket):
    try:
        request = client_socket.recv(1024)
        if not request:
            return  # No request received, so return early
        
        # Decode the request and split by spaces to get the URL
        request_str = request.decode()
        parts = request_str.split()
        
        if len(parts) < 2:  # This means the request is invalid (no URL)
            print("Invalid request: No URL found.")
            client_socket.close()
            return
        
        # Extract URL from the request
        url = parts[1]
        
        # Check if the URL has the correct format
        if "://" in url:
            url = url.split("://")[1]
        else:
            print("Invalid request: No protocol found in URL.")
            client_socket.close()
            return
        
        domain = url.split("/")[0]  # Get the domain part of the URL
        print(f"Proxying request to: {domain}")
        
        # Make the HTTP request to the target URL
        response = requests.get(f'http://{domain}')
        
        # Send the response content back to the client
        client_socket.send(response.content)
    except Exception as e:
        print(f"Error handling request: {e}")
    finally:
        client_socket.close()
