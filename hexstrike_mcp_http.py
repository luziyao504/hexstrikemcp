import sys
sys.path.append('/root/hexstrike-ai')
import hexstrike_mcp
from mcp.server.fastmcp import FastMCP

if __name__ == "__main__":
    print("[*] Starting HexStrike MCP over Streamable HTTP on port 8889...")
    
    # 1. 创建一个新的 FastMCP 实例
    mcp = FastMCP("hexstrike-ai-mcp")
    
    # 2. 调用原脚本中的 setup 函数，将工具注册到这个实例上
    # 注意：这里假设 setup_mcp_server() 接受 mcp 实例作为参数。
    # 如果报错，请检查 hexstrike_mcp.py 中该函数的定义。
    try:
        hexstrike_mcp.setup_mcp_server(mcp)
    except AttributeError:
        print("[!] 警告: 'setup_mcp_server' 函数不存在，尝试直接复用原实例...")
        # 部分版本可能直接暴露了 mcp 变量，可以尝试直接使用
        mcp = hexstrike_mcp.mcp 
    
    # 3. 以 Streamable HTTP 模式启动
    mcp.run(transport="streamable-http", host="0.0.0.0", port=8889)
