"""
Duck Decoder - Python version (100% translated from duckDecoder.ts)
Decodes ss_tools encrypted "duck" images using LSB steganography.
Supports optional password protection (SHA256 + XOR stream cipher).
"""

import hashlib
import io
from PIL import Image
from typing import Dict, Any, Optional, Union

# Constants matching ss_tools encoder
WATERMARK_SKIP_W_RATIO = 0.40
WATERMARK_SKIP_H_RATIO = 0.08


def generate_key_stream(password: str, salt: bytes, length: int) -> bytes:
    """Generate key stream for XOR decryption (matching TS version)"""
    encoder = lambda s: s.encode('utf-8')
    salt_hex = ''.join(f'{b:02x}' for b in salt)
    key_material = encoder(password + salt_hex)
    out = bytearray(length)
    offset = 0
    counter = 0
    while offset < length:
        counter_bytes = encoder(str(counter))
        combined = key_material + counter_bytes
        hash_bytes = hashlib.sha256(combined).digest()
        copy_len = min(len(hash_bytes), length - offset)
        out[offset:offset + copy_len] = hash_bytes[:copy_len]
        offset += copy_len
        counter += 1
    return bytes(out)


def sha256(data: bytes) -> bytes:
    """Compute SHA256 hash"""
    return hashlib.sha256(data).digest()


def extract_payload_with_k(image: Image.Image, k: int) -> bytes:
    """Extract LSB payload with given bit width (matching extractPayloadWithK)"""
    width, height = image.size
    skip_w = int(width * WATERMARK_SKIP_W_RATIO)
    skip_h = int(height * WATERMARK_SKIP_H_RATIO)
    pixels = image.load()

    values: list[int] = []
    for y in range(height):
        for x in range(width):
            if y < skip_h and x < skip_w:
                continue
            r, g, b = pixels[x, y][:3]  # skip alpha
            mask = (1 << k) - 1
            values.extend([r & mask, g & mask, b & mask])

    # Unpack bits
    bits: list[int] = []
    for val in values:
        for i in range(k - 1, -1, -1):
            bits.append((val >> i) & 1)

    if len(bits) < 32:
        raise ValueError('Insufficient image data')

    # Read length prefix (32 bits, big-endian)
    header_len = 0
    for i in range(32):
        header_len = (header_len << 1) | bits[i]

    if header_len <= 0 or 32 + header_len * 8 > len(bits):
        raise ValueError('Payload length invalid')

    # Extract payload bytes
    payload_bits = bits[32:32 + header_len * 8]
    payload = bytearray(header_len)
    for i in range(header_len):
        byte = 0
        for j in range(8):
            byte = (byte << 1) | payload_bits[i * 8 + j]
        payload[i] = byte
    return bytes(payload)


def arrays_equal(a: bytes, b: bytes) -> bool:
    """Compare two byte arrays"""
    return a == b


