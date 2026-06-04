#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
from PIL import Image

def compress_jpeg(input_path, output_path, quality=75, max_size=(1920, 1080)):
    """
    压缩 JPEG 图片
    
    Args:
        input_path: 输入图片路径
        output_path: 输出图片路径
        quality: 输出质量 (1-100)
        max_size: 最大尺寸 (width, height)
    
    Returns:
        (original_size, compressed_size): 压缩前后的文件大小（字节）
    """
    try:
        with Image.open(input_path) as img:
            original_size = os.path.getsize(input_path)
            
            if img.mode == 'RGBA':
                img = img.convert('RGB')
            
            img.thumbnail(max_size, Image.Resampling.LANCZOS)
            
            img.save(output_path, 'JPEG', quality=quality, optimize=True, progressive=True)
            
            compressed_size = os.path.getsize(output_path)
            
            return (original_size, compressed_size)
    except Exception as e:
        print(f"✗ 压缩失败 {input_path}: {str(e)}")
        return (0, 0)

def compress_png_to_webp(input_path, output_path, quality=70, max_size=(1920, 1080)):
    """
    将 PNG 转换为 WebP 格式进行压缩（保留透明度）
    
    Args:
        input_path: 输入图片路径
        output_path: 输出图片路径
        quality: 输出质量
        max_size: 最大尺寸
    
    Returns:
        (original_size, compressed_size): 压缩前后的文件大小（字节）
    """
    try:
        with Image.open(input_path) as img:
            original_size = os.path.getsize(input_path)
            
            img.thumbnail(max_size, Image.Resampling.LANCZOS)
            
            img.save(output_path, 'WEBP', quality=quality, lossless=False)
            
            compressed_size = os.path.getsize(output_path)
            
            return (original_size, compressed_size)
    except Exception as e:
        print(f"✗ WebP 压缩失败 {input_path}: {str(e)}")
        return (0, 0)

def compress_png_to_jpeg(input_path, output_path, quality=75, max_size=(1920, 1080)):
    """
    将 PNG 转换为 JPEG 格式进行压缩（丢弃透明度）
    
    Args:
        input_path: 输入图片路径
        output_path: 输出图片路径
        quality: 输出质量
        max_size: 最大尺寸
    
    Returns:
        (original_size, compressed_size): 压缩前后的文件大小（字节）
    """
    try:
        with Image.open(input_path) as img:
            original_size = os.path.getsize(input_path)
            
            if img.mode in ('RGBA', 'P'):
                background = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'RGBA':
                    background.paste(img, mask=img.split()[3])
                else:
                    background.paste(img)
                img = background
            
            img.thumbnail(max_size, Image.Resampling.LANCZOS)
            
            img.save(output_path, 'JPEG', quality=quality, optimize=True, progressive=True)
            
            compressed_size = os.path.getsize(output_path)
            
            return (original_size, compressed_size)
    except Exception as e:
        print(f"✗ JPEG 转换失败 {input_path}: {str(e)}")
        return (0, 0)

def compress_png_optimize(input_path, output_path, max_size=(1920, 1080)):
    """
    优化 PNG（无损压缩）
    
    Args:
        input_path: 输入图片路径
        output_path: 输出图片路径
        max_size: 最大尺寸
    
    Returns:
        (original_size, compressed_size): 压缩前后的文件大小（字节）
    """
    try:
        with Image.open(input_path) as img:
            original_size = os.path.getsize(input_path)
            
            img.thumbnail(max_size, Image.Resampling.LANCZOS)
            
            if img.mode == 'P':
                img = img.convert('RGBA')
            
            img.save(output_path, 'PNG', optimize=True)
            
            compressed_size = os.path.getsize(output_path)
            
            return (original_size, compressed_size)
    except Exception as e:
        print(f"✗ PNG 优化失败 {input_path}: {str(e)}")
        return (0, 0)

