
MOTOR_MAX_SPEED = 100
MOTOR_POWER_BRAKE = 127

def motorPowerOutput(power):
    offset = 35
    # We transform the initial input to a value between 35 and 100
    # since the motor doesn't actually start moving with anything below that

    if power == MOTOR_POWER_BRAKE:
        hexValue = intToHexString(power)
        return hexValue
    
    positiveValue = power >= 0
    power = abs(power)
    
    if power > MOTOR_MAX_SPEED: 
        power = MOTOR_MAX_SPEED

    actualPower = ((100.0 - offset) / 100.0) * power + offset
    actualPowerInt = round(actualPower)

    hexValue = ""
    
    if positiveValue:
        hexValue = intToHexString(actualPowerInt)

    else: # if value is negative
        actualPowerInt = -actualPowerInt
        hexValue = intToHexString(256 + actualPowerInt)

    return hexValue


def intToHexString(value):
    return "0x%0.2X" % value

#print(motorPowerOutput(-100))

        

        
            
