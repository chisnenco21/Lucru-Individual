
from flask import Flask, jsonify
import psutil

app = Flask(__name__)

@app.route('/status', methods=['GET'])
def get_status():
    cpu_load = psutil.cpu_percent(interval=2)
    
    # Informații memorie
    ram_info = psutil.virtual_memory()
    total_ram = ram_info.total / (1024**2)   # total memorie in MB
    used_ram = ram_info.used / (1024**2)     # memorie folosită in MB
    free_ram = ram_info.available / (1024**2) # memorie disponibilă in MB
    mem_percent = ram_info.percent           # procent utilizare memorie

    data = {
        'cpu_percent': cpu_load,
        'total_ram_mb': total_ram,
        'used_ram_mb': used_ram,
        'free_ram_mb': free_ram,
        'mem_percent': mem_percent
    }
    return jsonify(data), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)