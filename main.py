import pygame

pygame.init()

# =========================
# صفحه
# =========================

WIDTH = 720
HEIGHT = 1280

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("ماشین حساب")

clock = pygame.time.Clock()

# =========================
# رنگ‌ها
# =========================

BG = (25, 25, 25)
BUTTON = (55, 55, 55)
OPERATOR = (90, 90, 90)
WHITE = (255, 255, 255)
GREEN = (80, 180, 80)

# =========================
# فونت
# =========================

font_big = pygame.font.Font(None, 90)
font_button = pygame.font.Font(None, 60)

# =========================
# وضعیت ماشین حساب
# =========================

display = "0"

first_number = None
operator = None

new_number = True


# =========================
# محاسبه
# =========================

def calculate(a, b, op):

    if op == "+":
        return a + b

    if op == "-":
        return a - b

    if op == "×":
        return a * b

    if op == "÷":

        if b == 0:
            return None

        return a / b

    return None


# =========================
# دکمه
# =========================

def press(key):

    global display
    global first_number
    global operator
    global new_number

    # -------------------------
    # پاک کردن
    # -------------------------

    if key == "C":

        display = "0"
        first_number = None
        operator = None
        new_number = True

        return

    # -------------------------
    # عدد
    # -------------------------

    if key in "0123456789":

        if new_number or display == "0" or display == "Error":

            display = key
            new_number = False

        else:

            display += key

        return

    # -------------------------
    # اعشار
    # -------------------------

    if key == ".":

        if new_number:

            display = "0."
            new_number = False

        elif "." not in display:

            display += "."

        return

    # -------------------------
    # عملگر
    # -------------------------

    if key in ["+", "-", "×", "÷"]:

        try:
            first_number = float(display)

        except:
            first_number = 0

        operator = key
        new_number = True

        return

    # -------------------------
    # مساوی
    # -------------------------

    if key == "=":

        if first_number is None or operator is None:
            return

        try:

            second_number = float(display)

            result = calculate(
                first_number,
                second_number,
                operator
            )

            if result is None:

                display = "Error"

            elif result == int(result):

                display = str(int(result))

            else:

                display = str(round(result, 8))

        except:

            display = "Error"

        first_number = None
        operator = None
        new_number = True


# =========================
# دکمه‌ها
# =========================

labels = [
    ["C", "÷", "×", "-"],
    ["7", "8", "9", "+"],
    ["4", "5", "6", "="],
    ["1", "2", "3", "."],
    ["0", "", "", ""]
]

margin = 20
gap = 15

button_width = (
    WIDTH - margin * 2 - gap * 3
) // 4

button_height = 125

start_y = 430


# =========================
# مستطیل دکمه
# =========================

def get_button(col, row):

    x = margin + col * (button_width + gap)

    y = start_y + row * (button_height + gap)

    return pygame.Rect(
        x,
        y,
        button_width,
        button_height
    )


# =========================
# صفر بزرگ
# =========================

zero_rect = pygame.Rect(
    margin,
    start_y + 4 * (button_height + gap),
    button_width * 2 + gap,
    button_height
)


# =========================
# تشخیص لمس
# =========================

def handle_touch(x, y):

    # -------------------------
    # صفر
    # -------------------------

    if zero_rect.collidepoint(x, y):

        press("0")
        return

    # -------------------------
    # بقیه دکمه‌ها
    # -------------------------

    for row in range(4):

        for col in range(4):

            rect = get_button(col, row)

            if rect.collidepoint(x, y):

                key = labels[row][col]

                if key != "":

                    press(key)

                return


# =========================
# حلقه اصلی
# =========================

running = True

while running:

    for event in pygame.event.get():

        # خروج
        if event.type == pygame.QUIT:

            running = False

        # -------------------------
        # فقط لمس اندروید
        # -------------------------

        elif event.type == pygame.FINGERDOWN:

            # تبدیل مختصات نسبی لمس
            x = int(event.x * screen.get_width())
            y = int(event.y * screen.get_height())

            handle_touch(x, y)

    # =========================
    # رسم
    # =========================

    screen.fill(BG)

    # نمایشگر
    pygame.draw.rect(
        screen,
        (40, 40, 40),
        (20, 30, WIDTH - 40, 350),
        border_radius=25
    )

    # متن
    text = font_big.render(
        display,
        True,
        GREEN
    )

    screen.blit(
        text,
        (
            WIDTH - text.get_width() - 40,
            250
        )
    )

    # -------------------------
    # دکمه‌ها
    # -------------------------

    for row in range(4):

        for col in range(4):

            key = labels[row][col]

            if key == "":
                continue

            rect = get_button(col, row)

            if key in ["C", "÷", "×", "-", "+", "="]:

                color = OPERATOR

            else:

                color = BUTTON

            pygame.draw.rect(
                screen,
                color,
                rect,
                border_radius=20
            )

            text = font_button.render(
                key,
                True,
                WHITE
            )

            text_rect = text.get_rect(
                center=rect.center
            )

            screen.blit(
                text,
                text_rect
            )

    # -------------------------
    # صفر بزرگ
    # -------------------------

    pygame.draw.rect(
        screen,
        BUTTON,
        zero_rect,
        border_radius=20
    )

    text = font_button.render(
        "0",
        True,
        WHITE
    )

    text_rect = text.get_rect(
        center=zero_rect.center
    )

    screen.blit(
        text,
        text_rect
    )

    # نمایش
    pygame.display.flip()

    clock.tick(60)


pygame.quit()