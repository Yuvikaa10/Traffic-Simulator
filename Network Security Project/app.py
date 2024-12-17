from flask import Flask, render_template, request, jsonify
import matplotlib.pyplot as plt
import io
import base64
import random
import time

app = Flask(__name__)

# Simulate traffic (dummy data)
def simulate_traffic(traffic_type, duration):
    # Simulate traffic types
    traffic_data = {
        "HTTP": [random.randint(50, 150) for _ in range(duration)],
        "FTP": [random.randint(30, 100) for _ in range(duration)],
        "ICMP": [random.randint(10, 50) for _ in range(duration)],
    }
    
    # Get traffic data for the selected type
    data = traffic_data.get(traffic_type, [0] * duration)
    
    # Simulate traffic by waiting for the duration (optional, to simulate longer processing)
    time.sleep(2)
    
    return data

# Traffic details (brief descriptions)
traffic_details = {
    "HTTP": "HTTP traffic represents the data exchange for web pages. Higher values indicate heavier browsing activity or server load.",
    "FTP": "FTP traffic involves file transfer over the network. It can vary depending on the size of files being uploaded or downloaded.",
    "ICMP": "ICMP traffic includes ping requests and responses, commonly used for network diagnostics. It is typically lightweight and short-lived."
}

# Generate the graph
def generate_graph(traffic_types, duration):
    graphs = {}
    
    for traffic_type in traffic_types:
        data = simulate_traffic(traffic_type, duration)
        
        # Create a plot
        fig, ax = plt.subplots()
        ax.plot(range(1, duration + 1), data, label=f"Traffic Type: {traffic_type}")
        
        ax.set(xlabel="Time (seconds)", ylabel="Traffic Rate (requests/sec)", title=f"Traffic Simulation ({traffic_type})")
        ax.grid(True)
        ax.legend()
        
        # Convert plot to PNG image
        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        img_data = base64.b64encode(img.getvalue()).decode('utf-8')
        plt.close(fig)
        
        # Store the generated image data for the graph
        graphs[traffic_type] = img_data
    
    return graphs

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/simulate', methods=['POST'])
def simulate():
    traffic_types = request.form.getlist('traffic_type')  # List of selected traffic types
    duration = int(request.form['duration'])
    
    graphs = generate_graph(traffic_types, duration)
    
    # Generate traffic details for the selected types
    details = {traffic_type: traffic_details.get(traffic_type, "No description available") for traffic_type in traffic_types}
    
    return render_template('index.html', graphs=graphs, traffic_types=traffic_types, duration=duration, details=details)

if __name__ == '__main__':
    app.run(debug=True)
