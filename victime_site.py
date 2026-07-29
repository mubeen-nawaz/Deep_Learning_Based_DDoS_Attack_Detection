from flask import Flask, render_template_string

app = Flask(__name__)

# A professional looking business landing page
VICTIM_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Global Bank - Secure Portal</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        .loading-bar { height: 4px; width: 100%; background: #e2e8f0; position: fixed; top: 0; }
        .loading-progress { height: 100%; background: #3b82f6; width: 30%; animation: move 2s infinite; }
        @keyframes move { 0% { margin-left: -30%; } 100% { margin-left: 100%; } }
    </style>
</head>
<body class="bg-gray-50">
    <div class="loading-bar"><div class="loading-progress"></div></div>
    <nav class="bg-white shadow-sm p-4 flex justify-between items-center">
        <h1 class="text-xl font-bold text-blue-900">GLOBAL BANK</h1>
        <div class="space-x-4 text-gray-600"><span>Services</span><span>Login</span></div>
    </nav>
    <main class="max-w-4xl mx-auto mt-20 text-center">
        <h2 class="text-5xl font-extrabold text-gray-900 mb-4">Your Trust, Our Priority.</h2>
        <p class="text-lg text-gray-600">Welcome to our high-availability secure banking portal.</p>
        <div class="mt-10 p-10 bg-white shadow-xl rounded-2xl border border-gray-100">
            <p class="text-sm text-green-500 font-bold">● SYSTEM STATUS: OPTIMAL</p>
        </div>
    </main>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(VICTIM_HTML)

if __name__ == '__main__':
    app.run(port=8080)