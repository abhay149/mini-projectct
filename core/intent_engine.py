def detect_intent(text):
    text = text.lower().strip()

    # 🔥 STEP 1: NORMALIZE COMMON SPEECH ERRORS
    text = text.replace("hey aries", "hey aris")
    text = text.replace("hay aries", "hey aris")
    text = text.replace("here is", "hey aris")
    text = text.replace("hair is", "hey aris")
    text = text.replace("aries", "aris")

    # 🔥 STEP 2: OPEN ARIS (HIGHEST PRIORITY)
    if "aris" in text and "open" in text:
        return "open_aris"

    if "open aris" in text or "launch aris" in text:
        return "open_aris"

    # 🔥 STEP 3: SHOPPING
    if any(word in text for word in ["buy", "price", "shop", "order", "cost"]):
        return "shopping"

    # 🔥 STEP 4: ALARM
    if "alarm" in text or "reminder" in text:
        return "alarm"

    # 🔥 STEP 5: AUTOMATION (OTHER APPS)
    if any(word in text for word in ["open", "launch", "start"]):
        return "automation"

    # 🔥 DEFAULT
    return "chat"