from hedera import Client, AccountId, PrivateKey, ConsensusTopicCreateTransaction, ConsensusMessageSubmitTransaction, ConsensusTopicQuery, Hbar
import base64
from cryptography.fernet import Fernet

client = Client.for_testnet()
client.set_operator(AccountId.fromString("your-account-id"), PrivateKey.fromString("your-private-key"))

# Generate a key for encryption (only done once)
key = Fernet.generate_key()
cipher_suite = Fernet(key)

# Step 1: Create a Topic
def create_topic():
    tx = ConsensusTopicCreateTransaction() \
        .set_admin_key(PrivateKey.fromString("your-private-key")) \
        .set_max_renewal_period(2592000) \
        .set_auto_renew_period(2592000) \
        .freeze_with(client)
    
    tx_sign = tx.sign(PrivateKey.fromString("your-private-key"))
    tx_response = tx_sign.execute(client)
    
    receipt = tx_response.get_receipt(client)
    topic_id = receipt.topic_id
    print(f"Topic Created: {topic_id}")
    return topic_id

# Step 2: Encrypt a message
def encrypt_message(message):
    encrypted_message = cipher_suite.encrypt(message.encode())
    return base64.b64encode(encrypted_message).decode()

# Step 3: Send a message to the topic
def send_message(topic_id, message):
    encrypted_message = encrypt_message(message)
    tx = ConsensusMessageSubmitTransaction() \
        .set_topic_id(topic_id) \
        .set_message(encrypted_message) \
        .freeze_with(client)
    
    tx_sign = tx.sign(PrivateKey.fromString("your-private-key"))
    tx_response = tx_sign.execute(client)
    print(f"Message Sent: {message}")
    return tx_response

# Step 4: Decrypt a message
def decrypt_message(encrypted_message):
    encrypted_message_bytes = base64.b64decode(encrypted_message.encode())
    decrypted_message = cipher_suite.decrypt(encrypted_message_bytes).decode()
    return decrypted_message

# Step 5: Retrieve messages from the topic
def get_messages(topic_id):
    query = ConsensusTopicQuery() \
        .set_topic_id(topic_id) \
        .set_start_time(0) \
        .set_end_time(0) \
        .set_max_query_payment(Hbar.from(2)) \
        .set_max_query_record(10) \
        .set_query_payment(Hbar.from(1)) \
        .freeze_with(client)

    response = query.execute(client)
    messages = []
    for message in response.messages:
        decrypted_message = decrypt_message(message.message)
        messages.append(decrypted_message)
    return messages

# Step 6: Filter messages by keyword
def filter_messages(messages, keyword):
    filtered_messages = [msg for msg in messages if keyword.lower() in msg.lower()]
    return filtered_messages

# Example Usage
def main():
    topic_id = create_topic()
    
    messages = [
        "Hello, Hedera!",
        "Learning HCS",
        "Message 3"
    ]
    
    for msg in messages:
        send_message(topic_id, msg)
    
    # Retrieve messages from the topic
    received_messages = get_messages(topic_id)
    print(f"Messages Received: {received_messages}")
    
    # Filter messages based on a keyword
    filtered_messages = filter_messages(received_messages, "Hedera")
    print(f"Filtered Messages: {filtered_messages}")

if __name__ == "__main__":
    main()
