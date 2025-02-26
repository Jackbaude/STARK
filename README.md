# STARK  
**Starlink Testing of Application and Radio Ku-band**

## Hardware Setup

Ensure the following hardware components are set up properly:

- **Starlink Dish** and **Router** (for satellite communication)
- **10.7-12.7 GHz LNB** (Low-Noise Block converter)
- **Parabolic Dish** (for signal focusing)
- **Two 50V Bias Tees** (to power the LNB and SDR)
- **Power Supply** for Bias Tees
- **Software Defined Radio** (e.g., USRP B210)
- **Mini Computer** (for processing and analysis)

## Prerequisites and Dependencies

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

## Purpose

The purpose of **STARK** is to conduct integrated testing and analysis of Starlink communications using both physical-layer (Ku-band radio) measurements and application-layer network performance. Specifically, **STARK** aims to evaluate:

- **Ku-band radio signal quality** (PHY layer)
- **gRPC communication performance**
- **Network throughput** using iPerf

These measurements help to assess Starlink's performance in real-world conditions, contributing to the optimization of next-gen satellite communication systems.

## Getting Started

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
3. **Ensure all hardware is properly connected**:
   - Connect the Starlink dish and router.
   - Set up your LNB, SDR, and mini computer.

4. **Run the testing and measurement scripts** for Ku-band signal analysis and network performance.

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
