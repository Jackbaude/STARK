import uhd
import numpy as np
import time
import argparse

"""
USRP Data Capture Script with LNB LO Adjustment

This script captures samples from a specified Starlink frequency using a USRP device, 
adjusting for the Local Oscillator (LO) of the LNB, and saves the received data to a binary file.

Usage:
    python3 script.py --starlink_freq STARLINK_FREQ --lo LO_SELECTION \
                      [--samp_rate SAMPLE_RATE] [--gain GAIN] [--output_file OUTPUT_FILE] \
                      [--num_samples NUM_SAMPLES]

Arguments:
    --starlink_freq   Starlink frequency in Hz (required)
    --lo             LNB LO selection: A (9.75 GHz) or B (10.6 GHz) (required)
    --samp_rate      Sample rate in Hz (default: 6.1e6)
    --gain           RX gain in dB (default: 0.0)
    --output_file    File path for saving samples (default: data/LNBMeasurements.bin)
    --num_samples    Number of samples to capture (default: 10000)

Example:
    python3 script.py --starlink_freq 11.325e9 --lo A --samp_rate 10e6 --gain 30 --output_file data/output.bin --num_samples 20000

Dependencies:
    - UHD (USRP Hardware Driver)
    - NumPy
    - Python 3.x
"""

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="USRP data capture script with LNB LO adjustment")
    parser.add_argument("--samp_rate", type=float, default=5.7e6, help="Sample rate (Hz)")
    parser.add_argument("--starlink_freq", type=float, required=True, help="Starlink frequency (Hz)")
    parser.add_argument("--lo", type=str, choices=["A", "B"], required=True, help="LNB LO selection: A (9.75 GHz) or B (10.6 GHz)")
    parser.add_argument("--gain", type=float, default=0.0, help="RX gain in dB")
    parser.add_argument("--output_file", type=str, default="data/LNBMeasurements.bin", help="Output file for saving samples")
    parser.add_argument("--num_samples", type=int, default=10000, help="Number of samples to receive")

    args = parser.parse_args()

    # Determine LO frequency
    lo_freq = 9.75e9 if args.lo == "A" else 10.6e9

    # Calculate the center frequency
    center_freq = args.starlink_freq - lo_freq
    print(f"Using LO: {lo_freq / 1e9} GHz")
    print(f"Tuned Center Frequency: {center_freq / 1e6} MHz")
    print(f"Using RX Gain: {args.gain} dB")

    # Create USRP device (UHD)
    usrp = uhd.usrp.MultiUSRP()

    # Set parameters on the USRP
    usrp.set_rx_rate(args.samp_rate, 0)
    usrp.set_rx_freq(uhd.libpyuhd.types.tune_request(center_freq), 0)
    usrp.set_rx_gain(args.gain, 0)
    usrp.set_rx_agc(True, 0)
    usrp.set_rx_antenna('TX/RX', 0)

    # Set up the stream and receive buffer
    st_args = uhd.usrp.StreamArgs("fc32", "sc16")
    st_args.channels = [0]
    metadata = uhd.types.RXMetadata()
    streamer = usrp.get_rx_stream(st_args)
    recv_buffer = np.zeros((1, 1000), dtype=np.complex64)

    # Open the output file in binary mode
    with open(args.output_file, 'wb') as f:
        # Start the stream
        stream_cmd = uhd.types.StreamCMD(uhd.types.StreamMode.start_cont)
        stream_cmd.stream_now = True
        streamer.issue_stream_cmd(stream_cmd)

        try:
            samples = np.zeros(args.num_samples, dtype=np.complex64)
            for i in range(args.num_samples // 1000):
                streamer.recv(recv_buffer, metadata)
                samples[i * 1000:(i + 1) * 1000] = recv_buffer[0]
                f.write(recv_buffer.tobytes())
                print(f"Received {i * 1000 + 1000}/{args.num_samples} samples", end='\r')
        
        except KeyboardInterrupt:
            print("\nStopping...")
            stream_cmd = uhd.types.StreamCMD(uhd.types.StreamMode.stop_cont)
            streamer.issue_stream_cmd(stream_cmd)

if __name__ == "__main__":
    main()
