This project was designed for the purpose of monitoring my private 1.21.10 Minecraft server using RCON to send commands and receive data virtually.
Included is the use of ntfy.sh, a free, public, and open-source project for sending notifications via REST actions.

If personally using, please copy the config.tpl file to a config.json and update the parameters with your information.
host = server.properties:server-ip
port = server.properties:rcon.port
password = server.properties:rcon.password
topic = ntfy.sh topic
data_dir = directory to hold snapshot and player data
snapshot_file = filename of snapshot file
status_file = filename of player status file
