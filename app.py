import streamlit as st
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

st.set_page_config(page_title="Cryptography Toolkit", page_icon="🔐", layout="centered")

st.title("🔐 Cryptography Algorithms Toolkit")
st.caption("Internship Project #1 — AES · RSA · SHA | Built with Python & Streamlit")
st.markdown("---")

tab1, tab2, tab3 = st.tabs(["🔒 AES Encryption", "🗝️ RSA Encryption", "🔢 SHA Hashing"])

# ── TAB 1: AES ──────────────────────────────────────────────────────────────
with tab1:
    st.header("AES-256 — Symmetric Encryption")
    st.info(
        "**AES** uses the **same secret key** to both encrypt and decrypt. "
        "Think of it as a lockbox where sender and receiver both have identical keys. "
        "Used in Wi-Fi (WPA2), HTTPS, disk encryption, and messaging apps."
    )
    message = st.text_area("Enter a message to encrypt:", value="This is my confidential message!", height=80)

    if st.button("🔒 Encrypt then Decrypt", use_container_width=True):
        key = get_random_bytes(32)
        cipher_enc = AES.new(key, AES.MODE_CBC)
        iv = cipher_enc.iv
        ciphertext = cipher_enc.encrypt(pad(message.encode(), AES.block_size))
        cipher_dec = AES.new(key, AES.MODE_CBC, iv=iv)
        decrypted = unpad(cipher_dec.decrypt(ciphertext), AES.block_size).decode()

        col1, col2 = st.columns(2)
        col1.metric("Key length", "256 bits")
        col2.metric("Mode", "CBC")
        st.code(f"Secret key (hex) : {key.hex()}", language="text")
        st.code(f"IV         (hex) : {iv.hex()}", language="text")
        st.code(f"Ciphertext (hex) : {ciphertext.hex()}", language="text")
        if decrypted == message:
            st.success(f"✅ Decrypted successfully: **{decrypted}**")
        st.caption("The same key encrypted AND decrypted — that's symmetric encryption.")

# ── TAB 2: RSA ──────────────────────────────────────────────────────────────
with tab2:
    st.header("RSA-2048 — Asymmetric / Public-Key Encryption")
    st.info(
        "**RSA** uses two keys: a **public key** (anyone can encrypt with it) "
        "and a **private key** (only you can decrypt). This is how HTTPS works."
    )
    message = st.text_input("Enter a short message to encrypt:", value="Meet me at 9pm.")
    st.caption("Key generation takes 1-2 seconds — that is normal.")

    if st.button("🗝️ Generate Keys and Encrypt", use_container_width=True):
        with st.spinner("Generating 2048-bit RSA key pair..."):
            rsa_key = RSA.generate(2048)
            public_key = rsa_key.publickey()
            ciphertext = PKCS1_OAEP.new(public_key).encrypt(message.encode())
            decrypted = PKCS1_OAEP.new(rsa_key).decrypt(ciphertext).decode()

        st.success(f"✅ Decrypted successfully: **{decrypted}**")
        st.code(f"Ciphertext (hex): {ciphertext.hex()[:120]}...", language="text")
        with st.expander("🔓 Public Key (safe to share)"):
            st.code(public_key.export_key().decode())
        with st.expander("🔒 Private Key (NEVER share this)"):
            st.code(rsa_key.export_key().decode()[:300] + "\n... (truncated for safety)")

# ── TAB 3: SHA ──────────────────────────────────────────────────────────────
with tab3:
    st.header("SHA Hashing — One-Way Functions")
    st.info(
        "**Hashing** is one-way — you can NEVER reverse it. "
        "Websites store the hash of your password, never the password itself."
    )
    text = st.text_input("Enter any text to hash:", value="CyberSecurityInternship2025")

    if text:
        st.markdown("#### Hashes using different algorithms")
        for algo in ["md5", "sha1", "sha256", "sha512"]:
            h = hashlib.new(algo, text.encode()).hexdigest()
            st.code(f"{algo.upper().ljust(8)}: {h}", language="text")

        st.markdown("#### 🌊 Avalanche Effect — one character change scrambles everything")
        h1 = hashlib.sha256(text.encode()).hexdigest()
        h2 = hashlib.sha256((text + "!").encode()).hexdigest()
        col1, col2 = st.columns(2)
        col1.markdown(f"**`{text}`**")
        col1.code(h1)
        col2.markdown(f"**`{text}!`**")
        col2.code(h2)
        changed = sum(a != b for a, b in zip(h1, h2))
        st.metric("Characters changed in hash", f"{changed} / {len(h1)}")

st.markdown("---")
st.caption("Codect Technologies Cybersecurity Internship | Project 6: Cryptography Algorithms Implementation")
