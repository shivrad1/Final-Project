def passcode(passcode, person):
    bens_passcode = 89931
    shivs_passcode = 11242

    if passcode == bens_passcode and person == 'ben':
        return True
    elif passcode == shivs_passcode and person == 'shiv':
        return True
    else:
        return False
    
