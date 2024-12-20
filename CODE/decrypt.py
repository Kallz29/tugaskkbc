# Performs decryption on images
def decrypt_image(self, input_image_path, output_image_path, key, iv_path):
        self.output_image_path = output_image_path

        # Read the IV from the separate file
        with open(iv_path, 'rb') as f:
            unique_iv = f.read()

        # Read the encrypted data
        with open(input_image_path, 'rb') as f:
            encrypted_data = f.read()

        try:
            # Separate the IV from the encrypted data
            iv = encrypted_data[:AES.block_size]
            encrypted_data = encrypted_data[AES.block_size:]

            # Initialize AES cipher
            cipher = AES.new(key, AES.MODE_CBC, unique_iv)

            # Decrypt the image data
            decrypted_data = unpad(cipher.decrypt(encrypted_data), AES.block_size)

            try:
                # Convert decrypted bytes to image
                decrypted_image = Image.open(io.BytesIO(decrypted_data))
            except:
                tk.messagebox.showerror(title="Wrong IV File", message="Wrong IV File")
                self.clear_screen()
                self.file_name_label.destroy()
                self.file_status_label.destroy()
                self.key_entry.destroy()
                self.btn_3.destroy()
                return

            # Save the decrypted image
            decrypted_image.save(self.output_image_path, format=decrypted_image.format)

            self.display_decrypted_image(self.output_image_path)

            self.encryption_status = False
        except ValueError:
            tk.messagebox.showerror(title="Incorrect Key", message="Incorrect key value")
            self.clear_screen()
            self.file_name_label.destroy()
            self.file_status_label.destroy()
            self.key_entry.destroy()
            self.btn_3.destroy()
            
    # Performs pre-decryption tasks
def pre_decryption(self):
        if self.image_path == '':
            tk.messagebox.showerror(title="Image Missing", message="Please select an image")
            return
        elif self.key_entry.get()=='':
            tk.messagebox.showerror(title="Key Missing", message="Please enter the key")
            return
        elif self.iv_path == '':
            tk.messagebox.showerror(title="IV File Missing", message="Please select the IV file")
            return
        else:
            key = self.key_var.get()
            key = bytes(key, encoding="utf-8")

            chosen_dir = self.choose_directory()
            filename = os.path.basename(self.image_path)
            image_name = filename.split('.')[0]
            output_image_path = f"{chosen_dir}/{image_name}_recovered.jpg"
            
            self.decrypt_image(self.image_path, output_image_path, key, self.iv_path)
            self.image_path = ''
            self.iv_path = ''