import utime
from machine import I2C, Pin
from PICO_I2C_LCD  import *
from PLAYERMODULE import *

# I2C config
I2C_ADDR = 0x27
I2C_NUM_ROWS = 4
I2C_NUM_COLS = 20
i2c = I2C(1, sda = Pin(2), scl = Pin(3), freq = 400000)
lcd = I2cLcd(i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)

# Button config
reset_play = Pin(10, Pin.IN, Pin.PULL_UP)
btn_py1_moveUp = Pin(11, Pin.IN, Pin.PULL_UP)
btn_py1_shot = Pin(12, Pin.IN, Pin.PULL_UP)
btn_py1_moveDown = Pin(13, Pin.IN, Pin.PULL_UP)
btn_py2_moveUp = Pin(14, Pin.IN, Pin.PULL_UP)
btn_py2_shot = Pin(15, Pin.IN, Pin.PULL_UP)
btn_py2_moveDown = Pin(16, Pin.IN, Pin.PULL_UP)

Player01Char = [
  0x00,
  0x1E,
  0x1C,
  0x1F,
  0x1F,
  0x1C,
  0x1E,
  0x00
]

Player02Char = [
  0x00,
  0x1F,
  0x07,
  0x1F,
  0x1F,
  0x07,
  0x1F,
  0x00    
]

happyFace = [
  0x00,
  0x0A,
  0x00,
  0x04,
  0x11,
  0x11,
  0x0E,
  0x00
]

bullet = [
  0x00,
  0x00,
  0x00,
  0x0E,
  0x0E,
  0x00,
  0x00,
  0x00    
]

lcd.custom_char(0, bytearray(happyFace))
lcd.custom_char(1, bytearray(Player01Char))
lcd.custom_char(2, bytearray(Player02Char))
lcd.custom_char(3, bytearray(bullet))


def lcd_str(mensage, col, row):
    lcd.move_to(col, row)
    lcd.putstr(mensage)

def lcd_char(char, col, row):
    lcd.move_to(col,row)
    lcd.putchar(chr(char))
    
def welcome():
        lcd_str("Welcome brother: ", 0, 0)
        lcd_str("Let's play", 0, 1)
        lcd_str("Shot Game", 0, 2)
        for i in range(20):
          lcd.move_to(i,3)
          lcd.putchar(chr(0))
          utime.sleep_ms(100)

def winnerPoster(winner, p1, p2):
        marker = "P1:"+str(p1.score)+" -- P2:"+str(p2.score)
        if winner == "P1":
            winnerBox = "Player 1 has won :)"
        else:
            winnerBox = "Player 2 has won"
        lcd_str("Congratulations: ", 0, 0)
        lcd_str(winnerBox, 0, 1)
        lcd_str(marker, 0, 2)
        for i in range(20):
          lcd.move_to(i,3)
          lcd.putchar(chr(0))
          utime.sleep_ms(100)
  
p1 = Player(I2C_NUM_ROWS, I2C_NUM_COLS, 1)
p2 = Player(I2C_NUM_ROWS, I2C_NUM_COLS, 2)  

btn_py1_moveUp.irq(p1.moveUp,Pin.IRQ_FALLING)
btn_py1_moveDown.irq(p1.moveDown,Pin.IRQ_FALLING)
btn_py2_moveUp.irq(p2.moveUp,Pin.IRQ_FALLING)
btn_py2_moveDown.irq(p2.moveDown,Pin.IRQ_FALLING)
btn_py1_shot.irq(p1.shot, Pin.IRQ_FALLING)
btn_py2_shot.irq(p2.shot, Pin.IRQ_FALLING)

ref_timeP1 = utime.ticks_ms()
ref_timeP2 = utime.ticks_ms()

def main():
    global ref_timeP1
    global ref_timeP2
    welcome()
    utime.sleep_ms(3000)
    lcd.clear()
    while(True):
        if p1.shooting:
            ref_time_elapsedR1 = utime.ticks_diff(utime.ticks_ms(), ref_timeP1)
            if ref_time_elapsedR1 >= 70:
                p1.bulletAgain(p2)
                ref_timeP1 = utime.ticks_ms()
            if p1.score >= 5:
                    lcd.clear()
                    winnerPoster("P1", p1, p2)
                    utime.sleep_ms(4000)
                    lcd.clear()
                    p1.resetState()
                    p2.resetState()
        if p2.shooting:
            ref_time_elapsedR2 = utime.ticks_diff(utime.ticks_ms(), ref_timeP2)
            if ref_time_elapsedR2 >= 70:
                p2.bulletAgain(p1)
                ref_timeP2 = utime.ticks_ms()
            if p2.score >= 5:
                    lcd.clear()
                    winnerPoster("P2", p1, p2)
                    utime.sleep_ms(4000)
                    lcd.clear()
                    p1.resetState()
                    p2.resetState()
            
        lcd.clear()
        lcd_char(1,p1.position["x"], p1.position["y"])
        lcd_char(2,p2.position["x"], p2.position["y"])
        lcd_char(3,p1.shotPosition["x"], p1.shotPosition["y"])
        lcd_char(3,p2.shotPosition["x"], p2.shotPosition["y"])
        utime.sleep_ms(70)

if __name__ == "__main__":
    main()


