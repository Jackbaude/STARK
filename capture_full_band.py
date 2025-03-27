#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import uhd
import numpy as np
import time
import argparse

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="USRP satellite downlink capture script")
    parser.add_argument("--samp_rate", type=float, default=56e6, help="Sample rate (Hz)")
    parser.add_argument("--output_file", type=str, default="data/SatelliteDownlinkCapture.bin", help="Output file for saving samples")
    parser.add_argument("--num_samples", type=int, default=10000, help="Number of samples to receive per segment")
    parser.add_argument("--gain", type=float, default=40.0, help="RX gain (dB)")
    args = parser.parse_args()

    # List of observed downlink frequencies (MHz -> Hz)
    downlink_freqs = [11075e6, 11325e6, 11575e6]  # Known active channels
    # additional_channels = [11825e6, 12075e6, 12325e6, 12575e6]  # Hypothetical upper channels
    downlink_freqs.extend(additional_channels)  # Add them if exploration is desired

    # Define segmentation parameters (250 MHz captured in ~50 MHz chunks)
    segment_bw = 50e6  # 50 MHz per segment to fit within USRP B210 capabilities
    step_size = segment_bw - 5e6  # Overlapping segments to avoid data loss
    num_segments = int(250e6 // step_size)  # Number of segments per 250 MHz channel

    # Create USRP device (UHD)
    usrp = uhd.usrp.MultiUSRP()
    usrp.set_rx_rate(args.samp_rate, 0)
    usrp.set_rx_antenna('TX/RX', 0)

    # Set up the stream and receive buffer
    st_args = uhd.usrp.StreamArgs("fc32", "sc16")
    st_args.channels = [0]
    metadata = uhd.types.RXMetadata()
    streamer = usrp.get_rx_stream(st_args)
    recv_buffer = np.zeros((1, 1000), dtype=np.complex64)

    # Open the output file in binary mode
    with open(args.output_file, 'wb') as f:
        for center_freq in downlink_freqs:
            print(f"Capturing full 250 MHz around {center_freq / 1e6:.2f} MHz")
            
            for i in range(num_segments):
                segment_freq = center_freq - 125e6 + i * step_size
                print(f"  Tuning to {segment_freq / 1e6:.2f} MHz")
                usrp.set_rx_freq(uhd.libpyuhd.types.tune_request(segment_freq), 0)
                time.sleep(0.1)  # Allow tuning to stabilize

                # Start the stream
                stream_cmd = uhd.types.StreamCMD(uhd.types.StreamMode.start_cont)
                stream_cmd.stream_now = True
                streamer.issue_stream_cmd(stream_cmd)

                try:
                    samples = np.zeros(args.num_samples, dtype=np.complex64)
                    for j in range(args.num_samples // 1000):
                        streamer.recv(recv_buffer, metadata)
                        samples[j * 1000:(j + 1) * 1000] = recv_buffer[0]
                        f.write(recv_buffer.tobytes())
                    print(f"    Captured {args.num_samples} samples at {segment_freq / 1e6:.2f} MHz", end='\r')
                except KeyboardInterrupt:
                    print("\nStopping...")
                    break

                # Stop stream before tuning to next frequency
                stream_cmd = uhd.types.StreamCMD(uhd.types.StreamMode.stop_cont)
                streamer.issue_stream_cmd(stream_cmd)

if __name__ == "__main__":
    main()
