# STARK  
**Starlink Testing of Application and Radio Ku-band**

## Purpose

The purpose of **STARK** is to conduct integrated testing and analysis of Starlink communications using both physical-layer (Ku-band radio) measurements and application-layer network performance. Specifically, **STARK** aims to evaluate:

- **Ku-band radio signal quality** (PHY layer)
- **gRPC communication performance**
- **Network throughput** using iPerf

These measurements help to assess Starlink's performance in real-world conditions, contributing to the optimization of next-gen satellite communication systems.

## Hardware Setup

Ensure the following hardware components are set up properly:

- **Starlink Dish** and **Router** (for satellite communication)
- **10.7-12.7 GHz LNB** (Low-Noise Block converter)
- **Parabolic Dish** (for signal focusing)
- **Two 50V Bias Tees** (to power the LNB and SDR)
- **Power Supply** for Bias Tees
- **Software Defined Radio** (e.g., USRP B210)
- **Mini Computer** (for processing and analysis)

## Dependencies

Before using **STARK**, make sure the following software and dependencies are installed:

- **Python 3.x** (for running scripts and services)
- **UHD** (Universal Hardware Driver for USRP SDRs)  
  - Installation guide: [UHD Build Guide](https://files.ettus.com/manual/page_build_guide.html)  
  - [Python API for UHD](https://pysdr.org/content/usrp.html)
- **Docker and Docker-Compose** (if using containerized services like Starlink-mon)  
  - [Docker Installation Guide](https://docs.docker.com/get-docker/)
  - [Docker-Compose Installation](https://docs.docker.com/compose/install/)
  - Starlink-mon: [GitHub Repository](https://github.com/rzzldzzl/starlink-mon)
- **iPerf** (for network performance testing)  
  - [iPerf Installation](https://iperf.fr/)

Ensure your **Starlink dish** is set up correctly, and you have access to the necessary networking hardware such as routers and SDRs.


## Application tests

### Perform Starlink GRPC measurments 

1. **Clone the repository:**

   ```bash
   git clone https://github.com/jackbaude/stark.git
   cd stark
   ```

2. **Build and run containerized services** (e.g., Starlink-mon):   

    Clone Repo  

    ```git clone https://github.com/rzzldzzl/starlink-mon.git```

    Run Docker compose

    ```docker-compose -f starlink-mon/docker-compose.yaml up -d```

### Generate traffic to starlink dish via iperf

#### Quick Iperf

This will connect to the aws instance, and starlink instance, and start iperf using *tmux*

```
chmod +x tmux_iperf.sh
./tmux_iperf.sh
```

#### Manually run Iperf

If you would like to run these manually

From the **AWS** server
```
iperf3 -s -p 8211
```

From the starlink measurment machine

```
iperf3 -c AWS_PUBLIC_IP -p 8211 -R -u -b 50M -l 1400 -P 4 -t 600 
```
* `-p` port 8211
* `-R` reverse
* `-u` UDP instead of TCP
* `-b` bandwith of 50Mbs
* `-l` use 1400 byte packets
* `-t` run for 10 minutes

#### traceroute from inside out, and from outside in

## Radio Ku-band
LNB 

10.7-12.7Ghz

L.0. (local oscialtor) 9.75-10.6Ghz

Noise Floor 0.1 dB

Low Band – Horizontal Polarization

High Band – Horizontal Polarization

Low Band – Vertical Polarization

High Band – Vertical Polarization

> It is not able to downconvert all of these simultaneously – it needs to be sent commands from the satellite receiver that switch the output to the desired band/polarization. The satellite receiver switches to receive either High or Low Band with a 22Hz tone and either Horizontal or Vertical Polarization with a switching voltage between 12.5v – 18v. These tones and voltages are sent up the coaxial cable from the back of the receiver to the output of the LNB.


For starlink we need to measure the low band. 

**Capture Single Band**

```
python3 capture_single_band.py --samp_rate 6.1e6 --center_freq 1.5e9 --output_file data/measurements.bin --num_samples 10000
```

**Capture Multi Band**

```
python3 capture_multi_band.py --samp_rate 6.1e6 --output_file data/starlink.bin --num_samples 20000 --dwell_time 0.5 
```

## Parameters for Ku-band Signal and Testing

| Parameter | Value   | Units | Description                                                                 |
|-----------|---------|-------|-----------------------------------------------------------------------------|
| **Fs**        | 240     | MHz   | Channel bandwidth; information symbol rate                                  |
| **N**         | 1024    | -     | Number of subcarriers in bandwidth Fs                                       |
| **Ng**        | 32      | -     | Number of intervals 1/Fs in an OFDM symbol guard interval                    |
| **Tf**        | 1/750   | s     | Frame period                                                                |
| **Tfg**       | 68/15 ≈ 4.533 | µs | Frame guard interval                                                         |
| **Nsf**       | 302     | -     | Number of non-zero symbols in a frame                                       |
| **Nsfd**      | 298     | -     | Number of data (non-synchronization) symbols in a frame                     |
| **T**         | 64/15 ≈ 4.266 | µs | Useful (non-cyclic) OFDM symbol interval (T = N/F)                          |
| **Tg**        | 2/15 ≈ 0.133  | µs | Symbol guard interval (Tg = Ng/F)                                           |
| **Tsym**      | 4.4     | µs    | OFDM symbol duration including guard interval (Tsym = T + Tg)               |
| **F**         | 234375  | Hz    | Subcarrier spacing (F = F/N)                                                |
| **Fci**       | 10.7 + F/2 + 0.25(i - 1/2) | GHz | Center frequency of ith channel                                           |
| **Fδ**        | 250     | MHz   | Channel spacing (Fδ = Fci - Fc(i-1))                                        |
| **Fg**        | 10      | MHz   | Width of guard band between channels (Fg = Fs - Fδ)                         |

These parameters represent the settings used for the Ku-band signal analysis and help to define the characteristics of the radio communication system being tested.

## Authors
- Jack Baude <baude022@umn.edu>

## License
This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.
```
