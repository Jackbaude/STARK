import uhd
import numpy as np
import time
import argparse
from datetime import datetime

def calculate_signal_strength(samples):
    """
    Calculate the signal strength in dB from the received samples.
    """
    power = np.mean(np.abs(samples) ** 2)
    return 10 * np.log10(power) if power > 0 else -np.inf

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Capture a clip of data for a single band")
    parser.add_argument("--starlink_freq", type=float, default=11.325e9, help="Starlink frequency (Hz)")
    parser.add_argument("--lo", type=str, choices=["A", "B"], default="A", help="LNB LO selection: A (9.75 GHz) or B (10.6 GHz)")
    parser.add_argument("--samp_rate", type=float, default=1e6, help="Sample rate (Hz)")
    parser.add_argument("--gain", type=float, default=30.0, help="RX gain in dB")
    parser.add_argument("--duration", type=float, default=30.0, help="Capture duration in seconds")
    args = parser.parse_args()

    # Determine LO frequency
    lo_freq = 9.75e9 if args.lo == "A" else 10.6e9

    # Calculate the center frequency
    center_freq = args.starlink_freq - lo_freq
    print(f"Starlink Frequency: {args.starlink_freq / 1e9} GHz")
    print(f"Using LO: {lo_freq / 1e9} GHz")
    print(f"Tuned Center Frequency: {center_freq / 1e6} MHz")
    print(f"Using RX Gain: {args.gain} dB")
    print(f"Using Sample Rate: {args.samp_rate / 1e6} MHz")
    print(f"Capture Duration: {args.duration} seconds")

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

    # Calculate the number of samples to capture
    num_samples = int(args.samp_rate * args.duration)
    print(f"Capturing {num_samples} samples...")

    # Generate output filename with metadata
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f"starlink_{args.starlink_freq / 1e9}GHz_lo{args.lo}_gain{args.gain}dB_{args.duration}s_{timestamp}.bin"
    print(f"Output file: {output_file}")

    # Open the output file in binary mode
    with open(output_file, 'wb') as f:
        # Start the stream
        stream_cmd = uhd.types.StreamCMD(uhd.types.StreamMode.start_cont)
        stream_cmd.stream_now = True
        streamer.issue_stream_cmd(stream_cmd)

        try:
            samples_collected = 0
            while samples_collected < num_samples:
                # Receive samples
                streamer.recv(recv_buffer, metadata)
                samples_to_write = min(recv_buffer.size, num_samples - samples_collected)
                f.write(recv_buffer[0][:samples_to_write].tobytes())
                samples_collected += samples_to_write
                print(f"Captured {samples_collected}/{num_samples} samples", end='\r')
        
        except KeyboardInterrupt:
            print("\nCapture interrupted by user.")
        
        finally:
            # Stop the stream
            stream_cmd = uhd.types.StreamCMD(uhd.types.StreamMode.stop_cont)
            streamer.issue_stream_cmd(stream_cmd)
            print("\nCapture complete. Data saved to:", output_file)

if __name__ == "__main__":
    main()
