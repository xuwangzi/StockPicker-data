# run.py

from app import app

def print_routes(app):
    for rule in app.url_map.iter_rules():
        methods = ','.join(rule.methods) or 'GET'
        line = f"{rule} {methods}"
        print(line)
@app.route('/')
def init():
    return 'Hello, World!'

if __name__ == '__main__':
    # 调用print_routes函数打印路由信息
    print_routes(app)

    app.run(debug=True, threaded=False)