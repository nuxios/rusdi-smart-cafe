import model.cluster as ai

def main():
    print("Selamat datang di Rusdi Smart Cafe Assistant!")
    print("Ketik 'exit' untuk keluar dari percakapan.\n")

    while True:
        msg_content = input("\n\nYou: ")

        if msg_content.lower() == "exit":
            print("Terima kasih telah menggunakan Rusdi Smart Cafe Assistant. Sampai jumpa!")
            break

        ai.assistant(msg_content)

if __name__ == "__main__":
    main()