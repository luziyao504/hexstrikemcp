import sys
sys.path.append('/root/hexstrike-ai')

import hexstrike_mcp
import uvicorn
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

# 自定义中间件：强行修改前端发来的 Accept 请求头
class ForceAcceptHeaderMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.url.path == "/mcp":
            headers = request.scope.get("headers", [])
            new_headers = []
            has_accept = False
            
            # 遍历原始请求头
            for key, value in headers:
                if key.lower() == b"accept":
                    has_accept = True
                    # 如果没有 text/event-stream，强行加上去
                    if b"text/event-stream" not in value:
                        value += b", text/event-stream"
                new_headers.append((key, value))
                
            # 如果连 Accept 都没有，直接补全
            if not has_accept:
                new_headers.append((b"accept", b"application/json, text/event-stream"))
                
            request.scope["headers"] = new_headers
            
        return await call_next(request)

if __name__ == "__main__":
    print("[*] 正在启动带 Header 修复的 MCP HTTP 服务 (8889端口)...")
    
    # 1. 获取 hexstrike_mcp.py 中原生的 Starlette 应用
    original_app = hexstrike_mcp.mcp.streamable_http_app()
    
    # 2. 把中间件和原生应用缝合起来
    patched_app = Starlette(
        debug=original_app.debug,
        routes=original_app.routes,
        middleware=[Middleware(ForceAcceptHeaderMiddleware)],
        lifespan=original_app.lifespan
    )
    
    # 3. 直接跑在 8889 端口
    uvicorn.run(patched_app, host="0.0.0.0", port=8889)
