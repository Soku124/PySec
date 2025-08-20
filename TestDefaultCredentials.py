import paramiko
import telnetlib3
import asyncio

def SSHlogin(host, port, username, password):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, port, username=username, password=password)
        ssh_session = ssh.get_transport().open_session()
        if ssh_session.active:
            print(f"SSH login successful on {host}:{port} with username: {username} and password: {password}")
    except Exception as e:
        return
    ssh.close()

# def TelnetLogin(host, port, username, password):
#     user = bytes(username + "\n","utf-8")
#     passwd = bytes(password+"n","utf-8")

#     tn = telnetlib3.TelnetClient(host, passwd)
#     tn.reader(bytes("login: ","utf-8"))
#     tn.writer(user)
#     tn.reader(bytes("Password: ","utf-8"))
#     tn.writer(passwd)
#     try:
#         result = tn.expect([bytes("Last Login", "utf-8")], timeout = 2)
#         if (result[0] >= 0):
#             print(f"Telnet login successful on {host}:{port} with username:{username} and password: {password}")
#         tn.close()
#     except EOFError:
#         print(f"Login failed {username}: {password}")

async def TelnetLogin(host, port, username, password):
    try:
        reader, writer  = await telnetlib3.open_connection(host, port, encoding="utf-8")

        # wait for login prompt
        await reader.readuntil("login: ")
        writer.write(username+"\n")

        # wait for password prompt
        await reader.readuntil("Password: ")
        writer.write(password+"\n")


        # small delay to get server response
        await asyncio.sleep(1)
        output = await reader.read(1024)

        if "Last login" in output or "$" in output or "#" in output:
            print(f"Telnet login successful on {host}:{port} with username: {username} and password: {password}")
        else:
            print(f"Telnet login failed for {username}: {password}")
        
        writer.close()
        await writer.wait_closed()
    except Exception as e:
        print(f"Error: {e}")





host = "127.0.0.1"
with open("defaults.txt", "r") as f:
    for line in f:
        username, password = line.split()
        # SSH login (sync)
        SSHlogin(host=host, port=22, username=username, password=password)

        # Telnet login (async)
        asyncio.run(TelnetLogin(host=host, port=23, username=username, password=password))
