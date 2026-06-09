import os
import argparse
import datetime
from pathlib import Path
import ast
import re
import zipfile
import xml.etree.ElementTree as ET

IGNORE_DIRS = {
    '.git', '__pycache__', 'node_modules', 'venv', 'env', '.venv', 
    '.idea', '.vscode', 'dist', 'build', 'temp', 'Archive', 'cache',
    'plugins', 'embedding_models', 'event_logs'
}

IGNORE_EXTS = {
    '.exe', '.dll', '.so', '.dylib', '.class', '.pyc', 
    '.zip', '.tar', '.gz', '.rar', '.7z', '.whl',
    '.png', '.jpg', '.jpeg', '.gif', '.svg', '.ico', '.webp',
    '.mp3', '.mp4', '.avi',
    '.sqlite', '.sqlite3', '.db', '.iso', '.bin', '.laz', '.las', 
    '.pdf', '.doc', '.xls', '.ppt',
    '.skp', '.skb', '.dae'
}

def strip_html_tags(text):
    text = re.sub(r'<script.*?>.*?</script>', '', text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r'<style.*?>.*?</style>', '', text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r'<br\s*/?>', '\n', text, flags=re.IGNORECASE)
    text = re.sub(r'</p>', '\n\n', text, flags=re.IGNORECASE)
    text = re.sub(r'<h1.*?>', '# ', text, flags=re.IGNORECASE)
    text = re.sub(r'<h2.*?>', '## ', text, flags=re.IGNORECASE)
    text = re.sub(r'<h3.*?>', '### ', text, flags=re.IGNORECASE)
    text = re.sub(r'<li.*?>', '- ', text, flags=re.IGNORECASE)
    text = re.sub(r'<.*?>', '', text)
    return re.sub(r'\n{3,}', '\n\n', text).strip()

def generate_tree(dir_path, prefix=""):
    tree_str = ""
    try:
        paths = sorted([p for p in dir_path.iterdir() if p.name not in IGNORE_DIRS and not p.name.startswith('.')], 
                       key=lambda p: (p.is_file(), p.name.lower()))
    except PermissionError:
        return f"{prefix}[Přístup odepřen]\n"

    for i, path in enumerate(paths):
        is_last = (i == len(paths) - 1)
        connector = "└── " if is_last else "├── "
        tree_str += f"{prefix}{connector}{path.name}\n"
        if path.is_dir():
            extension_prefix = "    " if is_last else "│   "
            tree_str += generate_tree(path, prefix + extension_prefix)
    return tree_str

def extract_openxml_text(filepath, ext):
    try:
        text_content = []
        with zipfile.ZipFile(filepath, 'r') as z:
            xml_files = ['word/document.xml'] if ext == '.docx' else (['xl/sharedStrings.xml'] if ext == '.xlsx' else [])
            for xml_file in xml_files:
                if xml_file in z.namelist():
                    root = ET.fromstring(z.read(xml_file))
                    for node in root.iter():
                        if node.tag.endswith('}t') and node.text: text_content.append(node.text)
        return re.sub(r'\n{3,}', '\n\n', "\n".join(text_content)).strip()
    except Exception as e: 
        return f"[Chyba OpenXML: {str(e)}]"

def is_text_file_heuristic(filepath):
    try:
        with open(filepath, 'rb') as f:
            return b'\x00' not in f.read(8192)
    except: 
        return False

def get_file_content(file_path):
    ext = file_path.suffix.lower()
    try:
        if ext in {'.docx', '.xlsx', '.pptx'}: return extract_openxml_text(file_path, ext)
        with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
            return strip_html_tags(content) if ext in {'.html', '.htm'} else content
    except Exception as e:
        return f"[Chyba I/O: {str(e)}]"

def format_snippet(content, ext, size_bytes):
    """Proč: AST pro Python nechává AI pohled na logiku metod a tříd bez detailů iterací."""
    if not content: return "[Prázdný nebo nečitelný obsah]"
    if ext == '.py':
        try:
            tree = ast.parse(content)
            skeleton = []
            for n in tree.body:
                if isinstance(n, (ast.Import, ast.ImportFrom)): continue
                if isinstance(n, ast.FunctionDef): skeleton.append(f"def {n.name}(...):")
                elif isinstance(n, ast.ClassDef): skeleton.append(f"class {n.name}:")
            return "\n".join(skeleton) if skeleton else content[:500] + "..."
        except: return content[:500] + "..."
    return content[:1000] + ("..." if len(content) > 1000 else "")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("dir", nargs="?", default=".", help="Cílová složka")
    args = parser.parse_args()
    
    source = Path(args.dir).resolve()
    output_file = source / f"index_{source.name}.md"
    
    try:
        with open(output_file, 'w', encoding='utf-8') as out:
            # YAML front-matter pro master kontext
            out.write("---\n")
            out.write(f"title: Master_Context_{source.name}\n")
            out.write(f"source_url: local_tree://{source}\n")
            out.write(f"scraped_at: {datetime.datetime.now().isoformat()}\n")
            out.write("topic: code_context_map\n")
            out.write("data_type: markdown\n")
            out.write("---\n\n")
            
            out.write(f"# Zdrojový strom: {source.name}\n\n```text\n")
            out.write(generate_tree(source))
            out.write("\n```\n\n---\n\n")
            
            for root, dirs, files in os.walk(source):
                dirs[:] = [d for d in dirs if d not in IGNORE_DIRS and not d.startswith('.')]
                for f in files:
                    file_path = Path(root) / f
                    if file_path.name == "_index_v5.md" or file_path.suffix.lower() in IGNORE_EXTS:
                        continue
                    if not is_text_file_heuristic(file_path):
                        continue
                        
                    rel_path = file_path.relative_to(source)
                    out.write(f"## 📄 `{rel_path}`\n\n")
                    content = get_file_content(file_path)
                    snippet = format_snippet(content, file_path.suffix.lower(), file_path.stat().st_size)
                    
                    lang_hint = file_path.suffix.lower().replace('.', '')
                    out.write(f"```{lang_hint}\n{snippet}\n```\n\n")
                    
    except Exception as e:
        print(f"Chyba: {e}")

if __name__ == "__main__":
    main()
