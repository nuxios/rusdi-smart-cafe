import os
import platform
import model.assistant as ai


def clear_terminal():
    """Clear the terminal screen."""
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")


clear_terminal()

print("Selamat datang di Rusdi Smart Cafe Assistant!")
print("Ketik 'exit' untuk keluar dari percakapan.\n")


def main():

    while True:
        msg_content = input("\n\nYou: ")

        if msg_content.lower() == "exit":
            print(
                "Terima kasih telah menggunakan Rusdi Smart Cafe Assistant. Sampai jumpa!"
            )
            break

        ai.msg_data(msg_content)


if __name__ == "__main__":
    main()
