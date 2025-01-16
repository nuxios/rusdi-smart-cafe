import os
import platform
import model.as_test as ai


def clear_terminal():
    """Clear the terminal screen."""
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")


clear_terminal()

print("Selamat datang di ASSISTANT PEMBELIAN!")
print("Ketik 'exit' untuk keluar dari percakapan.\n")


def main():

    # print(ai.system_content)
    while True:
        msg_content = input("\n\nYou: ")
        if msg_content.lower() == "exit":
            print(
                "Terima kasih telah menggunakan ASSISTANT PEMBELIAN. Sampai jumpa!"
            )
            break  

        ai.msg_data(msg_content)


if __name__ == "__main__":
    main()
