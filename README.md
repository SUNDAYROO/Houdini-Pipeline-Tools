#  Houdini Pipeline Tools
![alt text](https://github.com/SUNDAYROO/Houdini-Pipeline-Tools/blob/main/icons/logo_CFX_Pipeline_icon_64.png)
## Description
The Houdini Pipeline Tools is a comprehensive system designed to enhance the efficiency of Houdini render farm simulations. The project facilitates seamless communication between servers and clients, enabling efficient job distribution and management. Its primary purpose is to streamline the rendering process in a multi-client, multi-server environment, ensuring optimal performance and resource utilization.

## Features
- **Server-Client Communication**: Enables communication between servers and clients, allowing clients to send commands.
- **Multi-Client, Multi-Server Support**: Supports communication between multiple clients and multiple servers simultaneously.
- **Automatic Protocol Service Discovery**: Automatically detects protocol services.
- **Houdini Execution Commands**: Sends commands to clients to execute Houdini tasks.
- **Render Farm Integration**: Connects shots generated in the Simulation tab to the render farm for job distribution.
- **Simulation Data Communication**: Tests simulation data communication for each client shot operation.
- **Job Info Management**: Provides job information, including screenshots, job details, and client status.
- **Update Interval Adjustment**: Allows adjustment of update intervals and connection optimization.
- **Job Setting Presets**: Creates job setting presets.
- **Security**: Ensures executable files are not recognized as viruses.

## Installation
1. Download the `CFX-0.3.0-windows-x64-installer.exe` from the provided [link](https://drive.google.com/file/d/1y1QsCIUnAiqGioF4b7N3lXAXcjLEskfL/view?usp=sharing).
2. Run the installer and follow the on-screen instructions to complete the installation.
3. Ensure that the `Renderfarm_for_server.exe` and `Renderfarm_for_client.exe` files are correctly placed in their designated directories.
4. Refer to the `ReadMe.txt` file for detailed setup and configuration instructions.

## Usage
1. **Video Guide**: For a visual walkthrough of the setup and usage, refer to our [Video Guide 1 - Tool](https://youtu.be/wmjQcO7WsDw) and [Video Guide 2 - Renderfarm](https://youtu.be/_CYaxjTqDk0).
2. **Server Setup**:
   - Launch the `Renderfarm_for_server.exe` on the server machine. This will initiate the server-side application and prepare it to handle client requests.
3. **Client Setup**:
   - Start the `Renderfarm_for_client.exe` on the client machines. This will connect the clients to the server, allowing them to send and receive commands.
4. **Managing Tasks**:
   - Use the `Houdini_Pipeline.py` script to execute and manage Houdini tasks. This script serves as the main interface for managing simulations and render jobs.
5. **Configuration**:
   - Follow the instructions in the `ReadMe.txt` file to configure the system and run simulations and rendering jobs. This file provides detailed guidance on setting up the environment, configuring clients and servers, and optimizing performance.

By following these steps, you can leverage the full capabilities of the Houdini Pipeline Tools to enhance your render farm operations and achieve efficient, high-quality rendering results.
