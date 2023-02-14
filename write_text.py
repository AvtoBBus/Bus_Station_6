from PIL import ImageFont, ImageDraw, Image
import random
import os


def check_input_format(text: str) -> bool:
    if len(text.split("_")) == 3:
        return True
    else:
        return False


def check_lenght_str(text: str, max_len: int) -> str:
    if len(text) < max_len:
        return text
    help_str = text
    result_str = ""
    str_to_rewrite = help_str.split("\n")[-1]
    while len(str_to_rewrite) > max_len:
        if str_to_rewrite[max_len - 1] != " ":
            help_list = str_to_rewrite.split(" ")
            calc_len = 0
            index = 0
            while calc_len < max_len:
                calc_len += len(help_list[index])
                index += 1
                if calc_len < len(str_to_rewrite):
                    calc_len += 1
            if str_to_rewrite[calc_len - 1] != " ":
                while str_to_rewrite[calc_len - 1] != " ":
                    calc_len -= 1
            li = list(str_to_rewrite)
            li[calc_len - 1] = '\n'
            help_str = "".join(li)
        else:
            li = list(str_to_rewrite)
            li[max_len - 1] = '\n'
            help_str = "".join(li)
        result_str += help_str.split('\n')[0]
        result_str += '\n'
        str_to_rewrite = help_str.split("\n")[-1]
    result_str += help_str.split("\n")[-1]
    return result_str


def separation_text(text: str) -> tuple:
    help_list = text.split("_")
    return (help_list[0], help_list[1], help_list[2])


def write_on_image(text: str, user_id: int) -> str:
    num_of_image = random.randint(1, len(os.listdir("image/")))
    image = Image.open(f"image/valentinka_{num_of_image}.png")
    draw = ImageDraw.Draw(image)
    new_path = f"New_file_{str(user_id)}.png"

    font_from_to = ImageFont.truetype("fonts/Ubuntu-BoldItalic.ttf", 100)
    font_text = ImageFont.truetype("fonts/Ubuntu-Bold.ttf", 120)
    fill_color = ""

    text_coord = (1850, 625)

    if num_of_image == 1 or num_of_image == 3:
        fill_color = "#FF2B6D"
    if num_of_image == 2:
        fill_color = "#15576D"
        text_coord = (1875, 625)

    result_tuple = separation_text(text)
    draw.text((2340, 1500), result_tuple[0], fill="white", font=font_from_to)
    draw.text((2340, 1880), result_tuple[1], fill="white", font=font_from_to)
    draw.text(text_coord, result_tuple[2], fill=fill_color, font=font_text)
    image.save(new_path)
    return new_path
