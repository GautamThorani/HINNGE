import qrcode
import base64
import io

class QRService:
    """Service for QR code generation"""
    
    @staticmethod
    def generate_qr_code(secret: str, email: str, issuer: str = "HENNGE") -> tuple[str, str]:
        """Generate QR code as base64 string and provisioning URI"""
        import pyotp
        
        totp = pyotp.TOTP(secret)
        provisioning_uri = totp.provisioning_uri(name=email, issuer_name=issuer)

        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(provisioning_uri)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")

        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)
        
        img_str = base64.b64encode(buffer.read()).decode()
        return f"data:image/png;base64,{img_str}", provisioning_uri

qr_service = QRService()