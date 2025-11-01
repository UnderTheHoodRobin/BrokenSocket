# BrokenSocket

# 🧩 BrokenSocket

> A broken (but functional) Python script to chat and send files over the same network or mobile hotspot — between two connected devices (vice versa).  
> Broken? Because it works on _my_ machine lol 😆

---

## 💡 What is this?

**BrokenSocket** is a lightweight Python experiment that lets two devices on the same Wi-Fi or hotspot chat and transfer files using nothing but sockets.  
No fancy protocols. No libraries. Just raw TCP — the way it was never meant to be used.

---

## ⚙️ Features

- 📡 Send files between devices on the **same network or hotspot**
- 💬 Chat between client and server
- 🔁 Works both ways (**vice versa**)
- 🧠 Pure Python (`socket`, `os`, `json`)
- 😂 “Broken” because it _only works perfectly on my machine_

---

## ⚡ Highspeed Mode

BrokenSocket runs at **highspeed** — as fast as your Wi-Fi (and luck) allows 🚀  

Send, chat, and transfer files instantly on your **local network**.  
No servers. No cloud.  
Just you, your friend, and a **broken socket** 💥


## Installation
- Using `pip` [recommended]:
```shell
pip install -U git+https://github.com/UnderTheHoodRobin/BrokenSocket
```

You can then use the tool by calling `BrokenSocket`

## Usage


```shell
usage: brokensocket [-h] {server,client}

BrokenSocket CLI

positional arguments:
  {server,client}  Run as server or client

options:
  -h, --help       show this help message and exit
```

➡️ **Launch as Server or Client from any terminal:**
- `brokensocket server`
- `brokensocket client`
- The server will show your **local IP address** (e.g. `192.168.43.1`)
- When asked, enter the IP shown by the server.

➡️ **Start chatting or use `/sendfile`** to send files between devices.