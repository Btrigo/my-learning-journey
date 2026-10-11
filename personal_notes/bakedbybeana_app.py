"""Learning project: local mock bakery + optional AWS CDK infrastructure.

Local preview: python bakedbybeana_app.py --local
CDK config:   {"app": "python bakedbybeana_app.py"}
Install CDK Python dependencies: pip install aws-cdk-lib constructs
Generate template: cdk synth
"""
import html
import sys
from urllib.parse import parse_qs

# Prices use whole cents to avoid floating-point money calculations.
PRODUCTS = [
    {"id": "cookie", "name": "Chocolate Chip Cookie", "price": 350},
    {"id": "brownie", "name": "Fudge Brownie", "price": 450},
    {"id": "cupcake", "name": "Vanilla Cupcake", "price": 500},
]


def money(cents):
    return f"${cents / 100:.2f}"


def checkout(form):
    total = 0
    count = 0
    for product in PRODUCTS:
        raw_quantity = form.get(product["id"], ["0"])[0]
        try:
            quantity = int(raw_quantity)
        except ValueError:
            return "Please enter whole-number quantities.", 400
        if quantity < 0 or quantity > 20:
            return "Choose between 0 and 20 of each item.", 400
        total += product["price"] * quantity
        count += quantity
    if count == 0:
        return "Choose at least one baked good.", 400
    return f"Demo order: {count} items. Total: {money(total)}. No payment taken; no order saved.", 200


def page(message=""):
    cards = []
    for product in PRODUCTS:
        cards.append(f'''
        <article>
          <h2>{html.escape(product["name"])}</h2>
          <p>{money(product["price"])}</p>
          <label>Quantity
            <input type="number" name="{product["id"]}" min="0" max="20" value="0">
          </label>
        </article>''')
    return f'''<!doctype html>
    <html lang="en"><head><meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>BakedByBeana — Demo Bakery</title>
    <style>
      body {{font-family:system-ui;max-width:850px;margin:60px auto;padding:20px;background:#fff7ee;color:#473126}}
      h1 {{font-size:42px}} .products {{display:flex;flex-wrap:wrap;gap:16px}}
      article {{background:white;padding:22px;border-radius:16px;flex:1;min-width:180px}}
      input {{display:block;width:70px;padding:8px;margin-top:8px}}
      button {{margin-top:24px;padding:14px 24px;border:0;border-radius:10px;background:#754b38;color:white;font-size:16px}}
      .message {{padding:16px;background:#ffe3be;border-radius:10px}}
    </style></head><body>
      <h1>BakedByBeana</h1><p>Small-batch treats, baked with love.</p>
      <p>Learning demo — checkout calculates a total only.</p>
      {('<p class="message" role="status">' + html.escape(message) + '</p>') if message else ''}
      <form method="post" action="/checkout">
        <div class="products">{''.join(cards)}</div>
        <button type="submit">Try mock checkout</button>
      </form>
    </body></html>'''


def respond(method, path, body=""):
    if method == "GET" and path == "/":
        return page(), 200
    elif method == "POST" and path == "/checkout":
        message, status = checkout(parse_qs(body))
        return page(message), status
    else:
        return page("Page not found."), 404


def handler(event, context):
    import base64
    request = event["requestContext"]["http"]
    body = event.get("body") or ""
    if event.get("isBase64Encoded"):
        body = base64.b64decode(body).decode("utf-8")
    content, status = respond(request["method"], request["path"], body)
    return {"statusCode": status, "headers": {"Content-Type": "text/html; charset=utf-8"}, "body": content}


def run_local():
    from http.server import BaseHTTPRequestHandler, HTTPServer

    class BakeryHandler(BaseHTTPRequestHandler):
        def serve(self):
            length = int(self.headers.get("Content-Length", "0"))
            body = self.rfile.read(length).decode("utf-8")
            content, status = respond(self.command, self.path.split("?")[0], body)
            self.send_response(status)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(content.encode("utf-8"))

        def do_GET(self):
            self.serve()

        def do_POST(self):
            self.serve()

    print("Open http://localhost:8000 — press Ctrl+C to stop.")
    HTTPServer(("127.0.0.1", 8000), BakeryHandler).serve_forever()


def build_infrastructure():
    from pathlib import Path
    from aws_cdk import App, Stack, Duration, CfnOutput
    from aws_cdk import aws_lambda as lambda_
    from constructs import Construct

    class BakeryStack(Stack):
        def __init__(self, scope: Construct, construct_id: str, **kwargs):
            super().__init__(scope, construct_id, **kwargs)
            # Inline code keeps this learning project in a single file.
            source = Path(__file__).read_text(encoding="utf-8")
            storefront = lambda_.Function(
                self, "Storefront",
                runtime=lambda_.Runtime.PYTHON_3_12,
                handler="index.handler",
                code=lambda_.Code.from_inline(source),
                memory_size=128,
                timeout=Duration.seconds(5),
            )
            url = storefront.add_function_url(
                auth_type=lambda_.FunctionUrlAuthType.NONE,
            )
            CfnOutput(self, "BakeryUrl", value=url.url)

    app = App()
    BakeryStack(app, "BakedByBeanaDemo")
    app.synth()


if __name__ == "__main__":
    if "--local" in sys.argv:
        run_local()
    else:
        build_infrastructure()
