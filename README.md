<h3>This project was designed for the purpose of monitoring my private 1.21.10 Minecraft server using RCON to send commands and receive data virtually.
</br></br>Included is the use of ntfy.sh, a free, public, and open-source project for sending notifications via REST actions.
</h3>
<h4>
If personally using, please copy the config.tpl file to a config.json and update the parameters with your information.
</h4>
<ul>
<li>host = server.properties:server-ip</li>
<li>port = server.properties:rcon.port</li>
<li>password = server.properties:rcon.password</li>
<li>topic = ntfy.sh topic</li>
<li>data_dir = directory to hold snapshot and player data</li>
<li>snapshot_file = filename of snapshot file</li>
<li>status_file = filename of player status file</li>
</ul>
