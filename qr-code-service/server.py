import io
from concurrent.futures import ThreadPoolExecutor

import grpc
import qrcode
import qrcode.image.pil
import qrcode.image.svg

from qr_code_service_pb2 import ErrorCorrection, ImageFormat, QrCodeResponse
from qr_code_service_pb2_grpc import QrCodeServiceServicer, add_QrCodeServiceServicer_to_server


class ColoredSvgPathImage(qrcode.image.svg.SvgPathImage):
    def __init__(self, *args, **kwargs):
        # Extrahiere die Farbparameter aus kwargs
        self.fill_color = kwargs.pop('fill_color', '#000000')
        self.back_color = kwargs.pop('back_color', '#ffffff')
        super().__init__(*args, **kwargs)
        
        # Setze die Farben korrekt
        self.background = self.back_color
        self.QR_PATH_STYLE = {
            'fill': self.fill_color,
            'fill-opacity': '1',
            'fill-rule': 'nonzero',
            'stroke': 'none'
        }


class QrCodeService(QrCodeServiceServicer):
    def CreateQrCode(self, request, context):
        try:
            version = request.version if 1 <= request.version <= 40 else None

            error_correction = {
                ErrorCorrection.LOW: qrcode.constants.ERROR_CORRECT_L,
                ErrorCorrection.MEDIUM: qrcode.constants.ERROR_CORRECT_M,
                ErrorCorrection.QUARTILE: qrcode.constants.ERROR_CORRECT_Q,
                ErrorCorrection.HIGH: qrcode.constants.ERROR_CORRECT_H,
            }[request.error_correction]

            # Unterschiedliche Behandlung für PNG und SVG
            if request.image_format == ImageFormat.SVG:
                # SVG-spezifische Behandlung
                qr = qrcode.QRCode(
                    version=version,
                    error_correction=error_correction,
                    box_size=request.box_size,
                    border=request.border,
                    image_factory=ColoredSvgPathImage
                )
                qr.add_data(request.data)
                qr.make(fit=True)
                
                # SVG mit Farben erstellen
                image = qr.make_image(fill_color=request.fill_color, back_color=request.back_color)
                
                # SVG als String und dann zu Bytes konvertieren
                svg_string = image.to_string(encoding='unicode')
                byte_array = svg_string.encode('utf-8')
                
            else:
                # PNG-Behandlung (wie bisher)
                qr = qrcode.QRCode(
                    version=version,
                    error_correction=error_correction,
                    box_size=request.box_size,
                    border=request.border
                )
                qr.add_data(request.data)
                qr.make(fit=True)
                
                image = qr.make_image(fill_color=request.fill_color, back_color=request.back_color)
                
                bytes_io = io.BytesIO()
                image.save(bytes_io, format='PNG')
                byte_array = bytes_io.getvalue()

            return QrCodeResponse(file=byte_array)

        except Exception as e:
            print(f"Error creating QR code: {str(e)}")  # Für Debugging
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details(f"Error generating QR code: {str(e)}")
            return QrCodeResponse()


def serve():
    print("Starting server...")
    server = grpc.server(ThreadPoolExecutor(max_workers=10))
    add_QrCodeServiceServicer_to_server(QrCodeService(), server)
    server.add_insecure_port('[::]:5000')
    server.start()
    print("Listening on port 5000")
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
