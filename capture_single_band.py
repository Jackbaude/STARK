#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import uhd
import numpy as np
import time
import argparse

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="USRP data capture script")
    parser.add_argument("--samp_rate", type=float, default=6.1e6, help="Sample rate (Hz)")
    parser.add_argument("--center_freq", type=float, default=1.5e9, help="Center frequency (Hz)")
    parser.add_argument("--output_file", type=str, default="data/LNBMeasurements.bin", help="Output file for saving samples")
    parser.add_argument("--num_samples", type=int, default=10000, help="Number of samples to receive")
    args = parser.parse_args()

    # Create USRP device (UHD)
    usrp = uhd.usrp.MultiUSRP()

    # Set parameters on the USRP
    usrp.set_rx_rate(args.samp_rate, 0)
    usrp.set_rx_freq(uhd.libpyuhd.types.tune_request(args.center_freq), 0)

    # Automatic gain control
    usrp.set_rx_agc(True, 0)  # 0 for channel 0, i.e., the first channel of the USRP
    usrp.set_rx_antenna('TX/RX', 0)

    # Set up the stream and receive buffer
    st_args = uhd.usrp.StreamArgs("fc32", "sc16")  # Stream argument for complex 32-bit samples
    st_args.channels = [0]  # Use the first channel
    metadata = uhd.types.RXMetadata()  # Metadata for the received samples
    streamer = usrp.get_rx_stream(st_args)
    recv_buffer = np.zeros((1, 1000), dtype=np.complex64)  # Buffer to hold received samples

    # Open the output file in binary mode
    with open(args.output_file, 'wb') as f:
        # Start the stream
        stream_cmd = uhd.types.StreamCMD(uhd.types.StreamMode.start_cont)
        stream_cmd.stream_now = True
        streamer.issue_stream_cmd(stream_cmd)

        try:
            # Receive samples in a loop
            samples = np.zeros(args.num_samples, dtype=np.complex64)
            for i in range(args.num_samples // 1000):
                # Receive samples into the buffer
                streamer.recv(recv_buffer, metadata)
                samples[i * 1000:(i + 1) * 1000] = recv_buffer[0]
                
                # Write the received samples to the file
                f.write(recv_buffer.tobytes())

                # Print feedback every 1 second
                print(f"Received {i * 1000 + 1000}/{args.num_samples} samples", end='\r')

        except KeyboardInterrupt:
            print("\nStopping...")
            stream_cmd = uhd.types.StreamCMD(uhd.types.StreamMode.stop_cont)
            streamer.issue_stream_cmd(stream_cmd)

if __name__ == "__main__":
    main()