async def decode_duck_image(
    image_source: Union[str, bytes, io.BytesIO],
    password: str = ''
) -> Dict[str, Any]:
    """
    主解码函数（和 TS 的 decodeDuckImage 完全一致）
    image_source 可以是：
      - 本地文件路径 (str)
      - 原始字节 (bytes)
      - BytesIO 对象
    返回结果和 TS 版一致，便于 skill 直接使用
    """
    try:
        # 加载图片
        if isinstance(image_source, str):
            img = Image.open(image_source).convert('RGBA')
        elif isinstance(image_source, bytes):
            img = Image.open(io.BytesIO(image_source)).convert('RGBA')
        else:
            img = Image.open(image_source).convert('RGBA')

        # 尝试不同 k 值 (2,6,8)
        payload = None
        parsed = None
        last_error = None
        for k in [2, 6, 8]:
            try:
                payload = extract_payload_with_k(img, k)
                parsed = await _parse_header(payload, password)
                break
            except Exception as e:
                last_error = e
                continue

        if not parsed:
            if getattr(last_error, 'type', None) == 'PASSWORD_REQUIRED':
                return {'success': False, 'error': 'PASSWORD_REQUIRED', 'errorMessage': 'Password required'}
            if getattr(last_error, 'type', None) == 'WRONG_PASSWORD':
                return {'success': False, 'error': 'WRONG_PASSWORD', 'errorMessage': 'Wrong password'}
            return {'success': False, 'error': 'NOT_DUCK_IMAGE', 'errorMessage': 'Not a valid duck image'}

        final_data = parsed['data']
        final_ext = parsed['ext']

        # 处理 .binpng 格式（视频数据）
        if final_ext.endswith('.binpng'):
            binpng_img = Image.open(io.BytesIO(final_data)).convert('RGBA')
            final_data = _binpng_to_bytes(binpng_img)
            final_ext = final_ext.replace('.binpng', '')

        # 决定 MIME 类型（仅供参考）
        mime_map = {
            'png': 'image/png', 'jpg': 'image/jpeg', 'jpeg': 'image/jpeg',
            'webp': 'image/webp', 'gif': 'image/gif',
            'mp4': 'video/mp4', 'webm': 'video/webm', 'mov': 'video/quicktime'
        }
        mime_type = mime_map.get(final_ext.lower(), 'application/octet-stream')

        return {
            'success': True,
            'data': final_data,           # 解码后的原始字节（干净图片/视频/JSON）
            'extension': final_ext,
            'mime_type': mime_type
        }

    except Exception as e:
        return {
            'success': False,
            'error': 'DECODE_FAILED',
            'errorMessage': str(e)
        }


async def _parse_header(header: bytes, password: str) -> Dict[str, Any]:
    """解析头部（和 TS parseHeader 完全一致）"""
    idx = 0
    if len(header) < 1:
        raise ValueError('Header corrupted')
    has_pwd = header[0] == 1
    idx += 1
    pwd_hash = None
    salt = None
    if has_pwd:
        if len(header) < idx + 32 + 16:
            raise ValueError('Header corrupted')
        pwd_hash = header[idx:idx + 32]
        idx += 32
        salt = header[idx:idx + 16]
        idx += 16
    if len(header) < idx + 1:
        raise ValueError('Header corrupted')
    ext_len = header[idx]
    idx += 1
    if len(header) < idx + ext_len + 4:
        raise ValueError('Header corrupted')
    ext_bytes = header[idx:idx + ext_len]
    ext = ext_bytes.decode('utf-8')
    idx += ext_len
    # Read data length (4 bytes big-endian)
    data_len = (header[idx] << 24) | (header[idx + 1] << 16) | (header[idx + 2] << 8) | header[idx + 3]
    idx += 4
    data = header[idx:]
    if len(data) != data_len:
        raise ValueError('Data length mismatch')

    if not has_pwd:
        return {'data': data, 'ext': ext}

    if not password:
        err = Exception('Password required')
        err.type = 'PASSWORD_REQUIRED'
        raise err

    # Verify password
    encoder = lambda s: s.encode('utf-8')
    salt_hex = ''.join(f'{b:02x}' for b in salt)
    check_hash = sha256(encoder(password + salt_hex))
    if not arrays_equal(check_hash, pwd_hash):
        err = Exception('Wrong password')
        err.type = 'WRONG_PASSWORD'
        raise err

    # XOR decrypt
    key_stream = generate_key_stream(password, salt, len(data))
    plain = bytearray(len(data))
    for i in range(len(data)):
        plain[i] = data[i] ^ key_stream[i]
    return {'data': bytes(plain), 'ext': ext}


def _binpng_to_bytes(image: Image.Image) -> bytes:
    """Convert binpng to raw bytes (matching binpngToBytes)"""
    width, height = image.size
    pixels = image.load()
    bytes_list = []
    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y][:3]
            bytes_list.extend([r, g, b])
    # Trim trailing zeros
    while bytes_list and bytes_list[-1] == 0:
        bytes_list.pop()
    return bytes(bytes_list)


# 可选：快速检查是否可能是鸭子图
async def might_be_duck_image(image_source: Union[str, bytes, io.BytesIO]) -> bool:
    result = await decode_duck_image(image_source)
    return result['success'] or result.get('error') == 'PASSWORD_REQUIRED'
