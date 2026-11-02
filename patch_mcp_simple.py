import sys
sys.path.append('/root/hexstrike-ai')
import hexstrike_mcp
import uvicorn
from starlette.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

class AcceptHeaderMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.url.path == "/mcp":
            headers = request.scope.get("headers", [])
            new_headers = []
            for k, v in headers:
                if k.lower() == b"accept" and b"text/event-stream" not in v:
                    v += b", text/event-stream"
                new_headers.append((k, v))
            request.scope["headers"] = new_headers
        return await call_next(request)

if __name__ == "__main__":
    print("[*] 正在启动带 Accept 修复的 MCP HTTP 服务 (8889端口)...")
    
    # 关键：直接获取原始 app，它会自动携带正确的 lifespan
    app = hexstrike_mcp.mcp.streamable_http_app()
    
    # 只在最外层添加我们的中间件，不创建新的 Starlette 实例
    app.add_middleware(AcceptHeaderMiddleware)
    
    # 直接运行原始 app
    uvicorn.run(app, host="0.0.0.0", port=8889)
