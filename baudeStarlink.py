#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import uhd
import numpy as np
import time
import sys

def main():
    # Parameters
    samp_rate = 6.1e6  # Sample rate
    center_freq = 1.5e9  # Center frequency
    output_file = "LNBMeasurements.bin"  # Output file for saving samples
    num_samples = 100000000  # Number of samples to receive
    rx_gain = 10
    # Create USRP device (UHD)
    usrp = uhd.usrp.MultiUSRP()

    # Set parameters on the USRP
    usrp.set_rx_rate(samp_rate, 0)
    usrp.set_rx_freq(uhd.libpyuhd.types.tune_request(center_freq), 0)
    usrp.set_rx_gain(rx_gain, 0)  # Gain setting for the specified channel (0 is default)

    # Set up the stream and receive buffer
    st_args = uhd.usrp.StreamArgs("fc32", "sc16")  # Stream argument for complex 32-bit samples
    st_args.channels = [0]  # Use the first channel
    metadata = uhd.types.RXMetadata()  # Metadata for the received samples
    streamer = usrp.get_rx_stream(st_args)
    recv_buffer = np.zeros((1, 1000), dtype=np.complex64)  # Buffer to hold received samples

    # Open the output file in binary mode
    with open(output_file, 'wb') as f:
        # Start the stream
        stream_cmd = uhd.types.StreamCMD(uhd.types.StreamMode.start_cont)
        stream_cmd.stream_now = True
        streamer.issue_stream_cmd(stream_cmd)

        try:
            # Receive samples in a loop
            samples = np.zeros(num_samples, dtype=np.complex64)
            for i in range(num_samples // 1000):
                # Receive samples into the buffer
                streamer.recv(recv_buffer, metadata)
                samples[i * 1000:(i + 1) * 1000] = recv_buffer[0]
                
                # Write the received samples to the file
                f.write(recv_buffer.tobytes())

                # Print feedback every 1 second
                print(f"Received {i * 1000 + 1000}/{num_samples} samples", end='\r')
                time.sleep(1)  # Sleep for 1 second (you can adjust this as needed)

        except KeyboardInterrupt:
            print("\nStopping...")
            stream_cmd = uhd.types.StreamCMD(uhd.types.StreamMode.stop_cont)
            streamer.issue_stream_cmd(stream_cmd)

if __name__ == "__main__":
    main()

