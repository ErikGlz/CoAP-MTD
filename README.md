# CoAP-MTD

## Overview  
This project explores security in **Internet of Things (IoT)** systems by implementing a **Moving Target Defense (MTD)** technique. The approach involves continuously reconfiguring the **CoAP (Constrained Application Protocol)** communication to mitigate **spoofing attacks** and other network threats.  

By randomizing CoAP protocol dialects and integrating machine learning-based decision-making, the system enhances resilience and adaptability against cyber threats in IoT environments.  

## Features  
- **CoAP Protocol Dialect Randomization** – Implemented using the `aiocoap` Python library.  
- **Dynamic Reconfiguration** – The system continuously modifies CoAP communications to increase security.  
- **Machine Learning Integration** – Uses a **decision tree algorithm** from `scikit-learn` to analyze and adapt security measures.  
- **IoT System Implementation** – Built with a **Raspberry Pi 4** as a sensor node and a **Linux client** for communication.  
- **Attack Simulation** – Uses **Scapy** to generate and test spoofing and network-based attacks.  

## Technologies Used  
- **Python** (Core language)  
- **aiocoap** (CoAP protocol implementation)  
- **scikit-learn** (Decision tree algorithm)  
- **Scapy** (Network attack simulation)  
- **Raspberry Pi 4** (IoT sensor node)  
- **Linux** (Client system)

## Future Work
- Enhancing the adaptability of the MTD technique.
- Expanding machine learning models for better threat detection.
- Testing with additional IoT devices and protocols.
