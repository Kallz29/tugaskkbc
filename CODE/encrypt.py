 # Generates random key values
def generate_random_text(self):
        # Available length options: 16, 24, or 32 (You can modify here)
        length = 32
        # Define the character pool containing all desired characters
        char_pool = string.ascii_uppercase + string.ascii_lowercase + string.digits

        random_text = ''.join(random.sample(char_pool, length))
        return random_text

    # Performs encryption on images
def encrypt_image(self, image_path, output_image_path, iv_path, key):
        image = Image.open(image_path)
        # Generate a random IV
        iv = get_random_bytes(AES.block_size)

        # Get a unique identifier from the filename
        image_hash = SHA256.new(os.path.basename(image_path).encode("utf-8")).hexdigest()

        # Combine key-specific value with random string (nonce) using HMAC
        key_specific = HMAC.new(key, msg=image_hash.encode("utf-8"), digestmod=SHA256).digest()
        unique_iv = HMAC.new(key_specific, msg=os.urandom(16), digestmod=SHA256).digest()[:16]

        # Convert the image to bytes
        img_byte_array = io.BytesIO()
        image.save(img_byte_array, format=image.format)
        img_bytes = img_byte_array.getvalue()

        # Initialize AES cipher
        cipher = AES.new(key, AES.MODE_CBC, unique_iv)

        # Encrypt the image data with padding
        padded_data = pad(img_bytes, AES.block_size)
        encrypted_data = iv + cipher.encrypt(padded_data)

        # Write the encrypted data with IV to the output image file
        with open(output_image_path, 'wb') as f:
            f.write(encrypted_data)

        # Saving the iv file
        with open(iv_path, 'wb') as f:
            f.write(unique_iv)

        self.decryption_status = False

    # Performs pre-encryprion tasks
def pre_encryption(self):
        if self.image_path == '':
            tk.messagebox.showerror(title="Image Missing", message="Please select an image")
        else:
            key = self.generate_random_text()
            key = bytes(key, encoding="utf-8")
            key_str = key[0:].decode("utf-8")

            chosen_dir = self.choose_directory()
            filename = os.path.basename(self.image_path)
            image_name = filename.split('.')[0]
            output_image_path = f"{chosen_dir}/{image_name}_encrypted.jpg"
            iv_path = f"{chosen_dir}/{image_name}_encrypted.iv"

            self.encrypt_image(self.image_path, output_image_path, iv_path, key)

            self.status_label.config(text="Image is encrypted", bg="green")

            self.key_label_var = StringVar()
            self.key_label = Entry(self.frame2, textvariable=self.key_label_var, font=("Montserrat", 8), width=20, bg="#03226F", fg="white")
            self.key_label.insert(0, f"{key_str}")
            self.key_label.place(x=180, y=17)

            self.clear_screen()
            self.image_path = ''