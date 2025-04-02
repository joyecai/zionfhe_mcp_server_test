from mcp.server.fastmcp import FastMCP
import httpx
from typing import List, Dict, Any, Optional
import os

# 初始化FastMCP服务器
mcp = FastMCP("zionfhe_mcp_server")

# 常量
API_KEY = os.getenv("ZIONFHE_APIKEY")
COMPUTE_SERVER_URL = "http://120.46.179.8:8001"  

async def  make_request(url: str, data: dict) -> dict:
    """向FHE计算服务器发送请求"""
    async with httpx.AsyncClient() as client:
        try:
            headers = {"X-API-Key": API_KEY}  # 添加 APIkey 到请求头
            response = await client.post(url, json=data, headers=headers, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e)}

@mcp.tool()
async def fhe_code_execute(code: str, file_url: Optional[str] = None, dependencies: Optional[str] = None) -> str:
    """
    在FHE计算服务器上执行代码。

    Args:
        code: 要执行的代码
        file_url: 可选的文件URL
        dependencies: 可选的依赖项

    Returns:
        代码执行结果或错误消息
    """
    url = f"{COMPUTE_SERVER_URL}/api/fhe_code_execu"
    data = {
        "code": code,
        "fileUrl": file_url,
        "dependencies": dependencies,
    }
    
    result = await make_request(url, data)
    
    if "error" in result:
        return f"代码执行出错：{result['error']}"
    
    if "codeOutput" in result:
        output = result["codeOutput"]
        error = result.get("codeError", "")
        
        if error:
            return f"代码执行结果：\n{output}\n\n错误：\n{error}"
        return f"代码执行结果：\n{output}"
    
    return "未知错误"

@mcp.tool()
async def fhe_encrypt(data) -> str:
    """
    使用FHE加密数据。

    Args:
        data: 要加密的数据，可以是标量或者数组

    Returns:
        加密后的数据或错误消息
    """
    url = f"{COMPUTE_SERVER_URL}/api/encrypt"
    request_data = {
        "plainData": str(data)
    }
    
    result = await make_request(url, request_data)
    
    if result["error"] is not None:
        return f"加密出错：{result['error']}"
    
    if "cipherData" in result:
        return f"加密结果：\n{result['cipherData']}"
    
    return "未知错误"

@mcp.tool()
async def fhe_encrypt_df(data, columns, index):
    """
    使用FHE加密DataFrame类型的数据

    Args：
        data    : 待加密的数据；
        columns ：待加密数据的列名；
        index   ：待加密数据的索引名

    Returns：
        加密后的数据或错误消息
    """
    url = f"{COMPUTE_SERVER_URL}/api/encrypt_df"
    request_data = {
        "data": str(data),
        "columns": str(columns),
        "index": str(index)
    }
    
    result = await make_request(url, request_data)
    print(result)
    
    if result["error"] is not None:
        return f"DataFrame加密出错：{result['error']}"
    
    if "cipherData" in result:
        return f"DataFrame加密结果：\n加密后的数据：{result['cipherData']}\n列名 {result['columns']}\n 索引名 {result['index']}"
    
    return "未知错误，加密DataFrame失败"


@mcp.tool()
async def fhe_decrypt(encrypted_data) -> str:
    """
    使用FHE解密数据。

    Args:
        encrypted_data: 要解密的加密数据

    Returns:
        解密后的数据或错误消息
    """
    url = f"{COMPUTE_SERVER_URL}/api/decrypt"
    request_data = {
        "cipherData": str(encrypted_data)
    }
    
    result = await make_request(url, request_data)
    
    if result["error"] is not None:
        return f"解密出错：{result['error']}"
    
    if "plainData" in result:
        return f"解密结果：\n{result['plainData']}"
    
    return "未知错误"

@mcp.tool()
async def fhe_decrypt_df(encrypted_data, columns, index) -> str:
    """
    使用FHE解密加密的DataFrame数据。

    Args:
        encrypted_data: 要解密的加密数据
        columns：加密DataFrame的列名
        index：加密DataFrame的索引


    Returns:
        解密后的数据或错误消息
    """
    url = f"{COMPUTE_SERVER_URL}/api/decrypt_df"
    request_data = {
        "cipherData": str(encrypted_data),
        "columns": str(columns),
        "index": str(index),
    }
    
    result = await make_request(url, request_data)
    
    if result["error"] is not None:
        return f"解密出错：{result['error']}"
    
    if "plainData" in result:
        return f"解密结果：\n{result['plainData']}"
    
    return "未知错误"

# if __name__ == "__main__":
#     # 初始化并运行服务器
#     mcp.run(transport='stdio')
#     pass
if __name__ == "__main__":
    # mcp.run(transport="sse")
    
    from uvicorn import run as uvicorn_run
    # 具体如何run，取决于客户端绑定的IP地址类型
    uvicorn_run(mcp.sse_app(), host="::", port=8000)