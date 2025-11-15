import pytesseract
from PIL import Image, ImageFilter, ImageEnhance
import base64
import io
import re

class CodeAnalyzer:
    def __init__(self):
        self.language_patterns = {
            'python': [r'def\s+\w+', r'import\s+\w+', r'class\s+\w+', r'print\(', r'from\s+\w+', r'if\s+.*:', r'for\s+.*:', r'return\s+'],
            'javascript': [r'function\s+\w+', r'const\s+\w+', r'let\s+\w+', r'console\.log', r'export\s+', r'=>', r'document\.'],
            'java': [r'public\s+class', r'void\s+main', r'System\.out', r'import\s+java', r'private\s+', r'protected\s+'],
        }
        
        # Better OCR config for code
        self.ocr_config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789{}[]()<>:=;.,"''_+-*/\\#!@$%^&| \n'
    
    def extract_code_from_image(self, screenshot_data):
        """Extract code from screenshot with better preprocessing"""
        try:
            image_data = base64.b64decode(screenshot_data)
            image = Image.open(io.BytesIO(image_data))
            
            # Focus on likely code areas (top-left quadrant where code editors usually are)
            width, height = image.size
            code_area = image.crop((0, 0, width * 0.7, height * 0.7))  # Top-left 70%
            
            # Enhanced preprocessing
            processed_image = self._enhance_for_code(code_area)
            
            text = pytesseract.image_to_string(processed_image, config=self.ocr_config)
            return self.analyze_code(text)
        except Exception as e:
            return {"error": str(e), "language": "unknown", "code_snippets": [], "line_count": 0, "confidence": 0}
    
    def _enhance_for_code(self, image):
        """Enhanced image preprocessing for code extraction"""
        # Convert to grayscale
        if image.mode != 'L':
            image = image.convert('L')
        
        # Increase contrast
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(2.0)
        
        # Sharpen
        image = image.filter(ImageFilter.SHARPEN)
        
        return image
    
    def analyze_code(self, text):
        """Analyze code with better filtering"""
        # Clean and filter text
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        
        # Remove lines that are clearly not code
        code_lines = []
        for line in lines:
            if self._is_likely_code(line) and len(line) > 3:
                code_lines.append(line)
        
        if len(code_lines) < 2:  # Need at least 2 lines of potential code
            return {"language": "unknown", "code_snippets": [], "line_count": 0, "confidence": 0}
        
        # Detect language
        language_scores = {}
        for lang, patterns in self.language_patterns.items():
            score = sum(1 for pattern in patterns if any(re.search(pattern, line, re.IGNORECASE) for line in code_lines))
            language_scores[lang] = score
        
        # Only consider languages with significant matches
        valid_languages = {lang: score for lang, score in language_scores.items() if score >= 2}
        
        if not valid_languages:
            return {"language": "unknown", "code_snippets": code_lines[:3], "line_count": len(code_lines), "confidence": 0}
        
        detected_language = max(valid_languages, key=valid_languages.get)
        confidence = valid_languages[detected_language] / len(self.language_patterns[detected_language])
        
        # Extract clean code snippets
        code_snippets = self._extract_clean_snippets(code_lines)
        
        return {
            "language": detected_language,
            "code_snippets": code_snippets[:3],
            "line_count": len(code_lines),
            "confidence": round(confidence, 2)
        }
    
    def _is_likely_code(self, line):
        """Better heuristic for code detection"""
        # Exclude common UI/terminal text
        excluded_patterns = [
            r'^[|¦]',  # Terminal borders
            r'^@',     # Mentions
            r'^http',  # URLs
            r'^[A-Z\s]+$',  # All caps (likely UI)
            r'^[0-9/:\.\s]+$',  # Dates/times
        ]
        
        if any(re.search(pattern, line) for pattern in excluded_patterns):
            return False
        
        # Must contain code-like patterns
        code_patterns = [
            r'[a-z]\([a-z]',  # Function calls
            r'=[^=]',         # Assignments (but not ==)
            r'def |class |import |function ',
            r'\{|\}|\(|\)|\[|\]',
            r'\.\w+',         # Method/property access
        ]
        
        return any(re.search(pattern, line) for pattern in code_patterns)
    
    def _extract_clean_snippets(self, code_lines):
        """Extract clean, meaningful code snippets"""
        snippets = []
        current_snippet = []
        
        for line in code_lines:
            if self._is_likely_code(line) and not self._is_noise(line):
                current_snippet.append(line)
                if len(current_snippet) >= 2:
                    snippets.append('\n'.join(current_snippet))
                    current_snippet = []
        
        if current_snippet and len(current_snippet) >= 1:
            snippets.append('\n'.join(current_snippet))
        
        return snippets
    
    def _is_noise(self, line):
        """Filter out noisy lines"""
        noise_patterns = [
            r'^[-\s]*$',  # Mostly dashes/spaces
            r'^[|¦].*[|¦]$',  # Terminal border lines
            r'^[0-9\s]+$',  # Numbers only
        ]
        return any(re.search(pattern, line) for pattern in noise_patterns)

if __name__ == "__main__":
    analyzer = CodeAnalyzer()
    # Test with some realistic mixed content
    test_text = """
    def hello_world():
        print("Hello World")
        return True
    
    | Terminal border
    Some random text
    class Calculator:
        def add(self, a, b):
            return a + b
    """
    result = analyzer.analyze_code(test_text)
    print("Improved Analysis:", result)
