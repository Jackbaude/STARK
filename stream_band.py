import uhd
import numpy as np
import argparse
import socket
import signal
import sys

"""
USRP Data Streaming Script with LNB LO Adjustment

This script captures samples from a specified Starlink frequency using a USRP device, 
adjusting for the Local Oscillator (LO) of the LNB, and streams the received data to any incoming TCP connection.

Usage:
    python3 script.py --starlink_freq STARLINK_FREQ --lo LO_SELECTION \
                      [--samp_rate SAMPLE_RATE] [--gain GAIN] \
                      [--port PORT]

Arguments:
    --starlink_freq   Starlink frequency in Hz (required)
    --lo             LNB LO selection: A (9.75 GHz) or B (10.6 GHz) (required)
    --samp_rate      Sample rate in Hz (default: 6.1e6)
    --gain           RX gain in dB (default: 0.0)
    --port           Port for TCP streaming (default: 12345)

Dependencies:
    - UHD (USRP Hardware Driver)
    - NumPy
    - Python 3.x
"""

sock = None
conn = None
streamer = None

def signal_handler(sig, frame):
    print("\nShutting down gracefully...")
    if streamer:
        stream_cmd = uhd.types.StreamCMD(uhd.types.StreamMode.stop_cont)
        streamer.issue_stream_cmd(stream_cmd)
    if conn:
        conn.close()
    if sock:
        sock.close()
    sys.exit(0)

def main():
    global sock, conn, streamer
    parser = argparse.ArgumentParser(description="USRP data streaming script with LNB LO adjustment")
    parser.add_argument("--samp_rate", type=float, default=6.1e6, help="Sample rate (Hz)")
    parser.add_argument("--starlink_freq", type=float, required=True, help="Starlink frequency (Hz)")
    parser.add_argument("--lo", type=str, choices=["A", "B"], required=True, help="LNB LO selection: A (9.75 GHz) or B (10.6 GHz)")
    parser.add_argument("--gain", type=float, default=0.0, help="RX gain in dB")
    parser.add_argument("--port", type=int, default=12345, help="Port for TCP streaming")

    args = parser.parse_args()

    lo_freq = 9.75e9 if args.lo == "A" else 10.6e9
    center_freq = args.starlink_freq - lo_freq

    print(f"Using LO: {lo_freq / 1e9} GHz")
    print(f"Tuned Center Frequency: {center_freq / 1e6} MHz")
    print(f"Using RX Gain: {args.gain} dB")
    print(f"Listening on port {args.port} for incoming connections")

    usrp = uhd.usrp.MultiUSRP()
    usrp.set_rx_rate(args.samp_rate, 0)
    usrp.set_rx_freq(uhd.libpyuhd.types.tune_request(center_freq), 0)
    usrp.set_rx_gain(args.gain, 0)
    usrp.set_rx_agc(True, 0)
    usrp.set_rx_antenna('TX/RX', 0)

    st_args = uhd.usrp.StreamArgs("fc32", "sc16")
    st_args.channels = [0]
    metadata = uhd.types.RXMetadata()
    streamer = usrp.get_rx_stream(st_args)
    recv_buffer = np.zeros((1, 1000), dtype=np.complex64)

    # Create TCP server socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(("0.0.0.0", args.port))
    sock.listen(1)

    print("Waiting for incoming TCP connections...")

    # Accept the incoming connection
    conn, addr = sock.accept()
    print(f"Accepted connection from {addr}")

    stream_cmd = uhd.types.StreamCMD(uhd.types.StreamMode.start_cont)
    stream_cmd.stream_now = True
    streamer.issue_stream_cmd(stream_cmd)

    # Register signal handler
    signal.signal(signal.SIGINT, signal_handler)

    try:
        while True:
            streamer.recv(recv_buffer, metadata)
            conn.sendall(recv_buffer.tobytes())
            print("Streaming samples...", end='\r')
    except KeyboardInterrupt:
        signal_handler(None, None)

if __name__ == "__main__":
    main()

