##### Synopsis
aGalaxy is a central management system for daily DDoS mitigation operations. It is used to manage TPS devices and streamline all DDoS related functions.
This code is developed to automate DDoS incident management based on BGP route announcements.
In short, it listens BGP updates and automatically creates & stops incidents for DDoS protected objects in aGalaxy.
Details
The code performs the following:
- It uses ExaBGP to establish neighborship with the flow analysis tools
- ExaBGP listens for route updates (advertisement or withdrawal)
- If a route matches a destination entry protected object in aGalaxy, an incident is created (if none exists) with the corresponding mitigation template
- If a route is withdrawn, related incident is stopped
- Appropriate logs are generated inside syslog file

ExaBGP version: 3.4.16-1
aGalaxy version: 3.0.2
TPS version: 3.1.3

##### Motivation
This project is done in order to ease security administrators’ daily life. When a DDoS event occurs, it is reflected to aGalaxy as an incident automatically. So it saves time and human dependency.

##### Installation
ExaBGP needs to be installed. Current code is compatible with 3.4.16-1 version. An example for ExaBGP is given inside the code directory. ExaBGP can peer with multiple neighbors but next-hop of the update messages is important. It should match the “bgp_next_hop” variable inside the code.
parse_routes_v4.py is triggered by ExaBGP when there is an update. This is the main section of the code.
a10_api_calls.py handles all aGalaxy API (aGAPI) calls.
a10_functions.py handles all manipulation, filtering and other stuff related with API outputs & inputs.

##### Tests
Tests can be done by peering ExaBGP with a neighbor and announcing routes that matches or contains destination entry objects.

