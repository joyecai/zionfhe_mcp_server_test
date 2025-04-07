## What is Zionfhe_mcp_server_test?
Zionfhe_mcp_server_test is a server implementation based on the new homomorphic encryption technology ZIONFHE, designed to provide secure computation capabilities.
## How to use Zionfhe_mcp_server_test?
1. Clone the repository and then go to the directory.
2. Contact the developer to get the apikey, then create a configuration file ```.env``` to configure the environment variables:  
```ZIONFHE_APIKEY=<YOUR APIKEY>```
3. Run the following command to install the package management software uv:  
```pip install uv```
4. Use the following command to update the dependency package:  
```uv sync```
5. Use the following command to run the mcp server:  
```uv run --env-file .env main.py```  
> The MCP Server will run on port 8000.
6. Connect to the server in sse mode using the client.  
[client_config](https://gitlab.com/phantaverse-tech/ai-product/zionfhe_mcp_server/-/blob/dev/mcp_server/client_config.png?ref_type=heads)