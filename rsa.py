import math
import random
import streamlit as st
def is_prime(p,q):
    if p <= 1 or q <= 1:
        return False
    if p == 2 or q == 2 :
        return True
    if p % 2 == 0 or q % 2 == 0:
        return False
    max_divisor_p = int(p**0.5) + 1
    max_divisor_q = int(q**0.5) + 1
    for d_p in range(3, max_divisor_p, 2):
        if p % d_p == 0:
            return False
    for d_q in range(3, max_divisor_q, 2):
        if q % d_q == 0:
            return False
    return True

# Calculate n & phi
def calculate_n_phi(p, q):
    n = p * q
    phi = (p-1) * (q-1)
    return n, phi

# Check if e is coprime with phi
def check_coprime(e, phi):
    return math.gcd(e, phi) == 1

# Generate e such that 1 < e < phi & gcd(e, phi) = 1
def generate_e(phi):
    e = random.randint(2, phi-1)
    while not check_coprime(e, phi):
        e = random.randint(2, phi-1)
    return e

# Generate d such that 1 < d < phi & (d * e) % phi = 1
def generate_d(e, phi):
    d = random.randint(2, phi-1)
    while (d * e) % phi != 1:
        d = random.randint(2, phi-1)
    return d

# RSA encryption function
def encrypt(plaintext, e, n):
    encrypted_text = [chr((ord(char) ** e) % n) for char in plaintext]
    return ''.join(encrypted_text)

# RSA decryption function
def decrypt(ciphertext, d, n):
    decrypted_text = [chr((ord(char) ** d) % n) for char in ciphertext]
    return ''.join(decrypted_text)

def main():
    st.set_page_config(
        page_title="RSA",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    st.title("RSA Application")

    st.sidebar.header("Operations")
    typ = st.sidebar.radio("Select operation", ["Encryption", "Decryption"])

    col1, col2, col3 = st.columns([1, 1, 2])

    with col1:
        p = st.number_input("Enter p:", min_value=1, step=1)

    with col2:
        q = st.number_input("Enter q:", min_value=1, step=1)

    with col3:
        e = st.number_input("Enter e:", min_value=1, step=1)

    n, phi = calculate_n_phi(p, q)

    if not is_prime(p, q):
        st.error("p or q are not prime.")
        return
    elif e == 0 or e == 1:
        st.error("e must be greater than 1.")
        return
    elif e >= phi:
        st.error("e must be less than phi.")
        return
    elif not check_coprime(e, phi):
        st.error("e and phi are not coprime.")
        return

    if typ == "Encryption":
        plaintext = st.text_input("Enter text to encrypt:")
        if st.button("Encrypt"):
            ciphertext = encrypt(plaintext, e, n)
            st.success(f"Encrypted text: {ciphertext}")
    elif typ == "Decryption":
        ciphertext = st.text_input("Enter text to decrypt:")
        d = generate_d(e, phi)
        if st.button("Decrypt"):
            decrypted_text = decrypt(ciphertext, d, n)
            st.success(f"Decrypted text: {decrypted_text}")
    else:
        st.warning("Please select a valid operation (Encryption or Decryption)")

if __name__ == "__main__":
    main()