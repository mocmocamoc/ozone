from flask import Flask, render_template
import lightning
import os
from collections import defaultdict

sockPath = os.path.join(os.environ["HOME"], ".lightning", "lightning-rpc")
l = lightning.LightningRpc(sockPath)

app = Flask(__name__)

@app.route("/")
def channels():
    peers = l.listpeers()["peers"]
    channels = defaultdict(list)
    nodes = l.listnodes()["nodes"]
    for peer in peers:
        aliases = [n["alias"] for n in nodes if n["nodeid"] == peer["id"]]
        alias = aliases[0] if aliases else "Unknown"
        for channel in peer.get("channels", []):
            channel["alias"] = alias
            channels[channel["state"]].append(channel)
    return render_template("channels.html", channels=channels)

def main():
    app.run(port=8081, host="0.0.0.0")

if __name__ == "__main__":
    main()
