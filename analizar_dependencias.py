"""
Script para analizar dependencias de archivos en src/
Identifica qué archivos se importan y cuáles se pueden eliminar
"""

import os
import re
from pathlib import Path

RAIZ = Path(__file__).parent
SRC_DIR = RAIZ / "src"
NOTEBOOKS_DIR = RAIZ / "notebooks"

def obtener_archivos_src():
    """Obtiene todos los archivos .py en src/"""
    if not SRC_DIR.exists():
        return []
    return [f.stem for f in SRC_DIR.glob("*.py") if f.stem != "__init__"]

def buscar_imports_en_archivo(ruta_archivo):
    """Busca todos los imports en un archivo Python"""
    imports = set()
    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as f:
            contenido = f.read()
        
        # Buscar imports del tipo: from modulo import ...
        patron_from = r'from\s+([\w]+)\s+import'
        matches_from = re.findall(patron_from, contenido)
        imports.update(matches_from)
        
        # Buscar imports del tipo: import modulo
        patron_import = r'^import\s+([\w]+)'
        matches_import = re.findall(patron_import, contenido, re.MULTILINE)
        imports.update(matches_import)
    except Exception as e:
        print(f"  ⚠️ Error leyendo {ruta_archivo}: {e}")
    
    return imports

def buscar_imports_en_notebooks():
    """Busca todos los imports en los notebooks"""
    imports = set()
    if not NOTEBOOKS_DIR.exists():
        return imports
    
    for notebook in NOTEBOOKS_DIR.glob("*.ipynb"):
        try:
            import json
            with open(notebook, 'r', encoding='utf-8') as f:
                nb = json.load(f)
            
            for cell in nb.get('cells', []):
                if cell.get('cell_type') == 'code':
                    source = ''.join(cell.get('source', []))
                    # Buscar from src.modulo import
                    patron = r'from\s+src\.([\w]+)\s+import'
                    matches = re.findall(patron, source)
                    imports.update(matches)
                    
                    # Buscar from modulo import (sin src.)
                    patron2 = r'from\s+([\w]+)\s+import'
                    matches2 = re.findall(patron2, source)
                    imports.update(matches2)
        except Exception as e:
            print(f"  ⚠️ Error leyendo {notebook}: {e}")
    
    return imports

def analizar_dependencias():
    """Analiza todas las dependencias"""
    print("="*70)
    print("🔍 ANÁLISIS DE DEPENDENCIAS DE src/")
    print("="*70)
    
    archivos_src = obtener_archivos_src()
    print(f"\n📁 Archivos en src/: {archivos_src}")
    
    # Buscar imports en notebooks
    imports_notebooks = buscar_imports_en_notebooks()
    print(f"\n📓 Módulos importados en notebooks: {imports_notebooks}")
    
    # Analizar dependencias entre archivos de src/
    print("\n" + "="*70)
    print("🔗 DEPENDENCIAS ENTRE ARCHIVOS DE src/")
    print("="*70)
    
    archivos_usados = set()
    
    for archivo in archivos_src:
        ruta = SRC_DIR / f"{archivo}.py"
        imports = buscar_imports_en_archivo(ruta)
        
        # Filtrar solo imports que son archivos de src/
        imports_src = [imp for imp in imports if imp in archivos_src and imp != archivo]
        
        if imports_src:
            print(f"  📄 {archivo}.py → importa: {imports_src}")
            archivos_usados.update(imports_src)
        else:
            print(f"  📄 {archivo}.py → no importa otros archivos de src/")
    
    # Identificar archivos que NO se importan en ningún lado
    print("\n" + "="*70)
    print("🗑️ ARCHIVOS CANDIDATOS A ELIMINAR")
    print("="*70)
    
    archivos_no_usados = []
    for archivo in archivos_src:
        if archivo not in imports_notebooks and archivo not in archivos_usados:
            if archivo != "__init__":
                archivos_no_usados.append(archivo)
                print(f"  🗑️ {archivo}.py - NO se usa en notebooks ni en otros archivos de src/")
    
    if not archivos_no_usados:
        print("  ✅ Todos los archivos de src/ están siendo utilizados")
    
    # Mostrar archivos que SÍ se usan
    print("\n" + "="*70)
    print("✅ ARCHIVOS EN USO")
    print("="*70)
    
    archivos_en_uso = [a for a in archivos_src if a in imports_notebooks or a in archivos_usados]
    for archivo in archivos_en_uso:
        print(f"  ✅ {archivo}.py")
    
    return archivos_no_usados

if __name__ == "__main__":
    archivos_eliminar = analizar_dependencias()
    
    if archivos_eliminar:
        print("\n" + "="*70)
        print("⚠️ RECOMENDACIÓN")
        print("="*70)
        print("Los siguientes archivos parecen no estar en uso:")
        for archivo in archivos_eliminar:
            print(f"  - src/{archivo}.py")
        print("\n⚠️ ANTES DE ELIMINAR, verifica manualmente que no se usen en otro lugar.")