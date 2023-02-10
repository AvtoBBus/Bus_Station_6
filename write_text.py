from PIL import ImageFont, ImageDraw, Image


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
    image = Image.open("valentine.jpg")
    draw = ImageDraw.Draw(image)
    new_path = f"New_file_{str(user_id)}.jpg"

    font_from_to = ImageFont.truetype("fonts/Ubuntu-Regular.ttf", 32)
    font_text = ImageFont.truetype("fonts/Ubuntu-Bold.ttf", 32)

    result_tuple = separation_text(text)
    draw.text((110, 150), result_tuple[0], fill="red", font=font_from_to)
    draw.text((110, 180), result_tuple[1], fill="red", font=font_from_to)
    draw.text((110, 230), result_tuple[2], fill="#FF2B6D", font=font_text)
    image.save(new_path)
    return new_path
