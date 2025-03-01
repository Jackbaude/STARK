#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
USRP Data Capture Script for Starlink Frequency Bands

This script captures samples from multiple frequency bands used by Starlink, 
cycling through center frequencies from 10.7 GHz to 12.7 GHz in 125 MHz steps. 
Each frequency is sampled for a configurable amount of time before switching.

Usage:
    python3 script.py [--samp_rate SAMPLE_RATE] [--output_file OUTPUT_FILE] \
                      [--num_samples NUM_SAMPLES] [--dwell_time DWELL_TIME]

Arguments:
    --samp_rate      Sample rate in Hz (default: 6.1e6)
    --output_file    File path for saving samples (default: data/LNBMeasurements.bin)
    --num_samples    Number of samples to capture per frequency (default: 10000)
    --dwell_time     Time in seconds to dwell on each frequency (default: 0.5)

Example:
    python3 script.py --samp_rate 10e6 --output_file data/starlink.bin --num_samples 20000 --dwell_time 1.0

Dependencies:
    - UHD (USRP Hardware Driver)
    - NumPy
    - Python 3.x

"""

import uhd
import numpy as np
import time
import argparse

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="USRP data capture script")
    parser.add_argument("--samp_rate", type=float, default=6.1e6, help="Sample rate (Hz)")
    parser.add_argument("--output_file", type=str, default="data/LNBMeasurements.bin", help="Output file for saving samples")
    parser.add_argument("--num_samples", type=int, default=10000, help="Number of samples to receive per frequency")
    parser.add_argument("--dwell_time", type=float, default=0.5, help="Time to dwell on each frequency (seconds)")
    args = parser.parse_args()

    # Define Starlink frequency range (10.7 GHz to 12.7 GHz in 125 MHz steps)
    center_freqs = np.arange(10.7e9, 12.7e9 + 125e6, 125e6)

    # Create USRP device (UHD)
    usrp = uhd.usrp.MultiUSRP()
    usrp.set_rx_rate(args.samp_rate, 0)
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
        try:
            for freq in center_freqs:
                print(f"Tuning to {freq / 1e9} GHz")
                usrp.set_rx_freq(uhd.libpyuhd.types.tune_request(freq), 0)
                
                # Start the stream
                stream_cmd = uhd.types.StreamCMD(uhd.types.StreamMode.start_cont)
                stream_cmd.stream_now = True
                streamer.issue_stream_cmd(stream_cmd)
                
                samples = np.zeros(args.num_samples, dtype=np.complex64)
                for i in range(args.num_samples // 1000):
                    streamer.recv(recv_buffer, metadata)
                    samples[i * 1000:(i + 1) * 1000] = recv_buffer[0]
                    f.write(recv_buffer.tobytes())
                    print(f"Received {i * 1000 + 1000}/{args.num_samples} samples at {freq / 1e9} GHz", end='\r')
                
                time.sleep(args.dwell_time)  # Dwell time on each frequency
                
                # Stop the stream before changing frequency
                stream_cmd = uhd.types.StreamCMD(uhd.types.StreamMode.stop_cont)
                streamer.issue_stream_cmd(stream_cmd)
        
        except KeyboardInterrupt:
            print("\nStopping...")
            stream_cmd = uhd.types.StreamCMD(uhd.types.StreamMode.stop_cont)
            streamer.issue_stream_cmd(stream_cmd)

if __name__ == "__main__":
    main()
