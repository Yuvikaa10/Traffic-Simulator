import matplotlib.pyplot as plt
from scapy.all import IP, TCP, ICMP, UDP, send
import time
import random

# Simulate traffic for a specific type with size variations
def simulate_traffic(traffic_type, target_ip, packet_count):
    traffic_data = []
    for _ in range(packet_count):
        timestamp = time.time()
        if traffic_type == "TCP":
            pkt = IP(dst=target_ip) / TCP()
            size = random.randint(100, 1500)  # TCP size variations
        elif traffic_type == "ICMP":
            pkt = IP(dst=target_ip) / ICMP()
            size = random.randint(64, 256)  # ICMP size variations
        elif traffic_type == "UDP":
            pkt = IP(dst=target_ip) / UDP()
            size = random.randint(128, 1024)  # UDP size variations
        else:
            raise ValueError("Invalid traffic type")

        send(pkt, verbose=False)
        traffic_data.append((timestamp, size))
        time.sleep(random.uniform(0.1, 0.3))  # Simulate realistic delays
    return traffic_data

def main():
    print("Choose traffic types (comma-separated):")
    print("1. TCP")
    print("2. ICMP")
    print("3. UDP")
    choices = input("Enter your choices (e.g., 1,2 for TCP and ICMP): ").strip()
    selected_types = [type_map.get(choice) for choice in choices.split(",")]
    
    if not all(selected_types):
        print("Invalid choice(s). Please try again.")
        return

    target_ip = input("Enter the target IP address: ").strip()
    packet_count = int(input("Enter the number of packets to simulate per type: ").strip())

    print(f"Simulating traffic for {', '.join(selected_types)} to {target_ip}...")
    
    all_traffic_data = {}
    for traffic_type in selected_types:
        all_traffic_data[traffic_type] = simulate_traffic(traffic_type, target_ip, packet_count)

    # Plotting
    plt.figure(figsize=(12, 8))
    for traffic_type, data in all_traffic_data.items():
        times = [d[0] - data[0][0] for d in data]  # Relative time
        sizes = [d[1] for d in data]
        plt.plot(times, sizes, label=f"{traffic_type} Traffic", marker="o", linestyle="-")

    # Add Graph Details
    plt.title("Simulated Network Traffic: Packet Sizes Over Time", fontsize=14)
    plt.xlabel("Time (seconds)", fontsize=12)
    plt.ylabel("Packet Size (bytes)", fontsize=12)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# Map user input to traffic types
type_map = {"1": "TCP", "2": "ICMP", "3": "UDP"}

if __name__ == "__main__":
    main()