def main():
    if len(sys.argv) < 2:
        print("用法: python compress_images.py <图片文件夹路径>")
        print("示例: python compress_images.py c:\\Users\\ALTC\\Desktop\\PyLearning\\MetlifeBuildinExhi\\met\\Designs")
        sys.exit(1)
    
    input_dir = sys.argv[1]
    
    if not os.path.isdir(input_dir):
        print(f"错误: {input_dir} 不是有效的文件夹路径")
        sys.exit(1)
    
    output_dir = os.path.join(input_dir, 'compressed')
    os.makedirs(output_dir, exist_ok=True)
    
    supported_formats = ('.jpg', '.jpeg', '.png', '.JPG', '.JPEG', '.PNG')
    
    total_original = 0
    total_compressed = 0
    processed_count = 0
    skipped_count = 0
    converted_to_jpeg = 0
    converted_to_webp = 0
    
    print("=" * 60)
    print("图片压缩工具 - 增强版")
    print("=" * 60)
    print(f"输入目录: {input_dir}")
    print(f"输出目录: {output_dir}")
    print("-" * 60)
    
    for filename in os.listdir(input_dir):
        if not filename.lower().endswith(supported_formats):
            continue
        
        if os.path.isdir(os.path.join(input_dir, filename)):
            continue
        
        input_path = os.path.join(input_dir, filename)
        basename, ext = os.path.splitext(filename)
        
        if ext.lower() == '.png':
            webp_path = os.path.join(output_dir, basename + '.webp')
            jpeg_path = os.path.join(output_dir, basename + '.jpg')
            
            orig_size = os.path.getsize(input_path)
            
            webp_result = compress_png_to_webp(input_path, webp_path, quality=75)
            jpeg_result = compress_png_to_jpeg(input_path, jpeg_path, quality=75)
            
            if webp_result[1] > 0 and jpeg_result[1] > 0:
                if webp_result[1] < jpeg_result[1]:
                    original, compressed = webp_result
                    output_path = webp_path
                    converted_to_webp += 1
                else:
                    original, compressed = jpeg_result
                    output_path = jpeg_path
                    converted_to_jpeg += 1
            elif webp_result[1] > 0:
                original, compressed = webp_result
                output_path = webp_path
                converted_to_webp += 1
            elif jpeg_result[1] > 0:
                original, compressed = jpeg_result
                output_path = jpeg_path
                converted_to_jpeg += 1
            else:
                original, compressed = compress_png_optimize(input_path, os.path.join(output_dir, filename))
        else:
            output_path = os.path.join(output_dir, basename + '.jpg')
            original, compressed = compress_jpeg(input_path, output_path, quality=75)
        
        if original > 0:
            processed_count += 1
            total_original += original
            total_compressed += compressed
            
            ratio = (1 - compressed / original) * 100
            
            orig_size = f"{original / 1024:.1f} KB" if original < 1024 * 1024 else f"{original / (1024 * 1024):.2f} MB"
            comp_size = f"{compressed / 1024:.1f} KB" if compressed < 1024 * 1024 else f"{compressed / (1024 * 1024):.2f} MB"
            
            print(f"✓ {filename}")
            print(f"   原始: {orig_size} → 压缩后: {comp_size} ({ratio:.1f}% 减少)")
        else:
            skipped_count += 1
    
    print("-" * 60)
    print("压缩完成！")
    print("=" * 60)
    print(f"处理文件: {processed_count} 个")
    print(f"跳过文件: {skipped_count} 个")
    print(f"转换为 WebP: {converted_to_webp} 个")
    print(f"转换为 JPEG: {converted_to_jpeg} 个")
    
    if total_original > 0:
        orig_total = f"{total_original / (1024 * 1024):.2f} MB"
        comp_total = f"{total_compressed / (1024 * 1024):.2f} MB"
        total_ratio = (1 - total_compressed / total_original) * 100
        
        print(f"原始总大小: {orig_total}")
        print(f"压缩后总大小: {comp_total}")
        print(f"总压缩率: {total_ratio:.1f}%")
        print(f"节省空间: {(total_original - total_compressed) / (1024 * 1024):.2f} MB")

if __name__ == "__main__":
    main()