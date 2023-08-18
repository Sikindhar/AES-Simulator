
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import os

# Encrypt function
def encrypt_image(input_image_path, output_image_path, key):
    cipher = AES.new(key, AES.MODE_CBC)

    with open(input_image_path, 'rb') as f:
        image_data = f.read()

    encrypted_image_data = cipher.encrypt(pad(image_data, AES.block_size))

    with open(output_image_path, 'wb') as f:
        f.write(cipher.iv + encrypted_image_data)


# Decrypt function
def decrypt_image(encrypted_image_path, decrypted_image_path, key):
    with open(encrypted_image_path, 'rb') as f:
        data = f.read()
        iv = data[:AES.block_size]
        ciphertext = data[AES.block_size:]

    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_image_data = unpad(cipher.decrypt(ciphertext), AES.block_size)

    with open(decrypted_image_path, 'wb') as f:
        f.write(decrypted_image_data)


# Main function
def main():
    input_image_path = r"yourPath" # Your path of the image 
    output_dir = os.path.expanduser("~")  # User's home directory
    image_name = os.path.splitext(os.path.basename(input_image_path))[0]
    
    # Create output filenames
    encrypted_image_path = os.path.join(output_dir, f"{image_name}_encrypted_image.png")
    decrypted_image_path = os.path.join(output_dir, f"{image_name}_decrypted_image.png")

    # Encrypt the image
    key = os.urandom(16)  # Generate a random 16-byte key (128-bit key size)
    print('Encryption key:', key.hex())
    encrypt_image(input_image_path, encrypted_image_path, key)
    print(f'Image encrypted and saved as {image_name}_encrypted_image.png')

    # Prompt for decryption key
    decryption_key = input("Enter the decryption key (in hexadecimal): ").strip()
    decryption_key = bytes.fromhex(decryption_key)

    # Decrypt the image
    try:
        decrypt_image(encrypted_image_path, decrypted_image_path, decryption_key)
        print(f'Image decrypted and saved as {image_name}_decrypted_image.png')
    except ValueError:
        print("Incorrect key! I am AES ...haha You cannot break me!")


if __name__ == "__main__":
    main()

