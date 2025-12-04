#!/usr/bin/env python3
"""Analyze Croody page with Puppeteer and identify improvements."""
import asyncio
from pyppeteer import launch
import os

async def analyze_page():
    browser = await launch(
        headless=True,
        args=['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage']
    )
    page = await browser.newPage()
    await page.setViewport({'width': 1440, 'height': 900})

    print("🎯 Navegando a http://localhost:8001...")
    await page.goto('http://localhost:8001', {'waitUntil': 'networkidle0'})

    # Take full page screenshot
    print("📸 Capturando página completa...")
    await page.screenshot({'path': '/tmp/croody_full.png', 'fullPage': True})

    # Analyze hero section
    print("\n🔍 Analizando sección Hero...")
    hero = await page.querySelector('.landing-hero')
    if hero:
        bounding = await hero.boundingBox()
        print(f"   ✓ Hero encontrado - Dimensiones: {bounding}")

    # Check header
    print("\n🔍 Analizando Header...")
    header = await page.querySelector('.site-header')
    if header:
        bounding = await header.boundingBox()
        print(f"   ✓ Header encontrado - Altura: {bounding['height']}px")

    # Analyze vectors section
    print("\n🔍 Analizando sección Vectores...")
    vectors = await page.querySelector('.landing-vectors__grid')
    if vectors:
        cards = await page.querySelectorAll('.vector-card')
        print(f"   ✓ Vectores encontrados: {len(cards)}")

    # Check if images are loaded
    print("\n🔍 Verificando imágenes...")
    images = await page.querySelectorAll('img')
    for idx, img in enumerate(images[:5]):
        src = await page.evaluate('(el) => el.src', img)
        natural_width = await page.evaluate('(el) => el.naturalWidth', img)
        print(f"   Imagen {idx+1}: {src[:50]}... (Width: {natural_width})")

    # Check console errors
    print("\n⚠️  Verificando errores de consola...")
    logs = []
    page.on('console', lambda msg: logs.append(f"{msg.type}: {msg.text}"))
    await page.reload({'waitUntil': 'networkidle0'})

    if logs:
        print("   Errores encontrados:")
        for log in logs[-10:]:
            print(f"   - {log}")
    else:
        print("   ✓ Sin errores en consola")

    # Check mobile responsiveness
    print("\n📱 Verificando responsive design...")
    await page.setViewport({'width': 375, 'height': 667})
    await page.goto('http://localhost:8001', {'waitUntil': 'networkidle0'})
    await page.screenshot({'path': '/tmp/croody_mobile.png'})
    print("   ✓ Screenshot mobile guardado")

    await browser.close()
    print("\n✅ Análisis completo!")

asyncio.get_event_loop().run_until_complete(analyze_page())
