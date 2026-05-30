from PIL import Image
import pytesseract
import io


def extract_text_from_image(img_bytes):

    try:

        image = Image.open(
            io.BytesIO(img_bytes)
        )

        text = pytesseract.image_to_string(
            image
        )

        return {
            "success": True,
            "text": text,
            "word_count": len(text.split()),
            "image_width": image.width,
            "image_height": image.height,
            "error": None
        }

    except Exception as e:

        return {
            "success": False,
            "text": "",
            "word_count": 0,
            "image_width": 0,
            "image_height": 0,
            "error": str(e)
        }