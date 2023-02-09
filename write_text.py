from PIL import ImageFont, ImageDraw, Image


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
