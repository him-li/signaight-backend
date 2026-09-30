import argparse
import uvicorn


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Combined app startup')
    parser.add_argument('--host', required=False,
                        help='app host')
    parser.add_argument('--port', required=False,
                        help='app port')
    parser.add_argument('--reload', required=False,
                        help='reload app on changes', action='store_true')
    parser.add_argument('-w', '--workers', required=False,
                        help='workers qty')
    args = parser.parse_args()
    
    "Run scheduler and the API"
    
    params = {
        "host": "0.0.0.0",
        "port": 8000,
        "log_level": "info",
        "loop": "asyncio",
        "ws": 'websockets'
    }
    if args.host:
        params["host"] = args.host
    if args.port:
        params["port"] = int(args.port)
    if args.reload and not args.workers:
        params["reload"] = True
    elif args.workers:
        params["workers"] = int(args.workers)
    else:
        params["workers"] = 4

    uvicorn.run("api.app:app", **params)
