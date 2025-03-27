import uhd
import numpy as np
import time
import argparse

def calculate_signal_strength(samples):
    """
    Calculate the signal strength in dB from the received samples.
    """
    power = np.mean(np.abs(samples) ** 2)
    return 10 * np.log10(power) if power > 0 else -np.inf

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Monitor Starlink channel signal strength")
    parser.add_argument("--starlink_freq", type=float, required=True, help="Starlink frequency (Hz)")
    parser.add_argument("--lo", type=str, choices=["A", "B"], required=True, help="LNB LO selection: A (9.75 GHz) or B (10.6 GHz)")
    parser.add_argument("--samp_rate", type=float, default=6.1e6, help="Sample rate (Hz)")
    parser.add_argument("--gain", type=float, default=0.0, help="RX gain in dB")
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

    # Start the stream
    stream_cmd = uhd.types.StreamCMD(uhd.types.StreamMode.start_cont)
    stream_cmd.stream_now = True
    streamer.issue_stream_cmd(stream_cmd)

    try:
        print("Monitoring signal strength. Press Ctrl+C to stop...")
        while True:
            # Receive samples
            streamer.recv(recv_buffer, metadata)
            
            # Calculate and print signal strength
            signal_strength = calculate_signal_strength(recv_buffer[0])
            print(f"Signal Strength: {signal_strength:.2f} dB", end='\r')
            
    except KeyboardInterrupt:
        print("\nStopping...")
        stream_cmd = uhd.types.StreamCMD(uhd.types.StreamMode.stop_cont)
        streamer.issue_stream_cmd(stream_cmd)

if __name__ == "__main__":
    main()
