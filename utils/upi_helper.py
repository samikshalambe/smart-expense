import qrcode
from PIL import Image
import io

def generate_upi_qr(upi_id, biller_name, amount, description):
    """
    Generates a UPI QR code image from the given parameters.
    Format: upi://pay?pa={upi_id}&pn={biller_name}&am={amount}&tn={description}
    """
    # Clean inputs
    biller_name = biller_name.replace(" ", "%20")
    description = description.replace(" ", "%20")
    
    upi_url = f"upi://pay?pa={upi_id}&pn={biller_name}&am={amount:.2f}&tn={description}"
    
    # Generate QR Code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(upi_url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    
    # Convert PIL Image to Bytes for Streamlit
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    byte_im = buf.getvalue()
    
    return byte_im
