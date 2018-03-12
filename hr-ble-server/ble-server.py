from server import server



if __name__ == "__main__":
    server.debug = True
    server.run(host = '0.0.0.0', port=5005)
