import streamlit as st

# ==========================================
# 1. THE EDITPAD-STYLE LOGIC (Backend)
# ==========================================

# We define three characters that take up physical space but are completely invisible.
ZERO_CHAR = '\u2800'  # Braille Pattern Blank (Represents '0')
ONE_CHAR = '\u3164'   # Hangul Filler (Represents '1')
SPLIT_CHAR = '\uffa0' # Halfwidth Hangul Filler (Separates letters)

def text_to_invisible(text):
    """Converts normal text to a massive block of invisible 'Empty Box' characters."""
    invisible_words = []
    
    for letter in text:
        # Convert letter to a 16-bit binary string (e.g., '0000000001100001')
        binary_string = format(ord(letter), '016b')
        
        # Swap 0s and 1s with our physical blank characters
        invisible_string = binary_string.replace('0', ZERO_CHAR).replace('1', ONE_CHAR)
        invisible_words.append(invisible_string)
        
    # Join the converted letters together with our invisible separator
    return SPLIT_CHAR.join(invisible_words)

def invisible_to_text(invisible_text):
    """Converts the massive block of invisible characters back to normal text."""
    # First, clean the input so we ONLY look at our three specific blank characters
    # This prevents normal spaces from breaking the decryption
    clean_text = "".join(c for c in invisible_text if c in [ZERO_CHAR, ONE_CHAR, SPLIT_CHAR])
    
    normal_words = []
    
    # Split the blank text back into individual letter blocks
    for block in clean_text.split(SPLIT_CHAR):
        if not block:
            continue
            
        # Swap the blank characters back to '0' and '1'
        binary_string = block.replace(ZERO_CHAR, '0').replace(ONE_CHAR, '1')
        
        # Convert the binary string back to a character
        try:
            letter = chr(int(binary_string, 2))
            normal_words.append(letter)
        except ValueError:
            continue
            
    return "".join(normal_words)

# ==========================================
# 2. THE FRONTEND (Using Streamlit)
# ==========================================

st.set_page_config(page_title="Editpad-Style Encryptor")

st.title("Ghost Text: Clipboard-Safe Encryptor")
st.write("This uses physical blank characters. It will create very long blocks of empty space, but it survives copy/pasting perfectly.")

# --- Encryption Section ---
st.subheader("1. Encrypt Normal Text")
text_to_hide = st.text_input("Type your secret message here:")

if st.button("Encrypt"):
    if text_to_hide:
        encrypted_result = text_to_invisible(text_to_hide)
        st.success("Successfully encrypted! Click the copy icon in the top right of the box below:")
        
        # The output will look like a massive blank space, but the copy button will grab it all perfectly.
        st.code(encrypted_result, language="text")
    else:
        st.warning("Please enter text to encrypt.")

st.divider()

# --- Decryption Section ---
st.subheader("2. Decrypt Invisible Text")
text_to_reveal = st.text_area("Paste your massive blank space here:")

if st.button("Decrypt"):
    if text_to_reveal:
        decrypted_result = invisible_to_text(text_to_reveal)
        if decrypted_result:
            st.success("Secret message revealed:")
            st.info(decrypted_result)
        else:
            st.error("Could not find any hidden text. Make sure you copied the entire blank space.")
    else:
        st.warning("Please paste invisible text to decrypt.")
