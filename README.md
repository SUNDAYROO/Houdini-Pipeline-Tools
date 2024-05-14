# Houdini Pipeline Tools
## Description
The Houdini Pipeline Tools is a comprehensive system designed to enhance the efficiency of Houdini render farm simulations. The project facilitates seamless communication between servers and clients, enabling efficient job distribution and management. Its primary purpose is to streamline the rendering process in a multi-client, multi-server environment, ensuring optimal performance and resource utilization.

## Features
- Server-Client Communication: Enables communication between servers and clients, allowing clients to send commands.
- Multi-Client, Multi-Server Support: Supports communication between multiple clients and multiple servers simultaneously.
- Automatic Protocol Service Discovery: Automatically detects protocol services.
- Houdini Execution Commands: Sends commands to clients to execute Houdini tasks.
- Render Farm Integration: Connects shots generated in the Simulation tab to the render farm for job distribution.
- Simulation Data Communication: Tests simulation data communication for each client shot operation.
- Job Info Management: Provides job information, including screenshots, job details, and client status.
- Update Interval Adjustment: Allows adjustment of update intervals and connection optimization.
- Job Setting Presets: Creates job setting presets.
- Security: Ensures executable files are not recognized as viruses.
## Installation
Download the CFX-0.3.0-windows-x64-installer.exe from the provided link.

Run the installer and follow the on-screen instructions to complete the installation.

Ensure that the Renderfarm_for_server.exe and Renderfarm_for_client.exe files are correctly placed in the designated directories.

Refer to the ReadMe.txt file for detailed setup and configuration instructions.

## Usage
[Video Guide](https://youtu.be/wmjQcO7WsDw)
Launch the Renderfarm_for_server.exe on the server machine.

Start the Renderfarm_for_client.exe on the client machines.

Use the Houdini_Pipeline.py script to execute and manage Houdini tasks.

Follow the instructions in the ReadMe.txt file to configure and run simulations and rendering jobs.
